import csv
import sys
from collections import Counter, defaultdict


def load_skz_to_plz(fn):
    skz_to_plz = {}
    with open(fn) as f:
        for row in csv.reader(f, delimiter=",", quotechar='"'):
            if not row[0]:
                continue
            _, skz, __, ___, plz = row
            skz_to_plz[skz] = plz

    return skz_to_plz


def counts_to_plz(stream, skz_to_plz):
    words_to_counts = defaultdict(Counter)
    word_totals = Counter()
    unknown_skz = set()
    for line in stream:
        fields = line.strip().split('\t')
        word, freq, skz_freqs = fields
        word_totals[word] = int(freq)
        for skz, freq in [s.split(':') for s in skz_freqs.split(',')]:
            if skz in unknown_skz:
                continue
            plz = skz_to_plz.get(skz)
            if plz is None:
                unknown_skz.add(skz)
                continue
            words_to_counts[word][plz] += int(freq)

    for word, freq in word_totals.most_common():
        print("{0}\t{1}\t{2}".format(
            word, freq, ",".join(
                f"{plz}:{plz_freq}"
                for plz, plz_freq in words_to_counts[word].most_common())))

    sys.stderr.write("unknown SKZs: " + ",".join(unknown_skz) + "\n")


def main():
    skz_to_plz = load_skz_to_plz(sys.argv[1])
    counts_to_plz(sys.stdin, skz_to_plz)


if __name__ == "__main__":
    main()
