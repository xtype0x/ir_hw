# -*- coding: utf-8 -*-
import re
from nltk.stem import *
import math

# -- IR tools --

"""
-- tokenize for english words, will convert to lowercase  --
params:
	doc: string (document for tokenization)
return: 
	list of tokens
"""
def tokenize(doc):
	tokens = re.compile("(?!-)\W*").split(doc.lower())
	#print tokens
	if "" in tokens:
		tokens.remove("")
	return tokens

"""
--- stemming tokens ---
params:
	tokens: list (list of tokens preparing for stemming)
return: 
	list of terms
"""
def stemming(tokens):
	#stemming each token and save in a new list
	terms = []
	for token in tokens:
		term = stemword(token)
		if term not in terms:
			terms.append(term)
	return terms

"""
--- use Poter's algorithm to stem the word ---
params: 
	word: string (the word for stemming)
return
	stemming word (string)
"""

def stemword(word):
	p = PorterStemmer()
	return p.stem(word)

"""
--- remove the stopwords from the terms ---
params:
	terms: list (list of terms)
return:
	list of terms
"""
def remove_stopword(terms):
	f = open("stopwordlist.txt","r")
	stopword_list = f.read().splitlines()
	f.close()
	new_terms = []
	for term in terms:
		if term not in stopword_list and term not in new_terms:
			new_terms.append(term)
	return new_terms


"""
--- calculate frequency for a document ---
params: 
	terms: list (list of terms)
return:
	list of term data
"""
def calc_frq(terms):
	dictionary = {}
	for term in terms:
		if term not in dictionary:
			dictionary[term]={"frq":1}
		else:
			dictionary[term]["frq"] = dictionary[term]["frq"] + 1
	return dictionary

"""
--- calculating cosine similarity ---
dictionary.txt required
params:
	docx: int (open {docx}.txt)
	docy: int
return:
	cosine similarity : float
"""
def cosine(docx,docy):
	#load dictionary data
	x = open("idf/"+str(docx)+".txt")
	y = open("idf/"+str(docy)+".txt")
	lines = x.readlines()
	x_index = []
	x_data={}
	for i in xrange(2,len(lines)-2):
		line = lines[i].split("\t")
		x_data[int(line[0])] = float(line[1])
		x_index.append(int(line[0]))
	lines = y.readlines()
	common_index=[]
	y_data={}
	for i in xrange(2,len(lines)-2):
		line = lines[i].split("\t")
		y_data[int(line[0])] = float(line[1])
		if int(line[0]) in x_index:
			common_index.append(int(line[0]))
	x.close()
	y.close()
	#caclulate similarity
	x_vector_len = 0.0
	y_vector_len = 0.0
	for i in x_data:
		x_vector_len = x_vector_len + x_data[i]*x_data[i]
	for i in y_data:
		y_vector_len = y_vector_len + y_data[i]*y_data[i] 
	x_vector_len = math.sqrt(x_vector_len)
	y_vector_len = math.sqrt(y_vector_len)
	inner_product = 0.0
	for ind in common_index:
		inner_product = inner_product +x_data[ind]*y_data[ind]

	return (inner_product/x_vector_len/y_vector_len)

