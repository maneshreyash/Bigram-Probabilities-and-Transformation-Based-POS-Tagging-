from __future__ import division
from collections import OrderedDict

# Function to scan the file
# @param:   path -          specifies the path of the input file
# @return:  file_content -  scans and returns the contents of the file
def read_file(path):
    file_content = open(path, "r")
    # print(f.read())
    file_content = file_content.read()
    return file_content


def split_processing(sentences):
    sentences = sentences.split(" . ")
    for i in range(0, len(sentences)):
        sentences[i] = sentences[i].split()
    # print(sentences)
    return sentences


def bigram_compute(tokens):

    word_count = {}
    total_words = 0
    bigrams = {}
    total_bigrams = 0

    for j in range(0, len(tokens)):
        for i in range(0, len(tokens[j])):
            total_words += 1
            if tokens[j][i] in word_count:
                word_count[tokens[j][i]] = word_count[tokens[j][i]] + 1
            else:
                word_count[tokens[j][i]] = 1
            if i < len(tokens[j]) - 1:
                total_bigrams += 1
                if (tokens[j][i], tokens[j][i+1]) in bigrams:
                    bigrams[(tokens[j][i], tokens[j][i+1])] += 1
                else:
                    bigrams[(tokens[j][i], tokens[j][i + 1])] = 1

    bigrams_prob = {}
    bigrams_addone = {}
    bigrams_addone_count = {}
    for bigram in bigrams:
        bigrams_prob[bigram] = (bigrams.get(bigram)) / (word_count.get(bigram[0]))
        bigrams_addone_count[bigram] = ((bigrams.get(bigram) + 1) * total_bigrams) / (total_bigrams + len(bigrams))
        bigrams_addone[bigram] = (bigrams.get(bigram) + 1) / (word_count.get(bigram[0]) + len(bigrams))
    # print (total_bigrams)
    # print (len(bigrams))
    buckets = {}
    for bigram in bigrams:
        if bigrams.get(bigram) in buckets:
            buckets[bigrams.get(bigram)] += 1
        else:
            buckets[bigrams.get(bigram)] = 1
    od = OrderedDict(sorted(buckets.items()))
    ol = sorted(buckets.items(), key=lambda t: t[0])
    c_star = {}
    for i in range(0, len(ol) - 1):
        c_star[ol[i][0]] = (ol[i+1][0]) * (od.get((ol[i+1][0]))) / (od.get((ol[i][0])))
    c_star[ol[len(ol)-1][0]] = ol[len(ol)-1][1]
    gt_prob = {}
    for bigram in bigrams:
        # print (bigrams.get(bigram))
        gt_prob[bigram] = c_star.get(bigrams.get(bigram)) / total_bigrams
    # print (bigrams)
    print (total_bigrams)
    print (c_star)
    print (gt_prob)


if __name__ == "__main__":
    filepath = 'HW2_F18_NLP6320-NLPCorpusTreebank2Parts-CorpusA-Windows.txt'
    f = read_file(filepath)
    tokens = split_processing(f)
    # print(tokens)
    bigram_compute(tokens)
