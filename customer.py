#!/usr/bin/env python
###########################################################################
# Purpose: Customer objects.
#
# Author:  Andrew Nisbet, Edmonton Public Library
# Date:    November 7, 2012
# Rev:     
#          0.0 - Dev.
###########################################################################

class Item:
	def __init__( self ):
		self.itemLines = []
		
	def addLine( self, text ):
		self.itemLines.append( text )
		
	def __str__( self ):
		return '\n'.join( self.itemLines )
		
		
class Customer:
	def __init__( self ):
		self.addressBlock = []
		self.items        = []
		self.items.append( Item() )
		
	def setAddressText( self, text ):
		self.addressBlock.append( text )
		
	def setItemText( self, text ):
		"""
		>>> c = Customer()
		>>> c.setItemText( "  1 this and that" )
		>>> print c
		  1 this and that
		"""
		# get the first item off the list
		item = self.items.pop()
		# Test if the first non-white char is a digit. Thats when to create a new item.
		if text.lstrip()[0].isdigit():
			# if we already are working with an item then append it to the array of items
			self.items.append( item )
			item = Item()
		item.addLine( text )
		# put it back on the stack for next time.
		self.items.append( item )
			
	def __str__( self ):
		output = ''
		for item in self.items:
			output += str( item )
		return output
	
	# Returns true if the customer's email address is complete and valid
	# and False otherwise. The last line of an address must be a postal code.
	def isWellFormed( self ):
		return len( self.addressBlock[-1].strip() ) == 7 # you can think of a better regex for a postal code.
		
def main():
	customer = Customer()
	# print customer
	# customer.setAddressText('some address')
	# print customer
	# customer.setItemText('text')
	# print customer
	
# Initial entry point for program
if __name__ == "__main__":
	import doctest
	doctest.testmod()
	main()