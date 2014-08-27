#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

__author__ = "Joe Edwards"
__version__ = "1.0.0"
__created__ = "08-21-2014"
__modified__ = "08-28-2014"
__maintainer__ = "Joe Edwards"
__email__ = "edwards@ucdavis.edu"

import sys
import getopt 
import pandas as pd 
from rpy2.robjects.packages import importr
import rpy2.robjects as ro
import pandas.rpy.common as com

script_info = {}
script_info['description'] = """
top_var.py

This script will take an OTU table and perform pairwise correlations on the values.
Using the resulting matrix as a distance matrix it will perform heirarchical clustering.
The tree will then be pruned using the R package 'DynamicTreeCut.'
There is an optional optimization step in progress.

Usage:

top_var.py -i otu_table.txt -o network.txt -m spearman [-b] [-u]"""

script_info['usage'] = """
Usage:

top_var.py -i otu_table.txt -o network.txt -m spearman [-b] [-u]

-i   input OTU table.  Must be tab delimited and have OTUs as rows and samples as columns
-o   output file. Defaults to network.txt
-m   method for correlation.  Default is spearman. Also takes pearson and kendall
-b   optimize the network.
-u   print usage statement
"""

def optLoad():
	## Load the files in based on the command line arguments
	otu_file = ''
	output_file = 'network.txt'
	m = "spearman"
	optimize = False
	opts, args = getopt.getopt(sys.argv[1:], "i:o:m:bu")
	for o, a in opts:
		if o == '-i':
			otu_file = a
		elif o == '-o':
			output_file = a
		elif o == '-m':
			m = a.lower()
			method_check(m)
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
	return(otu_file, output_file, m, optimize)

def method_check(m):
	accepted = {'pearson': 1, 'spearman': 1, 'kendall' : 1}
	if m in accepted:
		return()
	else:
		print "[ERROR] Please use an acceptable correlation method."
		print script_info['usage']

#def correlate

def main():
	otu_file, output_file, m, optimize = optLoad()
	otu_tab = pd.read_table(otu_file, sep = "\t", index_col = 0)
	otu_corr = otu_tab.transpose().corr(method = m)
	"""
	Going to end it here for now.  I'm finding out that I have to do everything in R because
	I need to use an R package to actually do the dynamic tree cutting. I can't figure out how to 
	talk to R via Python to do this at the moment.
	"""
	## Switch to Using R


main()



