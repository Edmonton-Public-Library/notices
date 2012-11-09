#!/usr/bin/env python
###########################################################################
# Purpose: Customer objects.
#
# Author:  Andrew Nisbet, Edmonton Public Library
# Date:    November 7, 2012
# Rev:     
#          0.0 - Dev.
###########################################################################

class Customer:
	def __init__( self ):
		self.addressBlock = ''
		self.items        = []
		
	def setAddressText( self, text ):
		pass
		
	def setItemText( self, text ):
		pass
		
	def __str__( self ):
		return ''
	
	# Returns true if the customer's email address is complete and valid
	# and False otherwise.
	def isWellFormed( self ):
		return False
		
def main():
	customer = Customer()
	print customer
	customer.setAddress('some address')
	print customer
	customer.setItemText('text')
	print customer
	
# Initial entry point for program
if __name__ == "__main__":
	import doctest
	doctest.testmod()
	main()