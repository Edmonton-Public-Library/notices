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
		
	def setAddress( self, text ):
		pass
	def setItemText( self, text ):
		pass
		
	def __str__( self ):
		return ''
		
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