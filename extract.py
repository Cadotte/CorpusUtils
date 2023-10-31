# Author: Antoine Cadotte
# https://github.com/cadotte
# Based on code from pdfplumber: https://github.com/jsvine/pdfplumber

import pdfplumber
import os

# Extract text from provided PDF file and write it to text file with same name & location
def extract(filepath):
    with pdfplumber.open(filepath) as pdf:
        with open(filepath.replace('pdf', 'txt'), 'w') as f:
            print("Reading file " + filename)
            for page in pdf.pages:
                f.write(page.extract_text(x_tolerance=3, y_tolerance=3))
                f.write("\n\n")
            
if __name__ == "__main__":

if (len(sys.argv) == 2):
    extract(sys.argv[1])

else:
    print("Missing PDF filepath")
