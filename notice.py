#!/usr/bin/python
###########################################################################
# Purpose: Format notices from reports into printable format.
# Method:  
# Find the prn report for corresponding bills, holds, or overdues. 
# Remove headers and footers of report (or ignore).
# Split report into chunks by customer boundary.
#	Split customer data into page chunks
#		Add Header with '.read /s/sirsi/Unicorn/Notices/blankmessage'
#		Optionally add additional graphic (HOLDs)
#		Add page item details
#		Add 'Statement 1 of n'
#		Add User name address
#	Format each page into PS and append to file
#
# Author:  Andrew Nisbet, Edmonton Public Library
# Date:    November 7, 2012
# Rev:     
#          0.0 - Dev.
###########################################################################

import sys
import getopt

def usage():
	print 'Usage:'
	print '  notice.py [-b[10]dh] -i <inputfile> -o <outputfile>'
	print '  Processes Symphony reports into printable notice format'
	
# Take valid command line arguments -b'n', -o, -i, -d, and -h.
def main( argv ):
	inputfile  = ''
	outputfile = ''
	billLimit  = 10.0
	try:
		opts, args = getopt.getopt( argv, "dhb:i:o:", [ "dollars=", "ifile=", "ofile=" ] )
	except getopt.GetoptError:
		usage()
		sys.exit()
	for opt, arg in opts:
		if opt == '-h':
			pass # holds.
		elif opt == '-d':
			pass # overdues
		elif opt in ( "-b", "--dollars" ): # bills
			billLimit = arg 
		elif opt in ( "-i", "--ifile" ):
			inputfile = arg
		elif opt in ( "-o", "--ofile" ):
			outputfile = arg
	print 'Input file is = ', inputfile
	print 'Output file is = ', outputfile
	print 'Lower bill limit = ', billLimit

# Initial entry point for program
if __name__ == "__main__":
	import doctest
	doctest.testmod()
	main(sys.argv[1:])
