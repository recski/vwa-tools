# vwa-tools

## Requirements
Install required python packages:

```
pip install -r requirements.txt
```



## Preprocessing

Original CSV data can be split into chunks of 1000 essays each using this command:

```
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
