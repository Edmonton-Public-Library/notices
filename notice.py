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
from noticeformatter import Formatter

NAME_DATE = '_DATE_'
TODAY     = date.today()

class Notice:
	def __init__( self, inFile ):
		self.iFile = inFile
		self.oFile = 'delete' + NAME_DATE # If we see this get rid of it the subclass screwed up.
		self.date  = TODAY.strftime("%A, %B %d, %Y")
		# Statememt date same for all notices
		self.statementDate = 'Statement produced: ' + self.date
		self.formatter = None
		
	def parseReport( self ):
		# read in the report and parse it.
		return True
		
	def setOutputFormat( self, formatter ):
		self.formatter = formatter
	
	# this method breaks the page into multiple pages if it is too long.
	def paginate( self ):
		pass
		
	def write( self ):
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
		return 'Bill Notice using: "' + self.iFile + ' minimum bill value = ' + str( self.minimumBillValue ) + '"'