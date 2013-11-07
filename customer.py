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
    
    def addAllLines( self, textBlock ):
        self.itemLines = textBlock
        
    def addLine( self, text ):
        self.itemLines.append( text )
        
    def getLastLine( self ):
        if len( self.itemLines ) == 0:
            return ''
        return self.itemLines[-1]
        
    def isEmpty( self ):
        return len( self.itemLines ) == 0 or len( self.itemLines[0] ) == 0
        
    def getItem( self ):
        return self.itemLines
        
    def getSize( self ):
        return len( self.itemLines )
        
    def __str__( self ):
        return ' '.join( self.itemLines )
        
# This class represents a customer who is potentially going to receive a notice from 
# the library. A Customer knows if its address is well formatted and can answer the 
# question 'can a printed notice for this customer be processed by Canada Post?'
class Customer:
    def __init__( self ):
        self.addressBlock = ItemBlock()
        self.header       = ''          # a customer header is for personalization. Currently only pickup library for holds.
        self.items        = []
        self.summaryBlock = ItemBlock() # Used for determining total bill amounts. The text is treated as an item though.
        self.postalCode   = re.compile( "(\s+)?[a-z]\d[a-z](\s+)?\d[a-z]\d(\s+)?", re.IGNORECASE )
        self.email        = ''
        self.pagesPrinted = 0
    
    # Sets the total pages printed for this customer.
    # param:  count - integer number of pages printed for customer.
    # return: 
    def setPageTotal( self, count ):
        self.pagesPrinted = count
        
    def setHeader( self, text ):
        self.header = text
        
    def getPagesPrinted( self ):
        return self.pagesPrinted
    
    # Returns True if the customer has more items and False otherwise.
    def hasMoreItems( self ):
        """
        >>> c = Customer()
        >>> print c.hasMoreItems()
        False
        >>> c.setItemText( "1" )
        >>> c.setItemText( "a" )
        >>> print c.hasMoreItems()
        True
        """
        return len( self.items ) > 0
    
    # Sets the pages printed for a customer for reporting.
    # param:  Number of pages printed.
    def setPagesPrinted( self, count ):
        self.pagesPrinted = count
        
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
        
    # Adds text to a summary block.
    def setSummaryText( self, text ):
        self.summaryBlock.addLine( text )
        # This treats the summary on bills as just part of the last item.
        # The summary text is used to calculate how much the customer owes on all bills.
        # self.setItemText( text )
    
    # Returns an array strings from the summary block.
    # param:  
    # return: array of strings which may be empty.
    def getFooter( self ):
        item = self.summaryBlock.getItem()
        self.summaryBlock = ItemBlock() # removes the summary block so it behaves like an item.
        return item
        
    def hasFooter( self ):
        """
        >>> c = Customer()
        >>> c.setSummaryText( '1' )
        >>> c.setSummaryText( '2' )
        >>> print str( c.summaryBlock )
        1 2
        >>> print c.hasFooter()
        True
        >>> item = c.getFooter()
        >>> print c.hasFooter()
        False
        """
        return not self.summaryBlock.isEmpty()
        
    def pushFooter( self, item ):
        """
        >>> c = Customer()
        >>> c.setSummaryText( '1' )
        >>> c.setSummaryText( '2' )
        >>> print str( c.summaryBlock )
        1 2
        >>> item = c.getFooter()
        >>> print str( c.summaryBlock )
        <BLANKLINE>
        >>> print str( item )
        ['1', '2']
        >>> c.pushFooter( item )
        >>> print str( c.summaryBlock )
        1 2
        """
        pushedItem = ItemBlock()
        pushedItem.addAllLines( item )
        self.summaryBlock = pushedItem
    
    # This method returns the total bills for the customer. If this customer was created
    # for a holds or overdue report the return value is 0.0. If the customer was invoked
    # by a bills report then the method returns the customers total bills.
    def getTotalBills( self ):
        """
        >>> c = Customer()
        >>> c.setSummaryText( '      =======================================================================' )
        >>> c.setSummaryText( '                                  TOTAL FINES/FEES AND UNPAID BILLS:     $2.00' )
        >>> print str( c.getTotalBills() )
        2.0
        >>> c.setSummaryText( '                                  some accidental line with no dollar value mentioned. ' )
        >>> print str( c.getTotalBills() )
        0.0
        """
        lastLine = self.summaryBlock.getLastLine()
        if lastLine == '':
            return 0.0
        try:
            return (float)(lastLine.split( '$' )[-1].rstrip())
        except IndexError:
            return 0.0
        
    # Returns the address block as an array of strings.
    def getAddress( self ):
        return self.addressBlock.getItem()
        
    def pushItem( self, textBlock ):
        """
        >>> c = Customer()
        >>> c.setItemText( "1" )
        >>> c.setItemText( "a" )
        >>> c.setItemText( "2" )
        >>> c.setItemText( "b" )
        >>> print len(c.items)
        2
        >>> print str(c.items[0])
        1 a
        >>> item = c.getNextItem()
        >>> print item
        ['1', 'a']
        >>> print len(c.items)
        1
        >>> c.pushItem( item )
        >>> print len(c.items)
        2
        >>> print str(c.items[0])
        1 a
        """
        replacementItem = ItemBlock()
        replacementItem.addAllLines( textBlock )
        self.items.insert( 0, replacementItem )
        
    # Sets the customer item text. Item text is added one line at-a-time
    # but items are packaged individually within this class.
    def setItemText( self, text ):
        """
        >>> c = Customer()
        >>> c.setItemText( "  1 this and that" )
        >>> print c.items[0]
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
        if len( text.strip() ) < 1:
            return
        item = None
        # Test if the first non-white char is a digit. Thats when to create a new item.
        if text.lstrip()[0].isdigit() or len( self.items ) == 0:
            item = ItemBlock()
        else:
            # get the first item off the list
            item = self.items.pop()
        item.addLine( text )
        # put it back on the stack for next time.
        self.items.append( item )
        
    # Returns the next item block text as an array or an empty array if there are no more.
    def getNextItem( self ):
        """
        >>> c = Customer()
        >>> c.setItemText( "1" )
        >>> c.setItemText( "a" )
        >>> c.setItemText( "2" )
        >>> c.setItemText( "b" )
        >>> print len(c.items)
        2
        >>> c.getNextItem()
        ['1', 'a']
        >>> print str( len( c.getNextItem() ) )
        2
        >>> c.getNextItem()
        []
        """
        try:
            nextItem = self.items.pop( 0 )
            return nextItem.getItem()
        except IndexError:
            return []
            
    def __str__( self ):
        output =  '[CUSTOMER\ncutomer receives mail notices: '+str(self.getsPrintedNotices())+'\n'
        output += 'cutomer\'s mail address is valid: '+str(self.isWellFormed())+'\n'
        output += 'items for this customer include: %d\n' % len( self.items )
        output += 'address block: \n' + str(self.addressBlock)
        return output + 'CUSTOMER]\n'
    
    # Returns true if the customer's mail address is complete and valid
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
        return not isinstance( self.postalCode.match( self.addressBlock.getLastLine().strip() ), type( None ) )
    
    # Creates a customer with bogus data for testing.
    def __create_customer__( self ):    
        """
        >>> c = Customer()
        >>> customer = c.__create_customer__()
        """
        c = Customer()
        c.setAddressText('Balzac Billy')
        c.setAddressText('12345 123 Street')
        c.setAddressText('Edmonton, Alberta')
        c.setAddressText('H0H 0H0')
        for i in range( 1, 8 ):
            c.setItemText('  '+str(i)+'   The lion king 1 1/2 [videorecording] / [directed by Bradley Raymond].')
            c.setItemText('      Raymond, Bradley.')
            c.setItemText('      $<date_billed:3>10/23/2012   $<bill_reason:3>OVERDUE      $<amt_due:3>     $1.60')
        return c
    
 
        
# Initial entry point for program
if __name__ == "__main__":
    import doctest
    doctest.testmod()