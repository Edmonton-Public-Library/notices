#!/usr/bin/python
###########################################################################
# Purpose: Notice object.
#
# Author:  Andrew Nisbet, Edmonton Public Library
# Date:    November 7, 2012
# Rev:     
#          0.0 - Dev.
###########################################################################

class Formatter:
	def __init__( self ):
		pass
	# outputs border.
	def __printtest__( self ):
		pass
	def open( self, fileName ):
		pass
	def setTitle( self, text ):
		pass
	def setStatementDate( self, text ):
		pass
	def setMessage( self, text='GLOBAL' ):
		pass
	def setItemText( self, text ):
		pass
	def setFooter( self, text ):
		pass
	def setAddress( self, text ):
		pass
	def close( self ):
		pass
		
class PostscriptFormatter( Formatter ):
	def __init__( self ):
		Formatter.__init__( self )
	# prints the borders of the ps for registration and proofing.
	def __printtest__( self ):
		pass
		
	def open( self, fileName ):
		pass
	def setTitle( self, text ):
		pass
	def setStatementDate( self, text ):
		pass
	def setMessage( self, text='GLOBAL' ):
		pass
	def setItemText( self, text ):
		pass
	def setFooter( self, text ):
		pass
	def setAddress( self, text ):
		pass
	def close( self ):
		pass
		
		

def main():
	formatter = PostscriptFormatter()
	formatter.open( 'test.ps' )
	formatter.__printtest__()
	formatter.close()
	
# Initial entry point for program
if __name__ == "__main__":
	import doctest
	doctest.testmod()
	main()		