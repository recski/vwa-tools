import json
import sys
from collections import Counter

from scipy.sparse import csc_matrix, save_npz
from tuw_nlp.common.vocabulary import Vocabulary


def main():
    vocab = Vocabulary.from_file(sys.argv[1])
    data, row_ind, col_ind = [], [], []
    n_docs = 0
    for line in sys.stdin:
        d = json.loads(line)
        if d['lang'] != 'de':
            continue
        n_docs += 1
        counter = Counter()
        for tok in d['text']['tokens']:
            w = tok['lemma']
            if w in vocab:
                counter[w] += 1

        for word, freq in counter.items():
            data.append(freq)
            row_ind.append(n_docs-1)
            col_ind.append(vocab.get_id(word))

    print('generating csr matrix...')
    print('shape:', (n_docs, len(vocab)))
    M = csc_matrix((data, (row_ind, col_ind)), (n_docs, len(vocab)))
    print('saving...')
    save_npz(sys.argv[2], M)


if __name__ == "__main__":
    main()
