#!/usr/bin/python

__author__ = "Joe Edwards"
__version__ = "1.0.0"
__created__ = "08-21-2014"
__modified__ = "08-28-2014"
__maintainer__ = "Joe Edwards"
__email__ = "edwards@ucdavis.edu"

import sys
import getopt
import re


script_info = {}
script_info['description'] = """
network_tax_matcher.py

This script will go through a network file and will match taxonomies from a taxonomy file to the OTUs.


Usage:

network_tax_matcher.py -i network.txt -o net_tax.txt [-u]"""

script_info['usage'] = """
Usage:

network_tax_matcher.py -i network.txt -o net_tax.txt [-u]

-i	input network.  
-t	input taxonomy file.
-o	output file. Defaults to net_tax.txt
-u	print usage statement
"""

#################
# Load in options
#################
def optLoad():
	## Load the files in based on the command line arguments
	net_file = ''
	output_file = 'net_tax.txt'
	tax_file = ''
	opts, args = getopt.getopt(sys.argv[1:], "i:o:t:u")
	for o, a in opts:
		if o == '-i':
			net_file = a
		elif o == '-o':
			output_file = a
		elif o == '-t':
			tax_file = a
		elif o == '-u':
			print script_info['usage']
			sys.exit()
			#raise Exception()
		elif o == '-v':
			print_var = True
		else:
			print script_info['usage']
			raise Exception()

	if net_file == '':
		print '[ERROR] Please include an input file!'
		print script_info['usage']
		raise Exception()
	return(net_file, tax_file, output_file)

def network_load(lines):
	net_dict = {}
	header = lines.readline()
	for line in lines:
		fields = line.rstrip().split("\t")
		otu = fields[0]
		otu = str(re.sub('\"', '', otu))
		module = str(fields[2])
		net_dict[otu] = module

	return(net_dict)

def taxonomy_parse(lines, net_dict, out_file):
	fout = open(out_file, 'w')
	header = lines.readline()
	print >> fout, "OTU\tModule\tKingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tSpecies"
	for line in lines:
		fields = line.rstrip().split("\t")
		otu = fields.pop(0)
		if otu in net_dict:
			print >> fout, otu, "\t", str(net_dict[otu]), "\t", join("\t").fields


def main():
	net_file, tax_file, output_file = optLoad()
	net_dict = network_load(open(net_file))
