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
        self.fileName        = fileBaseName
        self.title           = ''
        self.header          = ''
        self.footer          = ''
        self.today           = date.today().strftime("%A, %B %d, %Y")
        self.startNoticePath = ''
        self.endNoticePath   = ''

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
    def setFooter( self, text ):
        self.footer = text
    
    # Sets the closing notice (if any). This message limits the program to run on the
    # production server.
    # param:  readTag - path to the file to read, looks like '.read /s/sirsi/Unicorn/Notices/enclose
    # return: 
    def setClosingBulletin( self, readTag ):
        self.footer = readTag
        
    # Sets the closing notice (if any). This message limits the program to run on the
    # production server.
    # param:  readTag - path to the file to read, looks like '.read /s/sirsi/Unicorn/Notices/enclose
    # return: 
    def setOpeningBulletin( self, readTag ):
        pass
        
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
        return True
        
    # Sets the closing notice (if any). This message limits the program to run on the
    # production server.
    # param:  readTag - path to the file to read, looks like '.read /s/sirsi/Unicorn/Notices/enclose
    # return: 
    # TODO:  fix so this need not run on just the production server.
    def setClosingBulletin( self, readTag ):
        self.endNoticePath = readTag.split()[1]
        print 'setting end notice to read from path: ' + self.endNoticePath
        
    # Sets the open notice. This message limits the program to run on the
    # production server.
    # param:  readTag - path to the file to read, looks like '.read /s/sirsi/Unicorn/Notices/enclose
    # return: 
    # TODO:  fix so this need not run on just the production server.
    def setClosingBulletin( self, readTag ):
        self.startNoticePath = readTag.split()[1]
        print 'setting end notice to read from path: ' + self.startNoticePath
        
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