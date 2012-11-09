#!/usr/bin/python
###########################################################################
# Purpose: Formatter object. This object brokers information from Customer
# to a location on a page, dependant on the underlying requirement of 
# the type of output you are creating. Formatter is a interface, the
# real work happens in the subclasses that take care of set of the whole
# report, the coordination of the pagination and placement data on a 
# notice and any clean up required to create a well formed output document.
#
# Author:  Andrew Nisbet, Edmonton Public Library
# Date:    November 7, 2012
# Rev:     
#          0.0 - Dev.
###########################################################################
from datetime import date
import page

WARNING_MSG  = "% This file contains personal information about customers of Edmonton Public Library\n" 
WARNING_MSG += "% This information is protected by EPL's FOIP policy, and must NOT be distributed with expressed\n" 
WARNING_MSG += "% permission from the management of EPL.\n"

class NoticeFormatter:
	def __init__( self, fileBaseName ):
		self.fileName  = fileBaseName
		self.title     = ''
		self.header    = ''
		self.footer    = ''
		self.today     = date.today().strftime("%A, %B %d, %Y")

	# Sets the title of the notice.
	def setTitle( self, text ):
		self.title = text
	
	# Sets the global header-message string for the notices.
	def setHeader( self, text ):
		self.header = text
	
	# Sets the footer text (if any).
	# Normally the footer is reserved for the 'Statement 1 of 1' message
	# which is added automatically when the customer is formatted.
	# (See setCustomer()).
	def setFooters( self, text ):
		self.footer = text
		
	# Sets the customer data to be printed to the final notices.
	# Formats customers into multi-sheet notices if necessary.
	def setCustomer( self, customer ):
		pass
	
	# Formats the customers into pages based on the target output
	# file format.
	def format( self ):
		self.File.close()
		return True
		
class PostscriptFormatter( NoticeFormatter ):
	def __init__( self, fileBaseName ):
		NoticeFormatter.__init__( self, fileBaseName + '.ps' )
	
	# this method actually formats the customers data into pages.
	def format( self ):
		# Do the formatting then close the file.
		psText  = '%!PS-Adobe-2.0\n'
		psText += '% Created for Edmonton Public Library ' + self.today + '\n'
		psText += WARNING_MSG

# %%Pages: 2'
		return True
		
	def __str__( self ):
		return 'Postscript formatter: ' + self.fileName

def main():
	formatter = PostscriptFormatter( 'test.ps' )
	formatter.format()
	
# Initial entry point for program
if __name__ == "__main__":
	import doctest
	doctest.testmod()
	main()