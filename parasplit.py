import sys
import re as re
import math

# Divide full parallel sentence sets into training, validation and test sets

def split(corpus_path, src, tgt, valid_test_proportion):
    
    print("Corpus: " + corpus_path)
    print("Source: " + src)
    print("Target: " + tgt)
    print("Valid & test proportion: " + str(valid_test_proportion))

    # Open + read full sets
    all_src = open(corpus_path + 'all.' + src + '-' + tgt + '.' + src, 'r')
    all_src_lines = all_src.readlines()

    all_tgt = open(corpus_path + 'all.' + src + '-' + tgt + '.' + tgt, 'r')
    all_tgt_lines = all_tgt.readlines()

    # set delimiters
    nb_test_valid = math.floor(len(all_src_lines)*float(valid_test_proportion)/2)
    delimit_train_valid = len(all_src_lines) - 2*nb_test_valid
    delimit_valid_test = len(all_src_lines) - nb_test_valid


    # Extract, open & write Train sets
    train_src_lines = all_src_lines[0:delimit_train_valid]
    train_src = open(corpus_path + 'train.'+ src + '-' + tgt + '.' + src, 'w')
    for line in train_src_lines:
        train_src.write(line)
    train_tgt_lines = all_tgt_lines[0:delimit_train_valid]
    train_tgt = open(corpus_path + 'train.'+ src + '-' + tgt + '.' + tgt, 'w')
    for line in train_tgt_lines:
        train_tgt.write(line)

    # Extract, open & write Valid sets
    valid_src_lines = all_src_lines[delimit_train_valid:delimit_valid_test]
    valid_src = open(corpus_path + 'valid.'+ src + '-' + tgt + '.' + src, 'w')
    for line in valid_src_lines:
        valid_src.write(line)
    valid_tgt_lines = all_tgt_lines[delimit_train_valid:delimit_valid_test]
    valid_tgt = open(corpus_path + 'valid.'+ src + '-' + tgt + '.' + tgt, 'w')
    for line in valid_tgt_lines:
        valid_tgt.write(line)

    # Extract, open & write Test sets
    test_src_lines = all_src_lines[delimit_valid_test:]
    test_src = open(corpus_path + 'test.'+ src + '-' + tgt + '.' + src, 'w')
    for line in test_src_lines:
        test_src.write(line)
    test_tgt_lines = all_tgt_lines[delimit_valid_test:]
    test_tgt = open(corpus_path + 'test.'+ src + '-' + tgt + '.' + tgt, 'w')
    for line in test_tgt_lines:
        test_tgt.write(line)

def classic_split(corpus_path, src, tgt):
    print("Corpus: " + corpus_path)
    print("Source: " + src)
    print("Target: " + tgt)
    print("Classic split: keeping 20% for test, then 20% for validation")

    # Open + read full sets
    all_src = open(corpus_path + 'all.' + src + '-' + tgt + '.' + src, 'r')
    all_src_lines = all_src.readlines()

    all_tgt = open(corpus_path + 'all.' + src + '-' + tgt + '.' + tgt, 'r')
    all_tgt_lines = all_tgt.readlines()

    # set delimiters
    nb_test = math.floor(len(all_src_lines) * 0.2)
    nb_train_valid = len(all_src_lines) - nb_test
    nb_train = math.floor(nb_train_valid * 0.8)

    # Extract, open & write Train sets
    train_src_lines = all_src_lines[0:nb_train]
    train_src = open(corpus_path + 'train.' + src + '-' + tgt + '.' + src, 'w')
    for line in train_src_lines:
        train_src.write(line)
    train_tgt_lines = all_tgt_lines[0:nb_train]
    train_tgt = open(corpus_path + 'train.' + src + '-' + tgt + '.' + tgt, 'w')
    for line in train_tgt_lines:
        train_tgt.write(line)

    # Extract, open & write Valid sets
    valid_src_lines = all_src_lines[nb_train:nb_train_valid]
    valid_src = open(corpus_path + 'valid.' + src + '-' + tgt + '.' + src, 'w')
    for line in valid_src_lines:
        valid_src.write(line)
    valid_tgt_lines = all_tgt_lines[nb_train:nb_train_valid]
    valid_tgt = open(corpus_path + 'valid.' + src + '-' + tgt + '.' + tgt, 'w')
    for line in valid_tgt_lines:
        valid_tgt.write(line)

    # Extract, open & write Test sets
    test_src_lines = all_src_lines[nb_train_valid:]
    test_src = open(corpus_path + 'test.' + src + '-' + tgt + '.' + src, 'w')
    for line in test_src_lines:
        test_src.write(line)
    test_tgt_lines = all_tgt_lines[nb_train_valid:]
    test_tgt = open(corpus_path + 'test.' + src + '-' + tgt + '.' + tgt, 'w')
    for line in test_tgt_lines:
        test_tgt.write(line)

if __name__ == "__main__":

    if (len(sys.argv) == 5):
        if sys.argv[4] == "classic":
            classic_split(sys.argv[1], sys.argv[2], sys.argv[3])
        else:
            split(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    elif (len(sys.argv) == 4):
        print("Using default split value (0.15)")
        default_split = 0.15
        split(sys.argv[1], sys.argv[2], sys.argv[3], default_split)

    else:
        raise ValueError("Wrong number of arguments")
