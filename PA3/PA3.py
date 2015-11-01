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
	#load 1095 documents
	#extract the document and make dictionary data
	print "----- start extracting documents, 1095 documents to extract -----"
	#print "extracting..."
	term_list=[]
	terms_data = {}
	document_data = [{}]
	i=0
	sys.stdout.write("extracting...[%.2f%%]" % (i/10.95))
	sys.stdout.flush()
	for i in xrange(1,1096):
		f = open("IRTM/"+str(i)+".txt","r")
		tokens = ir.tokenize(f.read())
		terms = []
		doc = {"terms":[],"length":0,"class":0}
		for token in tokens:
			doc["length"] = doc["length"] + 1
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
		doc["terms"] = terms
		terms = ir.remove_stopword(terms)
		document_data.append(doc)

		sys.stdout.write("\rextracting... [%.2f%%]" % (i/10.95))
		sys.stdout.flush()
	sys.stdout.write("\n")
	print "----- extracting last step... -----"
	#construct dictionary for the collection
	#term_list = ir.remove_stopword(term_list)
	#term_list.sort()
	#print "----- extracting finished -----"
	
	#load training set data
	training_set = {}
	f = open("training.txt","r")
	lines = f.readlines();
	for line in lines:
		data_set = line.replace("\r\n","").split(" ")
		training_set[int(data_set[0])] = data_set[1:15]
		for did in data_set[1:15]:
			document_data[int(did)]["class"] = int(data_set[0])
	f.close()
	#training phase
	print "----- start training -----"
	N = 1095 #document counts
	Nc = 15.0 #document count in each class
	prior = {}
	condprob={}
	i = 0 
	sys.stdout.write("training...[%.2f%%]" % (i/0.15))
	sys.stdout.flush()
	for c in training_set:
		prior[c] = Nc / N
		text_c =[]
		T_c = {}
		T_total = 0
		for did in training_set[c]:
			text_c = text_c + document_data[int(did)]["terms"]
		for t in term_list:
			T_c[t] = text_c.count(t)
			T_total = T_total+T_c[t]
		for t in term_list:
			if t not in condprob:
				condprob[t]={}
			condprob[t][c]= float(T_c[t]+1)/(T_total+1)
		i = i+1
		sys.stdout.write("\rtraining... [%.2f%%]" % (i/0.15))
		sys.stdout.flush()

	print "----- training finished! -----"
	print "----- start testing remaining documents -----"
	sys.stdout.write("\rtesting...[%.2f%%]" % (0/10.95))
	sys.stdout.flush()

	for did in xrange(1,1096):
		if document_data[did]["class"] == 0:
			#do testing
			current_score = float('-inf')
			current_class = 0
			for c in training_set:
				score = math.log(prior[c])
				for t in document_data[did]["terms"]:
					if t in condprob:
						score = score + math.log(condprob[t][c])
				if score > current_score:
					current_score = score
					current_class = c
			document_data[did]["class"] = current_class
		sys.stdout.write("\rtesting...[%.2f%%]" % (did/10.95))
		sys.stdout.flush()


	print "----- testing fininshed!! -----"
	print "----- start generating output.txt -----"
	f = open("output.txt","w")
	for did in xrange(1,1096):
		#print str(did)+": "+str(document_data[did]["class"])
		f.write(str(did)+" "+str(document_data[did]["class"])+"\n")
	f.close()
	print "----- PA3 done^^ -----"



if __name__ == "__main__":
	main()