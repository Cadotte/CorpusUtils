# Author: Antoine Cadotte
# https://github.com/cadotte

import os
import sys
import re as re
import nltk
import pandas as pd

# Proceed to general formatting/cleaning operations on provided text file
def general_formatting(text):

    # Stitch words split in two by hyphen
    text = re.sub(r'(?<=\b)((-)(\n)+)(?=\b)', "", text)

    # Remove bullet characters
    text = re.sub(r'(\uf0b7)(\s)+', "", text)
    text = re.sub(r'(\u00b7)(\s)+', "", text)
    text = re.sub(r'(\uf0fc)(\s)+', "", text)

    # Replace all multiple newlines with single ones
    text = re.sub(r'((\s)*(\n)){3,}', " \n\n", text)

    # Remove leading and trailing newlines & spaces
    text = text.strip()

    # Replace all multiple spaces with single ones
    text = re.sub(r'[ ]{2,}', " ", text)

    # Replace non-standard characters with standard ones
    text = re.sub("´", "'", text)
    text = re.sub("’", "'", text)
    text = re.sub("…", "...", text)
    text = re.sub("ﬁ", "fi", text)
    text = re.sub("œ", "oe", text)

    return text

# Proceed to novel-specific formatting/cleaning operations on provided text file
def novel_formatting(text):

    # Stitch paragraphs
    text = re.sub(r'(?<=[^\s])\n(?=[A-Z])', "\n\n", text)

    # Stitch sentences
    text = re.sub(r'(?<=.)\n(?=.)', "", text)

    # Remove page numbers
    text = re.sub(r'(\n+)(\d+)(\n+)', "\n", text)

    return text

def format_file(filepath, type):
    with open(filepath, 'r') as fr:
        text = fr.read()

        if type == "novel":
            text = novel_formatting(text)
            text = general_formatting(text)

        else:
            text = general_formatting(text)

        # Write formatted text to file
        with open("../data/txt/" + "Formatted_" + filename, 'w') as fw:
            fw.write(text)
    return

if __name__ == "__main__":

    if (len(sys.argv) == 2):
        format_file(sys.argv[1], "general")
    elif (len(sys.argv) > 2):
        format_file(sys.argv[1], sys.argv[2])
    else:
        print("Missing text file path")