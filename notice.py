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
import os
import customer
from datetime import date

NAME_DATE = '_DATE_'
TODAY     = date.today()

class Notice:
	def __init__( self, inFile ):
		self.iFile = inFile
		self.oFile = 'delete' + NAME_DATE # If we see this get rid of it the subclass screwed up.
		self.date  = TODAY.strftime("%A, %B %d, %Y")
		# Statememt date same for all notices
		self.statementDate = 'Statement produced: ' + self.date
	def readReport( self ):
		pass
	def __str__( self ):
		return ' input file = ' + self.iFile
		
class Hold( Notice ):
	def __init__( self, inFile ):
		Notice.__init__( self, inFile )
		self.oFile = 'holds' + NAME_DATE
		self.title = 'PICKUP NOTICE'
	def __str__( self ):
		return 'Hold Notice using: "' + self.iFile + '"'
		
class Overdue( Notice ):
	def __init__( self, inFile ):
		Notice.__init__( self, inFile )
		self.oFile = 'overdue' + NAME_DATE
		self.title = 'OVERDUE NOTICE'
	def __str__( self ):
		return 'Overdue Notice using: "' + self.iFile + '"'
		
class Bill( Notice ):
	def __init__( self, inFile, billLimit=10.0 ):
		Notice.__init__( self, inFile )
		self.oFile = 'bills' + NAME_DATE
		self.minimumBillValue = billLimit
		self.title = 'NEW BILLINGS'
	def __str__( self ):
		return 'Bill Notice using: "' + self.iFile + ' minimum bill value = ' + self.minimumBillValue + '"'

def usage():
	print 'Usage:'
	print '  notice.py [-b[10]dh] -i <inputfile> -o <outputfile>'
	print '  Processes Symphony reports into printable notice format'
	
# Take valid command line arguments -b'n', -o, -i, -d, and -h.
def main( argv ):
	inputFile  = ''
	noticeType = 'INIT'
	billLimit  = 10.0
	try:
		opts, args = getopt.getopt( argv, "ohb:i:", [ "dollars=", "ifile=" ] )
	except getopt.GetoptError:
		usage()
		sys.exit()
	for opt, arg in opts:
		if opt == '-h':
			noticeType = 'HOLD' # holds.
		elif opt == '-o':
			# overdues
			noticeType = 'ODUE' # overdues.
		elif opt in ( "-b", "--dollars" ): # bills
			billLimit = arg 
			noticeType = 'BILL' # bills.
		elif opt in ( "-i", "--ifile" ):
			inputFile = arg
	print 'Input file is = ', inputFile
	print 'Lower bill limit = ', billLimit
	if os.path.isfile( inputFile ) == False:
		print 'error: ' + inputFile + ' is empty or does not exist.'
		sys.exit()
	notice = None
	if noticeType == 'HOLD':
		notice = Hold( inputFile )
	elif noticeType == 'BILL':
		notice = Bill( inputFile )
	elif noticeType == 'ODUE':
		notice = Overdue( inputFile )
	else:
		print 'nothing to do; notice type not selected'
		usage()
		sys.exit()
	print notice

# Initial entry point for program
if __name__ == "__main__":
	import doctest
	doctest.testmod()
	main(sys.argv[1:])
