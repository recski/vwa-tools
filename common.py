from nltk.corpus import stopwords

EXTRA_STOPWORDS = {
    'the',
    "vgl", "welch", "geben", "kommen", "arbeit", "mehr", "groß",
    "mensch", 'frau', 'kapitel', 'verlag', 'kind', 'jahr', 'zeit', "seite",
    'ebd', 'februar', 'gymnasium', 'entwicklung', 'auswirkungen', 'vergleich',
    "beispiel", 'ursachen', 'einfluss', 'auswirkung', 'ursache', 'jahrhundert',
    'leben', 'bedeutung', 'darstellung', 'entstehung', 'auswirkung',
    'berücksichtigung', 'veränderung', 'folge', 'analyse', 'anwendung',
    'verwendung', 'unterschied', 'aspekt', 'bezug', 'wirkung', 'rolle',
}

STOPWORDS = set(stopwords.words('german'))

# STOPWORDS |= EXTRA_STOPWORDS
