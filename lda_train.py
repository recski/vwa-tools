import argparse
import joblib

# from gensim.matutils import Sparse2Corpus
# from gensim.models import LdaMulticore
from scipy.sparse import load_npz
from sklearn.decomposition import LatentDirichletAllocation
from tuw_nlp.common.vocabulary import Vocabulary

from filter_vocab import filter_vocab


def get_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-m", "--model-file", type=str)
    parser.add_argument("-c", "--corpus-file", default=None, type=str)
    parser.add_argument("-n", "--n-topics", default=None, type=int)
    parser.add_argument("-j", "--n-workers", default=None, type=int)
    parser.add_argument("-v", "--vocab-file", default=None, type=str)
    parser.add_argument("-w", "--new-vocab", default=None, type=str)
    return parser.parse_args()


def main():
    args = get_args()
    print('loading vocabulary...')
    vocab = Vocabulary.from_file(args.vocab_file)
    print('loading corpus...')
    bow_matrix = load_npz(args.corpus_file)

    print('filtering...')
    new_vocab, new_matrix = filter_vocab(vocab, bow_matrix)
    print('saving filtered vocabulary...')
    new_vocab.to_file(args.new_vocab)

    print('training LDA model...')
    lda = LatentDirichletAllocation(
        n_components=args.n_topics, n_jobs=args.n_workers, random_state=0)
    lda.fit(new_matrix)

    print('saving model...')
    joblib.dump(lda, args.model_file)
    # lda.save(args.model_file)


if __name__ == "__main__":
    main()
