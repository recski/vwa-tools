"""filter words from a vocabulary and from a BOW matrix"""
import argparse

import numpy as np
from scipy.sparse import load_npz, save_npz
from tuw_nlp.common.vocabulary import Vocabulary

from common import STOPWORDS as SW


def filter_vocab(vocab, A):
    print(f'filtering matrix of shape {A.shape}...')
    rel_doc_counts = np.squeeze(np.asarray(
        A.astype(bool).sum(axis=0) / A.shape[0]))

    new_vocab = Vocabulary()
    id_map = {}
    for i, word in vocab.id_to_word.items():
        if rel_doc_counts[i] >= 0.9:
            continue
        if word.lower() in SW:
            continue

        new_vocab.add(word)
        id_map[i] = new_vocab.get_id(word)

    B = A[:, tuple(id_map.keys())]
    print('new matrix shape:', B.shape)
    return new_vocab, B


def get_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-c", "--corpus-file", default=None, type=str)
    parser.add_argument("-d", "--new-corpus", default=None, type=str)
    parser.add_argument("-v", "--vocab-file", default=None, type=str)
    parser.add_argument("-w", "--new-vocab", default=None, type=str)
    return parser.parse_args()


def main():
    args = get_args()

    print('loading...')
    vocab = Vocabulary.from_file(args.vocab_file)
    bow_matrix = load_npz(args.corpus_file)

    print('filtering...')
    new_vocab, new_matrix = filter_vocab(vocab, bow_matrix)

    print('saving...')
    new_vocab.to_file(args.new_vocab)
    save_npz(args.new_corpus, new_matrix)


if __name__ == "__main__":
    main()
