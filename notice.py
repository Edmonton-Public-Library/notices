#!/usr/bin/python
###########################################################################
# Purpose: Notice object.
#
# Author:  Andrew Nisbet, Edmonton Public Library
# Date:    November 7, 2012
# Rev:     
#          0.0 - Dev.
###########################################################################

import customer
from datetime import date
from noticeformatter import NoticeFormatter

class Notice:
	def __init__( self, inFile ):
		self.today         = date.today()
		self.humanDate     = self.today.strftime("%A, %B %d, %Y")
		self.iFileName     = inFile
		self.oFileName     = 'delete_' + str( self.today ) # If we see this file the subclass screwed up.
		self.oFile         = None
		self.statementDate = 'Statement produced: ' + self.humanDate
		self.formatter     = None
		# reporting values
		self.pagesPrinted  = 0
		self.noticeCount   = 0  # number of customers notices processed.
		self.incorrectAddress = []  # number of notices that couldn't be printed because customer data was malformed.
		
	# Reads the report and parses it into customer related notices.
	# Returns number of pages that will be printed.
	def parseReport( self, suppress_malformed_customer=True ):
		return self.pagesPrinted
		
	def setOutputFormat( self, formatter ):
		self.formatter = formatter
		
	def writeToFile( self ):
		self.formatter.format()
		
	def getOutFileBaseName( self ):
		return self.oFileName
		
	def __get_lines__( self ):
		# read in the report and parse it.
		iFile = open( self.iFileName, 'r' )
		print 'reading reading reading .... '
		lines = iFile.readlines()
		iFile.close()
		blocks = []
		lines.reverse()
		return lines
		
	def __str__( self ):
		return ' input file = ' + self.iFileName
		
class Hold( Notice ):
	def __init__( self, inFile ):
		Notice.__init__( self, inFile )
		self.oFileName = 'notices_hold_' + str( self.today ) 
		self.title = 'PICKUP NOTICE'
		
	def __str__( self ):
		return 'Hold Notice using: ' + self.iFileName
		
	# Reads the report and parses it into customer related notices.
	# Returns number of pages that will be printed.
	def parseReport( self, suppress_malformed_customer=True ):
		return False
		
class Overdue( Notice ):
	def __init__( self, inFile ):
		Notice.__init__( self, inFile )
		self.oFileName = 'notices_overdue_' + str( self.today )
		self.title = 'OVERDUE NOTICE'
		
	def __str__( self ):
		return 'Overdue Notice using: ' + self.iFileName
		
	# Reads the report and parses it into customer related notices.
	# Returns number of pages that will be printed.
	def parseReport( self, suppress_malformed_customer=True ):
		return False
		
class Bill( Notice ):
	def __init__( self, inFile, billLimit=10.0 ):
		Notice.__init__( self, inFile )
		self.oFileName = 'notices_bills_' + str( self.today )
		self.minimumBillValue = billLimit
		self.title = 'NEW BILLINGS'
		
	def __str__( self ):
		return 'Bill Notice using: ' + self.iFileName + '\nminimum bill value = ' + str( self.minimumBillValue )
		
	# Reads the report and parses it into customer related notices.
	# Returns number of pages that will be printed.
	def parseReport( self, suppress_malformed_customer=True ):
		# read in the report and parse it.
		lines = self.__get_lines__()
		# now pop off each line from the file and form it into a block of data
		while( len( lines ) > 0 ):
			line = lines.pop()
			if line.startswith( '.read' ): # message read instruction not in block. Thanks Sirsi.
				print 'found new customer'
			elif line.startswith( '.block' ):
				print 'block detected'
				while( len( lines ) > 0  ):
					line = lines.pop()
					if line.startswith( '.endblock' ):
						break
					if line.startswith( '.read' ): # closing message and end of customer.
						print 'found end of customer'
						break
					print line
				
		return True
