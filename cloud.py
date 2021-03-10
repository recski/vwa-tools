import json
import sys
from collections import defaultdict

import numpy as np
import spacy
from wordcloud import WordCloud
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.stats import entropy
from tuw_nlp.common.vocabulary import Vocabulary

from common import EXTRA_STOPWORDS


PLZ = [
    "1010", "1020", "1100", "1210"]
# PLZ = [
#    "1020", "1030", "1040", "1050", "1060", "1070", "1080", "1090", "1100",
#    "1110", "1120", "1130", "1140", "1150", "1160", "1170", "1180", "1190",
#    "1200", "1210", "1220", "1230"]


SW = set(stopwords.words('german'))

SW |= EXTRA_STOPWORDS

TFIDF = False

ENTROPY_THRESHOLD = 1.2


def keep(word):
    if not word.isalpha():
        return False
    if word.lower() in SW:
        return False
    if not word.istitle():
        return False
    return True


def keep_counts(word, freqs_by_plz):
    freqs = list(freqs_by_plz.values())
    ent = entropy(freqs)
    keep = ent < ENTROPY_THRESHOLD
    print(ent, word, freqs, keep)
    return keep


def get_counts(stream):
    print('reading vocabulary...')
    count_by_plz = {plz: defaultdict(int) for plz in PLZ}
    vocab = Vocabulary()
    for line in stream:
        fields = line.strip().split('\t')
        if len(fields) != 3:
            print('skipping line:', line)
            continue
        word, _ = fields[0], int(fields[1])
        if keep(word):
            freqs_by_plz = {}
            vocab.add(word)
            for field in fields[2].split(','):
                plz, freq = field.split(':')
                if plz in PLZ:
                    freqs_by_plz[plz] = int(freq)

            if keep_counts(word, freqs_by_plz):
                for plz, freq in freqs_by_plz.items():
                    count_by_plz[plz][word] = freq

    return count_by_plz, vocab


def get_tfidf(count_by_plz, vocab):
    print('building array...')
    counts = np.array([
        [count_by_plz[plz][vocab.get_word(i)] for plz in PLZ]
        for i in range(len(vocab))])
    counts = counts.transpose()
    print('done, shape:', counts.shape)

    print('calculating TFIDF...')
    tfidf = TfidfTransformer().fit_transform(counts)
    print('done, type and shape:', type(tfidf), tfidf.shape)

    cx = tfidf.tocoo()
    tfidf_by_plz = {plz: defaultdict(int) for plz in PLZ}
    for i, j, v in zip(cx.row, cx.col, cx.data):
        tfidf_by_plz[PLZ[i]][vocab.get_word(j)] = v

    return tfidf_by_plz


def generate_wordcloud(count, fn):
    wc = WordCloud(width=800, height=400)
    wc.generate_from_frequencies(count)
    wc.to_file(fn)


def generate_wordclouds(count_by_plz):
    print('generating wordclouds...')
    for plz in PLZ:
        fn = f"wordclouds/{plz}.png"
        generate_wordcloud(count_by_plz[plz], fn)


def get_words(text, nlp):
    return [w.text for w in nlp(text)]


def from_json(stream, field='text'):
    nlp = spacy.load("de_core_news_sm")
    counter = defaultdict(int)
    for line in stream:
        d = json.loads(line)
        for word in get_words(d[field], nlp):
            counter[word] += 1

    return counter


def print_count(count, fn):
    with open(fn, 'w') as f:
        for word, count in sorted(count.items(), key=lambda x: -x[1]):
            f.write(f"{word}\t{count}\n")


def load_count(fn):
    count = defaultdict(int)
    with open(fn) as f:
        for line in f:
            try:
                word, freq = line.strip().split('\t')
            except ValueError:
                continue
            count[word] = int(freq)
    return count


def filter_count(count):
    return {word: freq for word, freq in count.items() if keep(word)}


def main():
    # count_by_plz, vocab = get_counts(sys.stdin)
    # count = from_json(sys.stdin, field='title')
    # print_count(count, sys.argv[2])
    # count = filter_count(count)
    # generate_wordcloud(count, sys.argv[1])

    count = load_count(sys.argv[1])
    count = filter_count(count)
    generate_wordcloud(count, sys.argv[2])

    # if TFIDF:
    #    count_by_plz = get_tfidf(count_by_plz, vocab)
    #
    # generate_wordclouds(count_by_plz)


if __name__ == "__main__":
    main()
