# -*- coding: utf-8 -*-

import sys 
import os
import getopt
import re
import math
import ir_tools as ir


N = 1095
I = []

# -- main function --
def main(argv=None):
	if argv == None:
		argv = sys.argv
	K = int(argv[1])
	#simple HAC
	print "----- HAC Clustering -----"
	#initialize
	cluster = {}
	C = [[0 for x in range(N)] for x in range(N)]

	sys.stdout.write("initializing similarity matrix...[%.2f%%]" % (0/10.95))
	sys.stdout.flush()
	if os.path.exists("./sim_matrix.dat"):
		f = open("sim_matrix.dat","r")
		lines = f.readlines()
	for n in xrange(0,N):
		if os.path.exists("./sim_matrix.dat"):
			line = lines[n]
			vals = line.replace("\n","").split(" ")
			i=0
			for val in vals:
				C[n][i] = float(val)
				i=i+1
		else:
			for i in xrange(0,N):
				if n > i:
					C[n][i] = C[i][n]
				elif n == i:
					C[n][i] = 1.0
				else:
					C[n][i] = ir.cosine(n+1,i+1)

		I.append(1)
		cluster[n] = [n]

		sys.stdout.write("\rinitializing similarity matrix... [%.2f%%]" % ((n+1)/10.95))
		sys.stdout.flush()

	sys.stdout.write("\n")

	if os.path.exists("./sim_matrix.dat"):
		f.close()
	else:
		f = open("sim_matrix.dat","w")
		for c in C:
			f.write(" ".join(str(v) for v in c))
			f.write("\n")
		f.close()


	merge_index=[]
	#print C
	sys.stdout.write("\rclustering...[%.2f%%]" % (0))
	sys.stdout.flush()
	for k in xrange(0,N-K):
		pair = argmax(C)
		cluster[pair[0]].append(pair[1])
		for j in xrange(0,N):
			val = cluster_sim(cluster[j], cluster[pair[0]], C)
			C[pair[0]][j] = val
			C[j][pair[0]] = val
			sys.stdout.write("\rclustering...[%.2f%%]" % (float(k*N + j + 1)*100/(N*(N-K))))
			sys.stdout.flush()
		I[pair[1]] = 0
		merge_index.append(pair[1])
	sys.stdout.write("\n")

	print "----- save in the file -----"
	save = open(str(K)+".txt","w")
	for index in cluster:
		if index not in merge_index:
			for docid in cluster[index]:
				save.write(str(docid+1))
				save.write("\n")
			save.write("\n")
	save.close()
	print "finish clustering ^^"



def argmax(C):
	max_sim = float("-inf")
	pair = (0,0)
	for i in xrange(0,N):
		for j in xrange(0,N):
			if(i != j and I[i] == 1 and I[j] == 1 and C[i][j] > max_sim):
				max_sim = C[i][j]
				pair = (i,j)
	return pair

#use compelte-link
def cluster_sim(clu1, clu2, C):
	min_sim = float("inf")
	for c1 in clu1:
		for c2 in clu2:
			min_sim = min(C[c1][c2],min_sim)
	return min_sim



if __name__ == "__main__":
	main()