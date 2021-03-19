import argparse
import joblib

# from gensim.matutils import Sparse2Corpus
# from gensim.models import LdaMulticore
from scipy.sparse import load_npz
from sklearn.decomposition import LatentDirichletAllocation
# from tuw_nlp.common.vocabulary import Vocabulary


def get_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-m", "--model-file", type=str)
    parser.add_argument(
        "-p", "--print-errs", default=False, action='store_true')
    parser.add_argument("-c", "--corpus-file", default=None, type=str)
    # parser.add_argument("-v", "--vocab-file", default=None, type=str)
    parser.add_argument("-n", "--n-topics", default=None, type=int)
    parser.add_argument("-w", "--n-workers", default=None, type=int)
    return parser.parse_args()


def main():
    args = get_args()
    # vocab = Vocabulary.from_file(args.vocab_file)
    print('loading corpus...')
    bow_matrix = load_npz(args.corpus_file)
    # corpus = Sparse2Corpus(bow_matrix)
    print('training LDA model...')
    # lda = LdaMulticore(
    #    corpus, id2word=vocab.id_to_word, num_topics=args.n_topics,
    #    workers=args.n_workers)

    lda = LatentDirichletAllocation(
        n_components=args.n_topics, n_jobs=args.n_workers, random_state=0)
    lda.fit(bow_matrix)

    print('saving model...')
    joblib.dump(lda, args.model_file)
    # lda.save(args.model_file)


if __name__ == "__main__":
    main()
