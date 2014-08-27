#!/usr/bin/python

__author__ = "Joe Edwards"
__version__ = "1.0.0"
__created__ = "08-21-2014"
__modified__ = "08-28-2014"
__maintainer__ = "Joe Edwards"
__email__ = "edwards@ucdavis.edu"

import sys
import getopt 
from numpy import var as V

script_info = {}
script_info['description'] = """
top_var.py

This script will go through an OTU matrix and find the OTUs with the most variance.
The user must specify how many OTUs they would like back, the the program will default to 2000.
The user can optionally have a file printed out with the variance values for each OTU

Usage:

top_var.py -i otu_table.txt -o top_var_otus.txt -n 2000 [-v] [-u]"""

script_info['usage'] = """
Usage:

top_var.py -i otu_table.txt -o top_var_otus.txt -n 2000 [-v] [-u]

-i   input OTU table.  Must be tab delimited and have OTUs as rows and samples as columns
-o   output file. Defaults to top_var_otus.txt
-n   number of OTUs to keep. Defaults to 2000
-v   output the variances for each OTU
-u   print usage statement
"""

#################
# Load in options
#################
def optLoad():
	## Load the files in based on the command line arguments
	otu_file = ''
	output_file = 'top_var_otus.txt'
	n = 2000
	print_var = False
	opts, args = getopt.getopt(sys.argv[1:], "i:o:n:vu")
	for o, a in opts:
		if o == '-i':
			otu_file = a
		elif o == '-o':
			output_file = a
		elif o == '-n':
			n = int(a)
		elif o == '-u':
			print script_info['usage']
			sys.exit()
			#raise Exception()
		elif o == '-v':
			print_var = True
		else:
			print script_info['usage']
			raise Exception()

	if otu_file == '':
		print '[ERROR] Please include an input file!'
		print script_info['usage']
		raise Exception()
	return(otu_file, output_file, n, print_var)

def varCalc(lines, print_var):
	if print_var:
		print "---> Printing all variances otu_variances.txt"
		fout = open("otu_variances.txt", 'w')
		print >> fout, "OTU\tVariance" 

	header = lines.readline()
	variances = {}
	for line in lines:
		line = line.rstrip("\n")
		counts = line.split("\t")
		otu = str(counts.pop(0))
		counts = [float(i) for i in counts]
		var = float(V(counts))
		variances[otu] = var
		if print_var:
			print >> fout, otu, "\t", var

	return(variances)

def topVar(variances, n, output_file, lines):
	fout = open(output_file, 'w')

	## Sort hash to get highest vars
	count = 0
	tops = {}
	sorted_otus = []
	print "---> Sorting variances"
	for otu, var in sorted(variances.iteritems(), key=lambda (k,v): (v,k)):
		#if count == n:
		#	break
		sorted_otus.append(otu)
	best_otus = sorted_otus[-n:]
	for otu in best_otus:
		tops[otu] = 1

	## Go through original OTU file to get top
	print "---> Printing values for top OTUs"
	print >> fout, lines.readline().rstrip("\n")
	for line in lines:
		line = line.rstrip("\n")
		counts = line.split("\t")
		otu = str(counts.pop(0))
		if otu in tops:
			print >> fout, line



###################
# Find OTUs to keep
###################
## If list of OTUs exists get that

	## Else figure out how many OTUs we want to keep, have a default value ready

## Calculate the variance for OTUs and load into hash

## Sort hash

## Grab names of top x OTUs

def main():
	otu_file, output_file, n, print_var = optLoad()
	variances = varCalc(open(otu_file), print_var)
	topVar(variances, n, output_file, open(otu_file))

main()

