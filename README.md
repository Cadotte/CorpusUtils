# CorpusUtils

Set of utilities scripts for corpus preprocessing. Although they are mostly aimed at Machine Translation, many of the functions can be useful for any type of corpus.
They were developed in-house as tools used for my Masters Thesis on Machine Translation.


Divided into several python scripts, these utilities cover the following basic preprocessing steps: extraction, formatting, sentence alignment. The following presents each script, with their functions and use cases.

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
### align.py
Used for the alignment of bilingual corpora. Aligns sentences from source and target languages, by specifying alignment method (Gale & Church is the only supported method for now). Also allows to evaluate generated (hypothesized) aligned sentences compared to reference src and tgt sentences.

```
# Align src and target sentences
python align.py align path/to/src/sentences.txt path/to/tgt/sentences.txt gc

# Evaluate hypothesized aligned sentences compared to reference sentences
python align.py evaluate path/to/ref/src/sentences.txt path/to/ref/tgt/sentences.txt path/to/hyp/src/sentences.txt path/to/hyp/tgt/sentences.txt
```
