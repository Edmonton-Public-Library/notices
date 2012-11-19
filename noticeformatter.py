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
    def __init__( self ):
        pass
    # Sets the customer data to be printed to the final notices.
    # Formats customers into multi-sheet notices if necessary.
    def setCustomer( self, customer ):
        pass
        
    def setGlobalTitle( self, title ):
        pass
        
    def setGlobalHeader( self, text ):
        pass
        
    def setGlobalFooter( self, text ):
        pass
    
    # Formats the customers into pages based on the target output
    # file format.
    def format( self ):
        pass
        
class PostscriptFormatter( NoticeFormatter ):
    def __init__( self, fileBaseName ):
        self.today = date.today().strftime("%A, %B %d, %Y")
        self.File = open( fileBaseName + '.ps', 'w' )
        self.File.write( '%!PS-Adobe-2.0\n' )
        self.File.write( '% Created for Edmonton Public Library ' + self.today + '\n' )
        self.File.write( WARNING_MSG )
    
    # this method actually formats the customers data into pages.
    def format( self ):
        # Do the formatting then close the file.
        return True
    
    # Sets the customer data to be printed to the final notices.
    # Formats customers into multi-sheet notices if necessary.
    def setCustomer( self, customer ):
        pass
        
    def setGlobalTitle( self, title ):
        pass
        
    def setGlobalHeader( self, text ):
        pass
        
    def setGlobalFooter( self, text ):
        pass

    def __str__( self ):
        return 'Postscript formatter: ' + self.fileName
    
# Initial entry point for program
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    formatter = PostscriptFormatter( 'test.ps' )
    formatter.format()