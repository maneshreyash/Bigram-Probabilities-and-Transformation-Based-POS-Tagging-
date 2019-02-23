from __future__ import division
from collections import OrderedDict


# Function to scan the file
# @param:   path -          specifies the path of the input file
# @return:  file_content -  scans and returns the contents of the file
def read_file(path):
    file_content = open(path, "r")
    file_content = file_content.read()
    return file_content


# Preprocess the scanned file contents
# @param:   contents -      scanned contents of the file
# @return:  pairs -         a list of list containing the word and it's corresponding tag
def split_processing(sentences):
    sentences = sentences.split(" . ")
    for i in range(0, len(sentences)):
        sentences[i] = sentences[i].split()
    return sentences


# BiGram Computations
# @param:   tokens -        each word separated as a component of a list which represents one sentence.
#                           A list of such sentence lists.
# TODO @return value specification as per hand computation requirements
def bi_gram_compute(token):

    # total counts of word occurrences.
    word_count = {}
    total_words = 0
    
    # biGram counts of actual biGram occurrences in the corpus.
    bi_grams = {}
    total_bi_grams = 0

    # Computing total word counts
    for j in range(0, len(token)):
        for i in range(0, len(token[j])):
            
            total_words += 1
            
            if token[j][i] in word_count:
                word_count[token[j][i]] = word_count[token[j][i]] + 1
            
            else:
                word_count[token[j][i]] = 1
            
            if i < len(token[j]) - 1:
                total_bi_grams += 1
            
                if (token[j][i], token[j][i+1]) in bi_grams:
                    bi_grams[(token[j][i], token[j][i+1])] += 1
            
                else:
                    bi_grams[(token[j][i], token[j][i + 1])] = 1
    
    # Dictionary to store the probability of computed biGrams.
    bi_grams_prob = {}

    # Dictionary to store add one smoothing probabilities
    bi_grams_add_one_prob = {}

    # Dictionary to store add one smoothing counts with respect to the biGrams
    bi_grams_add_one_count = {}

    for bi_gram in bi_grams:
        bi_grams_prob[bi_gram] = (bi_grams.get(bi_gram)) / (word_count.get(bi_gram[0]))
        bi_grams_add_one_count[bi_gram] = ((bi_grams.get(bi_gram) + 1) * total_bi_grams) / (total_bi_grams + len(bi_grams))
        bi_grams_add_one_prob[bi_gram] = (bi_grams.get(bi_gram) + 1) / (word_count.get(bi_gram[0]) + len(bi_grams))

    # Creating buckets for good turing smoothing
    buckets = {}

    for bi_gram in bi_grams:
        if bi_grams.get(bi_gram) in buckets:
            buckets[bi_grams.get(bi_gram)] += 1
        else:
            buckets[bi_grams.get(bi_gram)] = 1

    # Sort the buckets depending on the value of counts that is keys of the buckets
    od = OrderedDict(sorted(buckets.items()))
    ol = sorted(buckets.items(), key=lambda t: t[0])

    # Computation of c* values for all the buckets
    c_star = {}

    for i in range(0, len(ol) - 1):
        c_star[ol[i][0]] = (ol[i+1][0]) * (od.get((ol[i+1][0]))) / (od.get((ol[i][0])))
    c_star[ol[len(ol)-1][0]] = ol[len(ol)-1][1]

    # Computation of good turing probabilities
    gt_prob = {}

    for bi_gram in bi_grams:
        gt_prob[bi_gram] = c_star.get(bi_grams.get(bi_gram)) / total_bi_grams

    print (bi_grams)
    print (bi_grams_prob)

    print (bi_grams_add_one_count)
    print (bi_grams_add_one_prob)

    print (c_star)
    print (gt_prob)


if __name__ == "__main__":
    filepath = 'HW2_F18_NLP6320-NLPCorpusTreebank2Parts-CorpusA-Windows.txt'
    f = read_file(filepath)
    tokens = split_processing(f)
    bi_gram_compute(tokens)
