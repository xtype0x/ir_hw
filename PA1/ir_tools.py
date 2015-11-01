# -*- coding: utf-8 -*-
import re
import porter

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
	p = porter.PorterStemmer()
	return p.stem(word,0,len(word)-1)

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
