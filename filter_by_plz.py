import csv
import json
import sys


def load_skz_to_plz(fn):
    skz_to_plz = {}
    with open(fn) as f:
        for row in csv.reader(f, delimiter=",", quotechar='"'):
            if not row[0]:
                continue
            _, skz, __, ___, plz = row
            skz_to_plz[skz] = plz

    return skz_to_plz


def filter_by_plz(stream, plz_to_keep, skz_to_plz):
    for line in stream:
        d = json.loads(line)
        skz = d['school_id']
        plz = skz_to_plz.get(skz)
        if plz == plz_to_keep:
            sys.stdout.write(line)


def filter_by_first_digit(stream, digit, skz_to_plz):
    plz_to_file_obj = {}
    for line in stream:
        d = json.loads(line)
        skz = d['school_id']
        plz = skz_to_plz.get(skz)
        if plz and plz[0] == digit:
            if plz not in plz_to_file_obj:
                plz_to_file_obj[plz] = open(f'data/vienna/{plz}.jsonl', 'w')
            fo = plz_to_file_obj[plz]
            fo.write(line)

    for fo in plz_to_file_obj.values():
        fo.close()


def main():
    skz_to_plz = load_skz_to_plz(sys.argv[2])
    # filter_by_plz(sys.stdin, sys.argv[1], skz_to_plz)
    filter_by_first_digit(sys.stdin, sys.argv[1], skz_to_plz)


if __name__ == "__main__":
    main()
