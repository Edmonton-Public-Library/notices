#!/usr/bin/env python
###########################################################################
# Purpose: Customer objects. Customers have a number of items (to be notified
# about), and an address block.
#
# Author:  Andrew Nisbet, Edmonton Public Library
# Date:    November 9, 2012
# Rev:     
#          0.0 - Dev.
###########################################################################

import re

# Items are blocks of text information destined for the notice. An item 
# is starts with a number that enumerates a list of a patron's items.
class ItemBlock:
    def __init__( self ):
        self.itemLines = []
        
    def addLine( self, text ):
        self.itemLines.append( text )
        
    def getLastLine( self ):
        return self.itemLines[-1]
        
    def __str__( self ):
        return '\n'.join( self.itemLines )
        
# This class represents a customer who is potentially going to receive a notice from 
# the library. A Customer knows if its address is well formatted and can answer the 
# question 'can a printed notice for this customer be processed by Canada Post?'
class Customer:
    def __init__( self ):
        self.addressBlock = ItemBlock()
        self.items        = [ItemBlock()]
        self.summaryBlock = ItemBlock()
        self.postalCode   = re.compile( "(\s+)?[a-z]\d[a-z]\s{1}\d[a-z]\d(\s+)?", re.IGNORECASE )
        self.email        = ''
        
    # Adds text to an address block. 
    def setAddressText( self, text ):
        self.addressBlock.addLine( text )
    
    # Sets the customer email, which in turn lets the customer object know that it doesn't 
    # get printed.
    # param:  text string containing '.email email@address.com'
    # return: 
    def setEmail( self, text ):
        address = text.split()[1]
        self.email = address
    
    # Answers the question: customer, do you receive printed notices?
    # param:  
    # return: True if customer does not have an email address and False otherwise.
    def getsPrintedNotices( self ):
        """
        >>> c = Customer()
        >>> c.getsPrintedNotices()
        True
        >>> c.setEmail( ".email ilsteam@epl.ca" )
        >>> c.getsPrintedNotices()
        False
        """
        return len( self.email ) == 0
        
    # Adds text to an summary block. 
    def setSummaryText( self, text ):
        print '%%%%%%%%%%%% Hey I ran - Nice job! %%%%%%%%%%%%%%%%%'
        self.summaryBlock.addLine( text )
        
    # Sets the customer item text. Item text is added one line at-a-time
    # but items are packaged individually within this class.
    def setItemText( self, text ):
        """
        >>> c = Customer()
        >>> c.setItemText( "  1 this and that" )
        >>> print c
          1 this and that
        >>> print len(c.items)
        1
        >>> c.setItemText( "     another line" )
        >>> print len(c.items)
        1
        >>> c.setItemText( "  2 this and that" )
        >>> c.setItemText( "     another second line" )
        >>> print len(c.items)
        2
        """
        if len( text.lstrip() ) < 1:
            return
        item = None
        # Test if the first non-white char is a digit. Thats when to create a new item.
        if text.lstrip()[0].isdigit():
            item = ItemBlock()
        else:
            # get the first item off the list
            item = self.items.pop()
        item.addLine( text )
        # put it back on the stack for next time.
        self.items.append( item )
            
    def __str__( self ):
        output = ''
        for item in self.items:
            output += str( item )
        output += '\nsummary block: ' + str(self.summaryBlock)
        output += '\naddress block: ' + str(self.addressBlock)
        return output + '\n'
    
    # Returns true if the customer's email address is complete and valid
    # and False otherwise. The last line of an address must be a postal code.
    def isWellFormed( self ):
        """
        >>> c = Customer()
        >>> c.setAddressText( "  Funky Monkey" )
        >>> print c.isWellFormed()
        False
        >>> c.setAddressText( "  12345 123 Street" )
        >>> print c.isWellFormed()
        False
        >>> c.setAddressText( "  Edmonton, Alberta" )
        >>> print c.isWellFormed()
        False
        >>> c.setAddressText( "  TgG jkl" )
        >>> print c.isWellFormed()
        False
        >>> c.setAddressText( "  T6G 0KY" )
        >>> print c.isWellFormed()
        False
        >>> c.setAddressText( "  T6G 0g4" )
        >>> print c.isWellFormed()
        True
        """
        # check if the matcher returned a non-None object when compared to the last line of the address block
        return not isinstance( self.postalCode.match( self.addressBlock.getLastLine() ), type( None ) )
    
# Initial entry point for program
if __name__ == "__main__":
    import doctest
    doctest.testmod()