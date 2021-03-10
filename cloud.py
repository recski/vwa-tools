import sys
from collections import defaultdict

import numpy as np
from wordcloud import WordCloud
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
from tuw_nlp.common.vocabulary import Vocabulary


PLZ = [
    "1020", "1030", "1040", "1050", "1060", "1070", "1080", "1090", "1100",
    "1110", "1120", "1130", "1140", "1150", "1160", "1170", "1180", "1190",
    "1200", "1210", "1220", "1230"]


SW = set(stopwords.words('german'))

SW |= {
    "vgl", "welch"
}


def keep(word):
    if word.lower() in SW:
        return False
    return True


def main():
    print('reading vocabulary...')
    count_by_plz = {plz: defaultdict(int) for plz in PLZ}
    vocab = Vocabulary()
    for line in sys.stdin:
        fields = line.strip().split('\t')
        if len(fields) != 3:
            print('skipping line:', line)
            continue
        word, _ = fields[0], int(fields[1])
        if keep(word):
            vocab.add(word)
            for field in fields[2].split(','):
                plz, freq = field.split(':')
                if plz in PLZ:
                    count_by_plz[plz][word] = int(freq)

    print('building array...')
    counts = np.array([
        [count_by_plz[plz][vocab.get_word(i)] for plz in PLZ]
        for i in range(len(vocab))])
    counts = counts.transpose()
    print('done, shape:', counts.shape)

    print('calculating TFIDF...')
    tfidf = TfidfTransformer().fit_transform(counts)
    print('done, type and shape:', type(tfidf), tfidf.shape)

    cx = tfidf.tocoo()
    tfidf_by_plz = {plz: defaultdict(int) for plz in PLZ}
    for i, j, v in zip(cx.row, cx.col, cx.data):
        print(i, j, v)
        tfidf_by_plz[PLZ[i]][vocab.get_word(j)] = v

    print(tfidf_by_plz['1020'])

    print('generating wordclouds...')
    for plz in PLZ:
        wc = WordCloud()
        wc.generate_from_frequencies(tfidf_by_plz[plz])
        wc.to_file(f"wordclouds/{plz}.png")


if __name__ == "__main__":
    main()
