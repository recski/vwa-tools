
import csv
import sys

from tqdm import tqdm

csv.field_size_limit(sys.maxsize)

fn = sys.argv[1]
n = int(sys.argv[2])
prefix = sys.argv[3]

out_file = None

with open(fn) as f:
    for i, row in tqdm(enumerate(csv.reader(f, delimiter=",", quotechar='"'))):
        if i == 0:
            header = row
            continue

        if i % n == 1:
            if out_file:
                out_file.close()
            batch_no = int(i / n)
            out_fn = f"{prefix}_{batch_no}.csv"
            out_file = open(out_fn, 'w')
            writer = csv.writer(
                out_file, delimiter=',', quotechar='"',
                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(header)

        writer.writerow(row)
