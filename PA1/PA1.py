# -*- coding: utf-8 -*-
import sys 
import getopt
# import ir tools
import ir_tools as ir


# -- main function --
def main(argv=None):
	if argv == None:
		argv = sys.argv
	doc_name = argv[1]
	savefile_name = argv[2]
	#read the document
	f = open(doc_name)
	doc = f.read()
	#tokenization and lowercasing
	tokens = ir.tokenize(doc)
	#stemming
	terms = ir.stemming(tokens)
	#stopword removal
	terms = ir.remove_stopword(terms)
	#save the result
	save = open(savefile_name,"w")
	for term in terms:
		save.write(term+"\n")
	save.close()
	f.close()


if __name__ == "__main__":
	main()