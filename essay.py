
import csv
import json
import logging
import sys
from collections import Counter

import langdetect
import spacy
import stanza
from tqdm import tqdm

csv.field_size_limit(sys.maxsize)
spacy.prefer_gpu()

DETECT_LANG = True


class VWAEssay():
    @staticmethod
    def gen_from_csv(fn, max_n):
        with open(fn) as f:
            for i, row in tqdm(enumerate(
                    csv.reader(f, delimiter=",", quotechar='"'))):
                if i == max_n:
                    return
                if i == 0:
                    continue
                try:
                    yield VWAEssay.from_csv_row(row)
                except ValueError:
                    logging.error(f'error parsing row #{i}: {row}')
                    continue

    @staticmethod
    def from_csv_row(row):
        doc_id, school_id, title, grade, notes, essay = row
        return VWAEssay(doc_id, school_id, title, grade, notes, essay)

    @staticmethod
    def from_dict(doc):
        doc_id = doc["id"]
        school_id = doc['school_id']
        title = doc['title']
        grade = doc['grade']
        notes = doc['notes']
        essay = doc['text']
        analyzed = isinstance(essay, dict)  # override flag for now
        lang = doc['lang']

        return VWAEssay(
            doc_id, school_id, title, grade, notes, essay, analyzed, lang)

    @staticmethod
    def preprocess_text(raw_text):
        return raw_text.replace('\n', ' ')[:999999]

    @staticmethod
    def _analyze(raw_text, nlp, doc_id):
        text = VWAEssay.preprocess_text(raw_text)
        if isinstance(nlp, spacy.language.Language):
            return VWAEssay._analyze_spacy(text, nlp, doc_id)
        elif isinstance(nlp, stanza.Pipeline):
            return VWAEssay._analyze_stanza(text, nlp, doc_id)
        else:
            raise ValueError('unknown processor type: ' + str(type(nlp)))

    @staticmethod
    def _analyze_spacy(text, nlp, doc_id):
        return nlp(text).to_json()

    @staticmethod
    def _analyze_stanza(text, nlp, doc_id):
        return [
            {
                "sen_id": f'{doc_id}_{i}',
                "text": sen.text,
                'tokens': sen.to_dict()}
            for i, sen in enumerate(nlp(text).sentences)]

    def __init__(
            self, doc_id, school_id, title, grade, notes, essay,
            analyzed=False, lang=None):
        self.doc_id = doc_id
        self.school_id = school_id
        self.title = title
        self.grade = grade
        self.notes = notes.strip() if isinstance(notes, str) else notes
        self.text = essay.strip() if isinstance(essay, str) else essay
        self.analyzed = analyzed
        self.lang = lang
        if self.lang is None:
            assert isinstance(self.text, str)
            self.detect_lang()

    def _detect_lang(self):
        if self.text:
            self.lang = langdetect.detect(self.text[:1000])
        elif self.title:
            self.lang = langdetect.detect(self.title[:1000])
        else:
            raise ValueError('empty title and text in {}'.format(self.doc_id))
            # self.lang = 'de'

    def detect_lang(self):
        if not DETECT_LANG:
            self.lang = 'de'
        try:
            return self._detect_lang()
        except (
                ValueError,
                langdetect.lang_detect_exception.LangDetectException):
            logging.debug('langdetect failed on {}, (doc {}), '.format(
                self.text[:1000], self.doc_id) + 'falling back to "de"')
            self.lang = 'de'

    def analyze(self, nlp):
        self.notes = VWAEssay._analyze(self.notes, nlp, self.doc_id)
        self.text = VWAEssay._analyze(self.text, nlp, self.doc_id)
        self.analyzed = True

    def to_dict(self):
        return {
            "id": self.doc_id,
            "lang": self.lang,
            "school_id": self.school_id,
            "title": self.title,
            "grade": self.grade,
            "notes": self.notes,
            "text": self.text,
            "analyzed": self.analyzed}


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s : " +
        "%(module)s (%(lineno)s) - %(levelname)s - %(message)s")
    # nlp = stanza.Pipeline('de')
    nlp = {
        "de": spacy.load("de_core_news_sm"),
        "en": spacy.load("en_core_web_sm")}
    fn, out_fn = sys.argv[1:3]
    max_n = int(sys.argv[3])
    lang_stats = Counter()
    with open(out_fn, 'w') as f:
        for essay in VWAEssay.gen_from_csv(fn, max_n):
            if essay.lang in nlp:
                essay.analyze(nlp[essay.lang])
            lang_stats[essay.lang] += 1
            f.write(json.dumps(essay.to_dict()))
            f.write('\n')
    print('lang stats:', lang_stats.most_common())


if __name__ == "__main__":
    main()
