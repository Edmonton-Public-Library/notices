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
from customer import Customer

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
        self.leftMargin      = 0.875   # inches
        self.fontSizeTitle   = 18.0    # points
        self.fontSizeText    = 10.0    # points
        self.xTitle          = 3.3125  # inches
        self.yTitle          = 10.1875 # inches
        self.yHeader         = self.leftMargin
        self.xHeader         = 9.875
        self.yHeaderEnd      = 8.0
        self.xHeaderEnd      = self.leftMargin
        self.xFooter         = self.leftMargin
        self.yFooter         = 4.5
        self.xAddressBlock   = 4
        self.yAddressBlock   = 1.75
        self.yItemLimit      = 4.68
        self.title           = []
        self.header          = []
        self.footer          = []
        self.fontDescription = ['/Courier findfont', '10 scalefont', 'setfont']
        self.customers       = []
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
        if len( self.title ) > 0:
            self.File.write( self.__define_function__( 'report_title', self.title ))
        self.File.write( self.__define_function__( 'report_font', self.fontDescription ))
        if len( self.header ) > 0:
            self.File.write( self.__define_function__( 'report_header', self.header ))
        # now we are ready to output pages.
        count = 1
        for customer in self.customers:
            # create a page for the customer
            page = PostscriptPage( count, True )
            count += self.__format_customer__( customer, page )
        return True
        
    def __format_customer__( self, customer, page ):
        # these don't have to be in order, address can be output first since PS plots by absolute x,y positions.
        # tell the page to add the title and header function to itself so they print on this page.
        page.setInstruction( 'report_title' )
        page.setInstruction( 'report_header' )
        page.setTextBlock( customer.getAddress(), self.xAddressBlock, self.yAddressBlock, False )
        pageCount = 1
        itemBlock = customer.getNextItem()
        nextLine = self.yHeaderEnd ############ TODO find where the header ended adn fix this ##############
        while len( itemBlock ) > 0:
            # msg = ['  1   The lion king 1 1/2 [videorecording] / [directed by Bradley Raymond].',
            # '      Raymond, Bradley.',
            # '      $<date_billed:3>10/23/2012   $<bill_reason:3>OVERDUE      $<amt_due:3>     $1.60']
            nextLine = page.setTextBlock( itemBlock, self.leftMargin, ( nextLine - 0.18 ), True, True )
            #test if we are at the bottom of the page and if yes print out the page statement.
            if nextLine < self.yItemLimit:
                page.setLine('Statement 1 of 2', 0.875, 4.5 ) ######### TODO fix this ########
                nextLine = self.yHeaderEnd
                self.File.write( page )
                ######### TODO create new page and call recursively ?????   
        self.File.write( page )
        return pageCount
        
    def __define_function__( self, fName, fBody ):
        if len( fBody ) == 0:
            return ''
        else:
            return '/'+fName+' {\n'+'\n'.join( fBody )+'\n} def\n'
    
    # Sets the customer data to be printed to the final notices.
    # Formats customers into multi-sheet notices if necessary.
    # Customers must be valid customers.
    def setCustomer( self, customer ):
        self.customers.append( customer )
        
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
        # only do this for global text. Use page's setTextBlock() otherwise.
        block = breakLongLines( text )
        yPos  = self.yHeader
        for line in block:
            self.header.append( 'newpath' )
            self.header.append( str( self.xHeader )+' '+str( yPos )+' moveto' )
            self.header.append( '('+str( line )+') show' )
            # calculate the position of the next line
            yPos -= 0.18 ###### TODO fix this so its not hard coded #########
        
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
    formatter.setGlobalHeader( 'Statement produced: Friday, August 24 2012\nThis is a test to see if the page break feature works. This line is far too long to fit on one line and should actually appear on two or more!' )
    
    formatter.format()
