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
def bi_gram_calculation(tags):
    uni_gram_tags = {}
    for tag in tags:
        if tag[1] in uni_gram_tags:
            uni_gram_tags[tag[1]] += 1
        else:
            uni_gram_tags[tag[1]] = 1
    uni_gram_tokens = {}
    for token in tags:
        pair = (token[0], token[1])
        if pair not in uni_gram_tokens:
            uni_gram_tokens[pair] = 1
        else:
            uni_gram_tokens[pair] += 1
    wi_given_ti = {}
    for uni_gram in uni_gram_tokens:
        wi_given_ti[uni_gram] = uni_gram_tokens.get(uni_gram) / uni_gram_tags.get(uni_gram[1])
    tags_bi_gram_count = {}
    for i in range(1, len(tags)):
        pair = (tags[i][1], tags[i-1][1])
        if pair in tags_bi_gram_count:
            tags_bi_gram_count[pair] += 1
        else:
            tags_bi_gram_count[pair] = 1
    tags_bi_gram_probability = {}
    for tag in tags_bi_gram_count:
        tags_bi_gram_probability[tag] = tags_bi_gram_count.get(tag) / uni_gram_tags.get(tag[1])
    return wi_given_ti, tags_bi_gram_probability


def missing_tags(in_sentence, wi_given_ti, ti_given_t_i_minus1):
    data = in_sentence.split()
    for i in range(0, len(data)):
        data[i] = data[i].split('_')
    # print (data)
    wi_ti = OrderedDict()
    for i in range(0, len(data)):
        new_map = {}
        if data[i][1] != "??":
            new_map[data[i][1]] = wi_given_ti.get((data[i][0], data[i][1]))
            wi_ti[data[i][0]] = new_map
        else:
            for tag in wi_given_ti.keys():
                if tag[0] == data[i][0]:
                    new_map[tag[1]] = wi_given_ti.get((data[i][0], tag[1]))
            wi_ti[data[i][0]] = new_map
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
