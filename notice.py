#!/usr/bin/python
###########################################################################
# Purpose: Notice object.
#
# Author:  Andrew Nisbet, Edmonton Public Library
# Date:    November 7, 2012
# Rev:     
#          0.0 - Dev.
###########################################################################

from customer import Customer
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
		self.customers     = []
		
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
		
	# Adds item text from the report to the customer.
	# def __set_customer_items__( self, lines, customer ):
		# pass
		
	# def __set_customer_address__( self, lines, customer ):
		# pass
		
	# def __set_customer_summary__( self, lines, customer ):
		# while( len( lines ) > 0  ):
			# line = lines.pop()
			# if line.startswith( '.endblock' ):
				# return
			# customer.setAddressText( line )
			
	def __set_customer_data__( self, lines, customerFunc ):
		while( len( lines ) > 0  ):
			line = lines.pop()
			if line.startswith( '.endblock' ):
				return
			customer.customerFunc( line )
		
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
		# .block
		# Luckie Luke
		# 12345 120 Street
		# Edmonton, AB
		# T5X 5N8
		# .endblock
		# .read /s/sirsi/Unicorn/Notices/blankmessage
		# .block
		# 1   A woman betrayed / Barbara Delinsky.
		# Delinsky, Barbara.
		# $<date_billed:3>10/23/2012   $<bill_reason:3>OVERDUE      $<amt_due:3>     $0.75
		# .endblock
		# .block
		# 2   Jump! / Jilly Cooper.
		# Cooper, Jilly.
		# $<date_billed:3>10/23/2012   $<bill_reason:3>OVERDUE      $<amt_due:3>     $0.75
		# .endblock
		# .block
		# 3   A perfect proposal / Katie Fforde.
		# Fforde, Katie.
		# $<date_billed:3>10/23/2012   $<bill_reason:3>OVERDUE      $<amt_due:3>     $0.75
		# .endblock
		# .block
		# 4   Looking for Peyton Place : a novel / Barbara Delinsky.
		# Delinsky, Barbara.
		# $<date_billed:3>10/23/2012   $<bill_reason:3>OVERDUE      $<amt_due:3>     $0.75
		# .endblock
		# .block
		# =======================================================================
		#
		#					 $<total_fines_bills:3>     $3.00
		# .endblock
		# .block
		# .read /s/sirsi/Unicorn/Notices/eclosing
		# .endblock
		# read in the report and parse it.
		lines = self.__get_lines__()
		# now pop off each line from the file and form it into a block of data
		customer = Customer()
		while( len( lines ) > 0 ):
			line = lines.pop()
			if line.startswith( '.block' ):
				# grab lines of the stack until the block ends.
				while( len( lines ) > 0 ):
					line = lines.pop()
					if line.startswith( '.endblock' ):
						break
					elif line.startswith( '.read' ): # closing message and end of customer.
						print 'found end message and end of customer'
						# get the message and pass it to the noticeFormatter.
						self.customers.append( customer )
						customer = Customer()
						break
					elif line.find( '=====' ) > 0: # summary block.
						print 'found summary'
						self.__set_customer_data__( lines, customer.setSummaryText )
					print line,
			elif line.startswith( '.read' ): # message read instruction not in block. Thanks Sirsi.
				print 'opening message and customer items'
			# ignore everything else it's just dross.
		return True
		
# Initial entry point for program
if __name__ == "__main__":
	import doctest
	doctest.testmod()
