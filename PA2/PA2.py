# -*- coding: utf-8 -*-
import sys 
import getopt
import re
import math
import ir_tools as ir

# -- main function --
def main(argv=None):
	if argv == None:
		argv = sys.argv
	#extract the document and make dictionary data
	print "----- start extracting documents, 1095 documents to extract -----"
	#print "extracting..."
	term_list=[]
	terms_data = {}
	document_data = []
	i=0
	sys.stdout.write("extracting...[%.2f%%]" % (i/10.95))
	sys.stdout.flush()
	for i in xrange(1,1096):
		f = open("IRTM/"+str(i)+".txt","r")
		tokens = ir.tokenize(f.read())
		terms = []
		for token in tokens:
			term = ir.stemword(token)
			if not re.compile("^[\d_]").match(term) and term:
				terms.append(term)
				if term not in term_list:
					term_list.append(term)
				if term not in terms_data:
					terms_data[term]={"frq":1,"df":0}
				else:
					terms_data[term]["frq"] = terms_data[term]["frq"] +1
		f.close()
		terms = ir.remove_stopword(terms)
		document_data.append(terms)

		sys.stdout.write("\rextracting... [%.2f%%]" % (i/10.95))
		sys.stdout.flush()
	sys.stdout.write("\n")
		
	#construct dictionary for the collection
	term_list = ir.remove_stopword(term_list)
	term_list.sort()
	print "----- extracting finished -----"
	
	print "----- calculating df for each term -----"

	N = 1095
	#calculate df
	progress=0 
	sys.stdout.write("calculating... [%.2f%%]" % (float(progress)*100/float(len(term_list))))
	sys.stdout.flush()
	for term in term_list:
		progress= progress+1
		for doc in document_data:
			if term in doc:
				terms_data[term]["df"] = terms_data[term]["df"] +1
		sys.stdout.write("\rcalculating... [%.2f%%]" % (float(progress)*100/float(len(term_list))))
		sys.stdout.flush()
	sys.stdout.write("\n")
	print "----- calculating finished -----"
	print "----- creating dictionary file -----"
	#save in dictionary.txt
	i = 0
	save = open("dictionary.txt","w")
	save.write("t_index\tterm\tdf\n")
	for term in term_list:
		i= i+1
		save.write(str(i)+"\t"+term+"\t"+str(terms_data[term]["df"])+"\n")
		terms_data[term]["t_index"] = i
	save.close()
	print "----- finish creating dictionary -----"
	print "----- save the tf-idf for each document -----"
	#save the idf to each document
	i=0
	sys.stdout.write("saving...[%.2f%%]" % (i/10.95))
	sys.stdout.flush()
	for i in xrange(1,1096):
		save = open("idf/"+str(i)+".txt","w")
		doc_data = document_data[i-1]
		temp_list = []
		idf_data = {}
		for term in doc_data:
			if term not in idf_data:
				temp_list.append(term)
				idf_data[term] = {"idf":math.log10(N / terms_data[term]["df"]),"tf":1}
			else:
				idf_data[term]["tf"] = idf_data[term]["tf"]+1
		temp_list.sort()
		save.write(str(len(temp_list))+"\n")
		save.write("t_index\ttf-idf\n")
		for term in temp_list:
			save.write(str(terms_data[term]["t_index"])+"\t"+str(idf_data[term]["idf"]*idf_data[term]["tf"])+"\n")
		
		sys.stdout.write("\rsaving...[%.2f%%]" % (i/10.95))
		sys.stdout.flush()
	sys.stdout.write("\n")
	print "----- finished -----"

if __name__ == "__main__":
	main()