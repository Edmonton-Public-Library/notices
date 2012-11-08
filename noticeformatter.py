#!/usr/bin/python
###########################################################################
# Purpose: Notice object.
#
# Author:  Andrew Nisbet, Edmonton Public Library
# Date:    November 7, 2012
# Rev:     
#          0.0 - Dev.
###########################################################################

import page

class Formatter:
	def __init__( self ):
		self.File = None
	# outputs border.
	def __printtest__( self ):
		pass
	def openDocument( self, fileName ):
		pass
	def setTitle( self, text ):
		pass
	def setStatementDate( self, text ):
		pass
	def setMessage( self, text='GLOBAL' ):
		pass
	def setCustomer( self, customer ):
		pass
	def closeDocument( self ):
		pass
		
class PostscriptFormatter( Formatter ):
	def __init__( self ):
		Formatter.__init__( self )

	# prints the borders of the ps for registration and proofing.
	def __printtest__( self ):
		self.File.write('this is a test 2\n')
	def openDocument( self, fileName ):
		try:
			self.File = open( fileName, 'w' );
		except e:
			print repr( e )
	def setTitle( self, text ):
		pass
	def setStatementDate( self, text ):
		pass
	def setMessage( self, text='GLOBAL' ):
		pass
	def setCustomer( self, customer ):
		pass
	def closeDocument( self ):
		# terminate the file and close it.
		self.File.close()
		
		

def main():
	formatter = PostscriptFormatter()
	formatter.openDocument( 'test.ps' )
	formatter.__printtest__()
	formatter.closeDocument()
	
# Initial entry point for program
if __name__ == "__main__":
	import doctest
	doctest.testmod()
	main()		