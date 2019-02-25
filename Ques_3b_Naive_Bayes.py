# IMPLEMENT BIGRAM MODELS TO FEED IN THE REQUIRED VALUES FOR THE FORMULAE OF NAIVE BAYESIAN CLASSIFICATION
# TO COMPUTE THE PROBABILITY OF THE GIVEN SENTENCE: The_DT standard_?? Turbo_NN engine_NN is_VBZ hard_JJ to_TO work_??
#
# @author: Shreyash Sanjay Mane


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
def preprocess(contents):
    pairs = contents.split()
    for i in range(0, len(pairs)):
        pairs[i] = pairs[i].split('_')
    return pairs


# Calculation of bi_grams
# @param:   tags -          correct tagged corpus
# @return:  wi_given_ti -   the biGram probabilities of a word given its tag
#           tags_bi_gram_probability- the probability of a tag for a word given its previous tag and
#                                     its corresponding previous word
def bi_gram_calculation(tags):

    # Computation of uniGram tags
    uni_gram_tags = {}
    for tag in tags:

        if tag[1] in uni_gram_tags:
            uni_gram_tags[tag[1]] += 1

        else:
            uni_gram_tags[tag[1]] = 1

    # Computation of uniGram of tokens that is words
    uni_gram_tokens = {}

    for token in tags:
        pair = (token[0], token[1])
        if pair not in uni_gram_tokens:
            uni_gram_tokens[pair] = 1
        else:
            uni_gram_tokens[pair] += 1

    # Computation of probabilities of word i given its tag i that is P(w(i)|t(i))
    wi_give_ti = {}

    for uni_gram in uni_gram_tokens:
        wi_give_ti[uni_gram] = uni_gram_tokens.get(uni_gram) / uni_gram_tags.get(uni_gram[1])

    # Counting the biGrams for tags
    tags_bi_gram_count = {}

    for i in range(1, len(tags)):

        pair = (tags[i][1], tags[i-1][1])
        if pair in tags_bi_gram_count:
            tags_bi_gram_count[pair] += 1

        else:
            tags_bi_gram_count[pair] = 1

    # Counting biGram probabilities of tags
    tags_bi_gram_probability = {}

    for tag in tags_bi_gram_count:
        tags_bi_gram_probability[tag] = tags_bi_gram_count.get(tag) / uni_gram_tags.get(tag[1])

    return wi_give_ti, tags_bi_gram_probability


# Calculating the necessary probabilities required for hand computation of the missing tags
# @param:   in_sentence -       The sentence having missing tags which need to be determined.
#           wi_given_ti -       The probabilities of all words given their respective tags.
#           ti_given_t_i_minus1- The probabilities of tags given their previous tags.
# @return:  wi_ti -             Necessary probabilities of words given their respective tags for the input sentence.
#           ti_t_i_minus1 -     Necessary probabilities of tags for words given the tags for their previous words
#                               in the input sentence.
def missing_tags(in_sentence, wi_given_ti, ti_given_t_i_minus1):

    # Basic processing of the sentence to convert it to a data structure containing the words and its tags
    # as list of lists.
    data = in_sentence.split()
    for i in range(0, len(data)):
        data[i] = data[i].split('_')

    # Creating a ordered dictionary to help keep track of the computed probabilities for a word given its tag
    wi_ti = OrderedDict()

    for i in range(0, len(data)):
        new_map = {}

        # Computation for all valid occurrences of tags
        if data[i][1] != "??":
            new_map[data[i][1]] = wi_given_ti.get((data[i][0], data[i][1]))
            wi_ti[data[i][0]] = new_map

        # Computation of tags by taking into consideration all possible tags for a word
        # whose tag in the input sentence is missing
        else:
            for tag in wi_given_ti.keys():
                if tag[0] == data[i][0]:
                    new_map[tag[1]] = wi_given_ti.get((data[i][0], tag[1]))
            wi_ti[data[i][0]] = new_map

    # Creating a ordered dictionary to help keep track of the computed probabilities for the tag of a word given
    # the tag of its previous word
    ti_t_i_minus1 = OrderedDict()

    for i in range(1, len(data)):
        for tags in wi_ti.get(data[i][0]).keys():
            for tag in wi_ti.get(data[i-1][0]).keys():
                pair = (tags, tag)
                ti_t_i_minus1[pair] = ti_given_t_i_minus1.get(pair)

    return wi_ti, ti_t_i_minus1


if __name__ == "__main__":
    filepath = 'HW2_F18_NLP6320_POSTaggedTrainingSet-Windows.txt'
    f = read_file(filepath)
    correct_tags = preprocess(f)
    wi_given_ti, ti_given_t_i_minus1 = bi_gram_calculation(correct_tags)
    in_sen = "The_DT standard_?? Turbo_NN engine_NN is_VBZ hard_JJ to_TO work_??"
    wi_ti, ti_t_i_minus1 = missing_tags(in_sen, wi_given_ti, ti_given_t_i_minus1)
    print ()
    print ("The probability counts for w(i)|t(i) are: ")
    print (wi_ti)
    print ()
    print ()
    print ("The probability counts for t(i)|t(i-1) are: ")
    print (ti_t_i_minus1)
