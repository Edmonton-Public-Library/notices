#!/usr/bin/env python 
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
from page import breakLongLines
from page import PostscriptPage

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
        self.today  = date.today().strftime("%A, %B %d, %Y")
        self.fontSizeTitle   = 18.0    # points
        self.fontSizeText    = 10.0    # points
        self.xTitle          = 3.3125  # inches
        self.yTitle          = 10.1875 # inches
        self.title           = []
        self.header          = []
        self.footer          = []
        self.fontDescription = ['/Courier findfont', '10 scalefont', 'setfont']
        self.File            = open( fileBaseName + '.ps', 'w' )
        self.File.write( '%!PS-Adobe-2.0\n' )
        self.File.write( '% Created for Edmonton Public Library ' + self.today + '\n' )
        self.File.write( WARNING_MSG )
        # defining this converts inches to points so all measurements (except font size) can be set in inches.
        self.File.write( self.__define_function__( 'inch', ['72.0 mul'] ) )
    
    # this method actually formats the customers data into pages.
    def format( self ):
        # Do the formatting then close the file.
        # First write out the function definitions that we use 
        # in each page of the Postscript file.
        # 1) all pages get a header text message.
        self.File.write( self.__define_function__( 'report_title', self.title ))
        self.File.write( self.__define_function__( 'report_title', self.fontDescription ))
        return True
        
    def __define_function__( self, fName, fBody ):
        if len( fBody ) == 0:
            return ''
        else:
            return '/'+fName+' {\n'+'\n'.join( fBody )+'\n} def\n'
    
    # Sets the customer data to be printed to the final notices.
    # Formats customers into multi-sheet notices if necessary.
    def setCustomer( self, customer ):
        # Each customer is a separate page.
        pass
        
    def setGlobalTitle( self, text ):
        self.title = [ 
            'gsave', 
            '/Courier-Bold findfont', 
            str( self.fontSizeTitle )+' scalefont', 
            'setfont', 
            'newpath', 
            str( self.xTitle )+' '+str( self.yTitle )+' moveto',
            '('+str(text)+') show',
            'grestore' ]
        
    def setGlobalHeader( self, text ):
        # get the page to split the text on the page boundaries for us.
        self.header = breakLongLines( text )
        for line in self.header:
            print line
        
    def setGlobalFooter( self, text ):
        self.footer = text

    def __str__( self ):
        return 'Postscript formatter: ' + self.fileName
    
# Initial entry point for program
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    formatter = PostscriptFormatter( 'testFormatPage' )
    # formatter.setGlobalTitle( 'Test Page' )
    formatter.setGlobalHeader( 'This is a test to see if the page break feature works. This line is far too long to fit on one line and should actually appear on two or more!' )
    formatter.format()
