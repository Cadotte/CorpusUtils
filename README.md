# CorpusUtils

Set of utilities scripts for corpus preprocessing. Although they are mostly aimed at Machine Translation, many of the functions can be useful for any type of corpus.


Divided into several python scripts, these utilities cover the following basic preprocessing steps: extraction, formatting, sentence alignment. The following presents each script, with their functions and use cases.

### align.py
Used for the alignment of bilingual corpora. Aligns sentences from source and target languages, by specifying alignment method (Gale & Church is the only supported method for now). Also allows to evaluate generated (hypothesized) aligned sentences compared to reference src and tgt sentences.

```
# Align src and target sentences
python align.py align path/to/src/sentences.txt path/to/tgt/sentences.txt gc

# Evaluate hypothesized aligned sentences compared to reference sentences
python align.py evaluate path/to/ref/src/sentences.txt path/to/ref/tgt/sentences.txt path/to/hyp/src/sentences.txt path/to/hyp/tgt/sentences.txt
```

### extract.py
Extracts raw text from a PDF file. This script requires/uses the very convenient pdfplumber library (https://github.com/jsvine/pdfplumber). Make sure to adapt dimensions/tolerances so they fit your document.
```
python extract.py path/to/your/file.pdf
```

### format.py
Formats (or cleans) the raw text extracted from a document. Formatting operations include deleting multiple newlines or spaces, standardizing non-standard characters, stitching sentences or paragraphs, etc. 
```
# General document
python format.py path/to/your/text.txt

# Novel type document
python format.py path/to/your/text.txt novel
```

### split.py
Splits a full parallel set into training, validation and testings sets. There are two modes: classic (80-20-20 split) and a personalized "half & half", where the proportion of sentence kept for the test & valid sets needs to be specified. The proportion of test and valid will be equal (specified proportion is divided in 2). For example, specifying 0.20 will result in 80% of sentences in train, 10% in valid and 10% in test.
Path to corpus directory needs to be specified, as well as src and tgt languages.
Complete parallel sentence sets needs to be named as follows: 'all.src-tgt.src' and 'all.src-tgt.tgt'. Resulting train, valid and test sets will named as follows: 'train.src-tgt.src', 'train.src-tgt.tgt', 'valid.src-tgt.tgt', etc.
Sentence order is not randomized before split.
```
# Classic split (80-20-20)
python parasplit.py classic path/to/your/corpus/directory/ src tgt

# Personalized half & half split (default is 0.15)
python parasplit.py path/to/your/corpus/directory/ src tgt 0.20

```
