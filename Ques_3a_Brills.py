# IMPLEMENT BRILL'S TAGGING ALGORITHM TO FIND THE BEST POSSIBLE RULES FOR THE FOLLOWING CONVERSIONS:
# NN --> VB
# NN --> JJ
#
# @author: Shreyash Sanjay Mane


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


# Generate a corpus consisting of words only stripped of of all their tags
# @param:   tagged_tokens - The preprocessed data consisting of words and their tags
# @return:  data-           A corpus consisting of words only stripped of of all their tags
def corpus_generate(tagged_tokens):
    data = []
    for token in tagged_tokens:
        data.append(token[0])
    return data


# Generate a dictionary with all words as keys and their count occurrences as values
# @param:   tags -          The preprocessed data consisting of words and their tags
# @return:  data -          A dictionary with all words as keys and their count occurrences as values
def token_counter(tags):
    data = {}
    for token in tags:
        if token[0] not in data:
            data[token[0]] = 1
        else:
            data[token[0]] += 1
    return data


# Generate a dictionary with all words and the count of their corresponding tags
# as a map of tag as keys and counts as values.
# @param:   tags -          The preprocessed data consisting of words and their tags
# @return:  data -          A dictionary with all tags as keys and their count occurrences as values
def tag_counter(tags):
    data = {}
    for token in tags:
        if token[0] not in data:
            tag_map = {}
            tag_map[token[1]] = 1
            data[token[0]] = tag_map
        else:
            tag_map = data.get(token[0])
            if token[1] in tag_map:
                tag_map[token[1]] += 1
            else:
                tag_map[token[1]] = 1
            data[token[0]] = tag_map
    return data


# Re-tagging the stripped off corpus with most probable tags by choosing the tag for a word with the highest count.
# @param:   inp -           input corpus having just the words
#           tags -          a corpus having words and a map of all their tags and tag counts
# @return:  retags -        a corpus tagged with their most probable tags also called as current_tags corpus
def retag(inp, tags):
    retags = []

    for i in inp:
        tag_map = tags.get(i)
        max_tags = -1
        tag = ""

        for j in tag_map:
            if max_tags < tag_map.get(j):
                max_tags = tag_map.get(j)
                tag = j

        pair = [i, tag]
        retags.append(pair)

    return retags

# Create a set of all tags
# @param:   tags -          a corpus having words and a map of all their tags and tag counts
def tag_set(tags):
    tag = set()
    for i in tags:
        tag.add(i[1])
    return tag


def get_best_instance(correct_tags, current_tags):
    to_tags = {"JJ", "VB"}
    rules = []
    best_rule = []
    for to_tag in to_tags:
        num_good_transforms = {}
        for pos in range(1, len(current_tags)):
            if correct_tags[pos][1] == to_tag and current_tags[pos][1] == "NN":
                if current_tags[pos-1][1] in num_good_transforms:
                    num_good_transforms[current_tags[pos - 1][1]] += 1
                else:
                    num_good_transforms[current_tags[pos - 1][1]] = 1
            elif correct_tags[pos][1] == "NN" and current_tags[pos][1] == "NN":
                if current_tags[pos-1][1] in num_good_transforms:
                    num_good_transforms[current_tags[pos - 1][1]] -= 1
                else:
                    num_good_transforms[current_tags[pos - 1][1]] = -1
        # print(num_good_transforms)

        best_Z = max(num_good_transforms, key=num_good_transforms.get)
        new_rule = []
        new_rule.append('NN')
        new_rule.append(to_tag)
        new_rule.append(best_Z)
        best_rule.append(new_rule)
        # best_score = 0
        # if num_good_transforms.get(best_Z) > best_score:
        rule = []
        rule.append("NN")
        rule.append(to_tag)
        rule.append(best_Z)
        rule.append(num_good_transforms)
        rules.append(rule)
    return rules, best_rule


# Parse the input sentence to find the missing tag and replace it with the current tags initially
# and then see if they can be improved by applying the learned rules.
# @param:   input_sentence -    The input sentence with missing tags
#           rules -             The learnt rules from brill's algorithm
#           current -           the current corpus replaced with most probable tags
# @return:  data -              The tags that are supposed to be correct for the input sentence
def find_missing(input_sentence, rules, current):
    data = input_sentence.split()
    for i in range(0, len(data)):
        data[i] = data[i].split('_')
    # print (data)

    # Initialize the missing tags to the most probable tags from the current_tag corpus
    missing = {}
    for i in range(0, len(data)):
        if data[i][1] == '??':
            for j in range(0, len(current)):
                if current[j][0] == data[i][0]:
                    data[i][1] = current[j][1]
                    missing[data[i][0]] = current[j][1]

    # Check from all possible rules if any of them apply
    for i in range(0, len(data)):

        if data[i][0] in missing:
            if missing.get(data[i][0]) == "NN":
                prev_tag = data[i - 1][1]

                if prev_tag == rules[0][2]:
                    data[i][1] = rules[0][2]
                if prev_tag == rules[1][2]:
                    data[i][1] = rules[1][2]
    return data


if __name__ == "__main__":
    filepath = 'HW2_F18_NLP6320_POSTaggedTrainingSet-Windows.txt'
    f = read_file(filepath)
    correct_tags = preprocess(f)
    corpus = corpus_generate(correct_tags)
    counted_tokens = token_counter(correct_tags)
    counted_tags = tag_counter(correct_tags)
    current_tags = retag(corpus, counted_tags)
    tag_set = tag_set(correct_tags)
    rules, best_rule = get_best_instance(correct_tags, current_tags)
    input_sen = "The_DT standard_?? Turbo_NN engine_NN is_VBZ hard_JJ to_TO work_??"
    answer = find_missing(input_sen, best_rule, current_tags)

    print ("\n")
    print ("The best learnt rules from Brill's Algorithm for NN to VB and NN to JJ conversion are as follows: ")
    print ("[From, To, Previous]")
    for i in best_rule:
        print (i)

    print ("\n\n")
    print ("The output sentence without any missing tags")
    for i in range(0, len(answer)):
        answer[i] = answer[i][0] + "_" + answer[i][1]
    print (answer)
