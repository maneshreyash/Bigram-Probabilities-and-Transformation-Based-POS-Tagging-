# N-Grams and POS Tagging
Author: Shreyash Sanjay Mane (ssm170730)

# Bigram Probabilities:
Write a computer program to compute the bigram model (counts and probabilities) on the given corpus (HW2_F17_NLP6320-NLPCorpusTreebank2Parts-CorpusA.txt provided as Addendum to this homework on eLearning) under the following three (3) scenarios: 
* No Smoothing
* Add-one Smoothing
* Good-Turing Discounting based Smoothing

Note:
* Use the “ . ” string sequence in the corpus to break it into sentences.
* Each sentence should be tokenized into words and the bigrams computed ONLY within a sentence.
* Please use whitespace (i.e. space, tab, and newline) to tokenize a sentence into words/tokens that are required for the bigram model.
* Do NOT perform any type of word/token normalization (i.e. stem, lemmatize, lowercase, etc.).
* Creation and matching of bigrams should be exact and case-sensitive.

Input Sentence: The Fed chairman warned that the board 's decision is bad

Given the bigram model (for each of the three (3) scenarios) computed by your
computer program, hand compute the total probability for the above input sentence.

Please provide all the required computation details.
Note: Do NOT include the unigram probability P(“The”) in the total probability
computation for the above input sentence


# Transformation Based POS Tagging

For this question, you have been given a POS-tagged training file, HW2_F17_NLP6320_POSTaggedTrainingSet.txt (provided as Addendum to this homework on eLearning), that has been tagged with POS tags from the Penn Treebank POS tagset (Figure 1). 

Use the POS tagged file to perform:

* Transformation-based POS Tagging: Implement Brill’s transformation-based POS
tagging algorithm using ONLY the previous word’s tag to extract the best
transformation rule to:
i. Transform “NN” to “JJ”
ii. Transform “NN” to “VB”

Using the learnt rules, fill out the missing POS tags (for the words “standard” and
“work”) in the following sentence:

The_DT standard_?? Turbo_NN engine_NN is_VBZ hard_JJ to_TO work_??b. Naïve Bayesian Classification (Bigram) based POS Tagging:

* Using the given corpus, write a computer program to compute the bigram models (counts and probabilities) required by the above Naïve Bayesian Classification formula.
Using the created bigram models, hand compute the missing POS tags (for the words “standard” and “work”) in the following sentence: The_DT standard_?? Turbo_NN engine_NN is_VBZ hard_JJ to_TO work_??

Steps to run the code:

1. For BiGram Models:
	Run the file using command: python Ques_2_Bigrams_Smoothing.py

	The outputs will be written in the files named accordingly.

4. For Brill's POS Tagging:
	Run the file using command: python Ques_3a_Brills.py
	The output will be printed in the console.

5. For POS Tagging using Naive Bayesian Classification using Bigrams:
	Run the file using command: python Ques_3b_Naive_Bayes.py
	The output is the probabilities necessary for hand computation.
