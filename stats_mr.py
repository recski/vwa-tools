import json
from collections import Counter

from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol


class EssayStats(MRJob):

    OUTPUT_PROTOCOL = RawValueProtocol

    def mapper(self, _, line):
        try:
            doc = json.loads(line)
            lang = doc['lang']
            yield "lang", (lang, 1)
            if lang == 'de':
                no_sens = len(doc['text']['sents'])
                no_toks = len(doc['text']['tokens'])

                yield 'n_sens', no_sens
                yield 'n_toks', no_toks

        except TypeError:
            doc_id = doc['id']
            yield (f'_PARSE_ERROR_{doc_id}', doc['school_id']), 1

    def combiner(self, key, counts):
        if key == "lang":
            lang_sums = Counter()
            for lang, n in counts:
                lang_sums[lang] += n
            for lang, n in lang_sums.most_common():
                yield key, (lang, n)
        else:
            N, S = 0, 9
            for c in counts:
                N += 1
                S += c
            yield key, (N, S)

    def reducer(self, key, sums):
        if key == "lang":
            lang_sums = Counter()
            for lang, n in sums:
                lang_sums[lang] += n
            for lang, n in lang_sums.most_common():
                yield None, "lang {}: {}".format(lang, n)
        else:
            N, S = 0, 0
            for n, s in sums:
                N += n
                S += s
            yield None, "avg {}:, {:.2f}".format(key, S / N)


if __name__ == "__main__":
    EssayStats.run()
