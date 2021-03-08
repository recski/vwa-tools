import json
from collections import Counter

from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol


class EssayStats(MRJob):

    OUTPUT_PROTOCOL = RawValueProtocol

    def mapper(self, _, line):
        try:
            doc = json.loads(line)
            if doc['lang'] == 'de':
                for token in doc['text']['tokens']:
                    lemma = token['lemma'].strip()
                    if lemma:
                        yield (token['lemma'], doc['school_id']), 1
        except TypeError:
            doc_id = doc['id']
            yield (f'_PARSE_ERROR_{doc_id}', doc['school_id']), 1

    def combiner(self, key, counts):
        key1, key2 = key
        yield key1, (key2, sum(counts))

    def reducer(self, key1, key2_counts):
        count_by_key2 = Counter()
        total = 0
        for key2, count in key2_counts:
            count_by_key2[key2] += count
            total += count

        yield None, "{0}\t{1}\t{2}".format(key1, total, ",".join(
            f"{key2}:{count}" for key2, count in count_by_key2.most_common()))


if __name__ == "__main__":
    EssayStats.run()
