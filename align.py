# Author: Antoine Cadotte (2023)
# https://github.com/cadotte

import os
import sys
import regex as re
import nltk
from nltk.translate import gale_church as gc

def calculate_lengths(paragraph_list):
    lengths = []
    for sen_list in paragraph_list:
        sen_lengths = []
        for sen in sen_list:
            sen_lengths.append(len(sen))
        lengths.append(sen_lengths)

    return lengths

# Generate aligned sentences from alignment and src, tgt sentence lists
def generate_paragraph(src_par_sen_list, tgt_par_sen_list, par_alignment):

    # initialize aligned sentence lists
    aligned_src_sen_list = []
    aligned_tgt_sen_list = []

    # create buffers
    src_buffer = ''
    tgt_buffer = ''

    # initialize operation state
    merge_state = 'no_merge'

    for alignment_index, alignment_pair in  enumerate(par_alignment):
        # get sentence indexes
        src_sen_index = alignment_pair[0]
        tgt_sen_index = alignment_pair[1]

        if (alignment_index > 0):

            # get previous sentence indexes
            previous_src_sen_index = par_alignment[alignment_index-1][0]
            previous_tgt_sen_index = par_alignment[alignment_index-1][1]

            # calculate deltas
            src_index_delta = previous_src_sen_index - src_sen_index
            tgt_index_delta = previous_tgt_sen_index - tgt_sen_index

            # identify operation type
            if (src_index_delta == 0): # tgt merge
                merge_state = 'tgt_merge'

            elif (tgt_index_delta == 0): # src merge
                merge_state = 'src_merge'

            else:
                merge_state = 'no_merge'

            # print("merge state: " + merge_state)

            # decide what to do with buffer based on merge_state
            if merge_state == 'end_merge':

                # append aligned sentence list with sentence in buffer
                aligned_src_sen_list.append(src_buffer)
                aligned_tgt_sen_list.append(tgt_buffer)

                # reinitialize buffer with current sentences
                src_buffer = src_par_sen_list[src_sen_index]
                tgt_buffer = tgt_par_sen_list[tgt_sen_index]

            elif merge_state == 'src_merge':

                # concatenate previous src sentence to sentence in buffer
                src_buffer += ' ' + src_par_sen_list[src_sen_index]

            elif merge_state == 'tgt_merge':

                # concatenate previous tgt sentence to sentence in buffer
                tgt_buffer += ' ' + tgt_par_sen_list[tgt_sen_index]

            else:  # no merge

                # append aligned sentence list with sentence in buffer
                aligned_src_sen_list.append(src_buffer)
                aligned_tgt_sen_list.append(tgt_buffer)

                # reinitialize buffer with current sentences
                src_buffer = src_par_sen_list[src_sen_index]
                tgt_buffer = tgt_par_sen_list[tgt_sen_index]

        else:
            # initialize buffer with current sentences
            src_buffer = src_par_sen_list[src_sen_index]
            tgt_buffer = tgt_par_sen_list[tgt_sen_index]

    # end of alignment list reached: append aligned sentence list with sentence in buffer
    aligned_src_sen_list.append(src_buffer)
    aligned_tgt_sen_list.append(tgt_buffer)

    return aligned_src_sen_list, aligned_tgt_sen_list

def count_tp_fp_fn(hypothesis_list, reference_list):

    # Count number of True Positives («right»)
    tp = 0
    for pair in reference_list:
        if pair in hypothesis_list:
            tp+=1

    # Count number of False Positives («wrong»)
    fp = 0
    for pair in hypothesis_list:
        if pair not in reference_list:
            fp+=1

    # Count number of False Negatives («omitted»)
    fn = 0
    for pair in reference_list:
        if pair not in hypothesis_list:
            fn += 1

    return tp, fp, fn

def calculate_prec_rec_f1(tp, fp, fn):

    # Calculate Precision, Recall and F1
    if tp!=0:
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1_score = 2 * (precision * recall) / (precision + recall)
    else:
        precision = 0
        recall = 0
        f1_score = 0
    print("Precision: " + str(precision))
    print("Recall: " + str(recall))
    print("F1 Score: " + str(f1_score))

    return precision, recall, f1_score

def get_combined_sentences(src_par, tgt_par):

    combined_sentences = []

    # split both paragraphs into a sentence list
    try:
        src_sentences = src_par.split("\n")
        tgt_sentences = tgt_par.split("\n")
    except:
        print("Erreur de split pour le paragraphe suivant:")
        print(src_par)
        print(tgt_par)

    if len(src_sentences)!=len(tgt_sentences):
        print("Following par does not have the same number of sentences ("
              + str(len(src_sentences)) + " vs. " + str(len(tgt_sentences)) + ")")
        print(src_par)
        print(tgt_par)
    
    # concatenate sentences from both languages
    for index, src_sen in enumerate(src_sentences):
        combined_sen = src_sen.strip() + " " + tgt_sentences[index].strip()
        combined_sentences.append(combined_sen)
    
    return combined_sentences

def evaluate(src_ref_path, tgt_ref_path, src_hyp_path, tgt_hyp_path):

    src_ref_par_list=[]
    fr = open(src_ref_path, "r")
    src_ref_par_list = [fr.read().split("\n\n")]
    fr.close()
    
    tgt_ref_par_list=[]
    fr = open(tgt_ref_path, "r")
    tgt_ref_par_list = [fr.read().split("\n\n")]
    fr.close()
    
    src_hyp_par_list=[]
    fr = open(src_hyp_path, "r")
    src_hyp_par_list = [fr.read().split("\n\n")]
    fr.close()
    
    tgt_hyp_par_list=[]
    fr = open(tgt_hyp_path, "r")
    tgt_hyp_par_list = [fr.read().split("\n\n")]
    fr.close()
        
    # Get TPs, FPs and FNs for all paragraphs
    global_tp = 0
    global_fp = 0
    global_fn = 0

    # for each par
    for index, hyp_src_par in enumerate(src_hyp_par_list):

        hyp_tgt_par = tgt_hyp_par_list[index]
        ref_src_par = src_ref_par_list[index]
        ref_tgt_par = tgt_ref_par_list[index]

        hyp_combined_sentences = get_combined_sentences(hyp_src_par, hyp_tgt_par)
        ref_combined_sentences = get_combined_sentences(ref_src_par, ref_tgt_par)

        # Get TPs, FPs and FNs for paragraph
        par_tp, par_fp, par_fn = count_tp_fp_fn(hyp_combined_sentences, ref_combined_sentences)
        print("Paragraph index:")
        print(index)
        print("Counts:")
        print(par_tp)
        print(par_fp)
        print(par_fn)
        global_tp+=par_tp
        global_fp+=par_fp
        global_fn+=par_fn

    # Calculate Precision, Recall and F1-Score
    print(global_tp)
    print(global_fp)
    print(global_fn)
    calculate_prec_rec_f1(global_tp, global_fp, global_fn)

def align_with_method(src_path, tgt_path, method):

    if method == "gc":

        # get src and tgt sentences
        fr = open(src_path, "r")
        src_paragraph_sen_list = [fr.read().split("\n")]
        fr.close()
        fr = open(tgt_path, "r")
        tgt_paragraph_sen_list = [fr.read().split("\n")]
        fr.close()

        # calculate lengths
        src_lengths = calculate_lengths(src_paragraph_sen_list)
        tgt_lengths = calculate_lengths(tgt_paragraph_sen_list)

        # call GC aligner
        try:
            par_alignment = gc.align_texts(source_blocks=src_lengths, target_blocks=tgt_lengths)
        except:
            print("GC alignment error for following file: " + filename)
            continue

        # generate src and tgt paragraphs from alignment
        print(filename)
        print(src_paragraph_sen_list[0])
        print(tgt_paragraph_sen_list[0])
        print(par_alignment[0])

        aligned_src_sentences, aligned_tgt_sentences = generate_paragraph(src_paragraph_sen_list[0], tgt_paragraph_sen_list[0], par_alignment[0])
        print(aligned_src_sentences)
        print(aligned_tgt_sentences)

        # write aligned sentences to files
        aligned_src_path = src_path + ".aligned.gc"
        aligned_src_paragraph = '\n'.join(aligned_src_sentences)
        fw = open(aligned_src_path, "w")
        fw.write(aligned_src_paragraph)
        fw.close()
        aligned_tgt_path = tgt_path + ".aligned.gc"
        aligned_tgt_paragraph = '\n'.join(aligned_tgt_sentences)
        fw = open(aligned_tgt_path, "w")
        fw.write(aligned_tgt_paragraph)
        fw.close()

    else:
        print("Alignment method not supported")
    return

if __name__ == "__main__":

    if (len(sys.argv) >= 2):
        if (sys.argv[1] == "align"):
            align_with_method(sys.argv[2], sys.argv[3])
        elif (sys.argv[1] == "evaluate"):
                evaluate(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        else:
            print("Unsupported functionality")

    else:
        raise ValueError("Wrong number of arguments")



