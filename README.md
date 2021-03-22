# vwa-tools

## Requirements
Install required python packages:

```
pip install -r requirements.txt
```

## Preprocessing

Original CSV data can be split into chunks of 1000 essays each using this command (assuming it is available in a directory called `data`):

```
mkdir data/essays
python split_csv.py data/essays.csv 1000 data/essays/essays
```

These were processed using the standard German NLP pipeline of spacy and saved
as json using multiple CPUs, 40 in this example
(output size will be around 184 GB):

```
nice parallel -j40 ./run.sh {} ::: {0..109}
```


## Word count

A simple word count based on lemmas detected by spacy can be performed by
running the following command, this also
maintains separate counts for each SKZ code.

```
nice python count_mr.py --runner=local data/essays/ana/*.jsonl >
data/essays_word_count_by_skz.tsv
```

This command will use all
available cores for a local map-reduce job (temporarily creating files for a hadoop
job, which includes duplicating the input data). Using different runners it can
also be run using e.g. Spark or Amazon EMR, see [this
document](https://mrjob.readthedocs.io/en/latest/guides/runners.html) for details.


## Word count by PLZ

This word count can be aggregated by PLZ-s like this:

```
cat data/essays_word_count_by_skz_sorted.tsv | python counts_to_plz.py data/skz_to_address_postcode.csv > data/essays_word_count_by_plz_sorted.tsv
```

This will also print to stderr the SKZ codes missing from the map:
```
unknown SKZs: 304056,1100006,205046,922706,1132235,1132236,1132211,1132210
```


## Languages

The `langdetect` package was used to determine the primary language of each
document. Remaining stats are calculated for German essays only.

Language distribution (based on ~10% of essays):

- de: 9628
- en: 363
- cs: 4
- sk: 2
- it: 1
- el: 1
- ca: 1


## Corpus stats on German essays:

- Corpus size: 655M tokens (of which standard punctuation: 79M, rest: 576M)
- Vocabulary: 8.7M
- Avg. tokens / document : 6703
- Avg. sentences / doc: 505


## Vocabulary

- raw: 8.7M
- letters-only strings only: 3.8M, coverage of all tokens (without standard
  punct): 85.9%
- **letters-only with at least 10 occurrences: 593K, coverage: 84.7%**



## Topic modeling

- creating bag-of-words matrix from preprocessed corpus:

```
pv data/essays/ana/essays_*.jsonl | python to_bow.py data/essays_vocab_min10.txt data/essays_bow_min10.npz
```

- training LDA model after simple vocabulary filtering (see `filter_vocab.py`):

```
python lda_train.py -c data/essays_bow_min10.npz -m models/essays_filtered_max100k_lda_10 -v data/essays_vocab_min10.txt -w data/essays_vocab_filtered_max100k.txt  -n 10 -j 40
```

This will also save the filtered vocabulary for subsequent analysis

- printing top words of each topic (to `topics.png`):

```
python lda_test.py -m models/essays_filtered_max100k_lda_10 -n 10 -v data/essays_vocab_filtered_max100k.txt
```

