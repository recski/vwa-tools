import json
import sys

d = {}

for line in sys.stdin:
    fields = line.strip().split('\t')
    try:
        word, freq, plz_freqs = fields
    except ValueError:
        sys.stderr.write('skipping line: ' + line)
        continue
    d[word] = {
        plz: int(freq)
        for plz, freq in [s.split(':') for s in plz_freqs.split(',')]}

print(json.dumps(d))
