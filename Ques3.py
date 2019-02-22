
def read_file(path):
    file_content = open(path, "r")
    # print(f.read())
    file_content = file_content.read()
    return file_content


def preprocess(contents):
    pairs = contents.split()
    for i in range(0, len(pairs)):
        pairs[i] = pairs[i].split('_')
    return pairs


def corpus_generate(tagged_tokens):
    data = []
    for token in tagged_tokens:
        data.append(token[0])
    return data


def token_counter(tags):
    data = {}
    for token in tags:
        if token[0] not in data:
            data[token[0]] = 1
        else:
            data[token[0]] += 1
    return data


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


def retag(inp, tags, tokens):
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


def tag_set(tags):
    tag = set()
    for i in tags:
        tag.add(i[1])
    return tag


def get_best_instance(correct_tags, current_tags):
    to_tags = {"JJ", "VB"}
    rules = []
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
        print(num_good_transforms)
        best_Z = max(num_good_transforms, key=num_good_transforms.get)
        # best_score = 0
        # if num_good_transforms.get(best_Z) > best_score:
        best_score = num_good_transforms.get(best_Z)
        rule = []
        rule.append("NN")
        rule.append(to_tag)
        rule.append(best_Z)
        print (best_score)
        rules.append(rule)
    return rules

if __name__ == "__main__":
    filepath = 'HW2_F18_NLP6320_POSTaggedTrainingSet-Windows.txt'
    f = read_file(filepath)
    correct_tags = preprocess(f)
    corpus = corpus_generate(correct_tags)
    counted_tokens = token_counter(correct_tags)
    counted_tags = tag_counter(correct_tags)
    current_tags = retag(corpus, counted_tags, counted_tokens)
    tag_set = tag_set(correct_tags)
    best = get_best_instance(correct_tags, current_tags)
    print (best)