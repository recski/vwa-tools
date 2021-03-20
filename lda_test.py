import argparse
import joblib

import matplotlib.pyplot as plt
# from gensim.matutils import Sparse2Corpus
# from gensim.models import LdaMulticore
# from scipy.sparse import load_npz
# from sklearn.decomposition import LatentDirichletAllocation
from tuw_nlp.common.vocabulary import Vocabulary


def plot_top_words(model, feature_names, n_top_words, title, fn):
    """https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html#sphx-glr-auto-examples-applications-plot-topics-extraction-with-nmf-lda-py"""  # noqa
    fig, axes = plt.subplots(2, 5, figsize=(30, 15), sharex=True)
    axes = axes.flatten()
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[:-n_top_words - 1:-1]
        top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind]

        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7)
        ax.set_title(f'Topic {topic_idx +1}',
                     fontdict={'fontsize': 30})
        ax.invert_yaxis()
        ax.tick_params(axis='both', which='major', labelsize=20)
        for i in 'top right left'.split():
            ax.spines[i].set_visible(False)
        fig.suptitle(title, fontsize=40)

    plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)

    plt.savefig(fn)
    # plt.show()


def get_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-m", "--model-file", type=str)
    # parser.add_argument("-c", "--corpus-file", default=None, type=str)
    parser.add_argument("-v", "--vocab-file", default=None, type=str)
    parser.add_argument("-n", "--n-topics", default=None, type=int)
    # parser.add_argument("-w", "--n-workers", default=None, type=int)
    return parser.parse_args()


def main():
    args = get_args()
    vocab = Vocabulary.from_file(args.vocab_file)

    print('loading LDA model...')

    model = joblib.load(args.model_file)

    print('plotting topics...')
    plot_top_words(
        model, vocab.id_to_word, 10, "Topics in LDA model", "topics.png")


if __name__ == "__main__":
    main()
