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
from page import PostscriptPage
from customer import Customer
import sys # testing only

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
        self.today           = date.today().strftime("%A, %B %d, %Y")
        self.title           = '' # text string for title
        self.header          = '' # text string for header
        self.footer          = '' # text strings for footer
        self.customers       = []
        self.fileBaseName    = fileBaseName
        self.font            = 'Courier'
        self.fontSize        = 10.0         # points
        self.kerning         = 11.0
            
    # this method actually formats the customers data into pages.
    def format( self, isDebug=True ):
        # now we are ready to output pages.
        customerNotices = []
        totalPages = 1
        for customer in self.customers:
            pageNumber = 1
            customerPages = []
            # create a page for the customer
            page = PostscriptPage( pageNumber, self.font, self.fontSize, self.kerning )
            # every page gets a title and statement date and header
            page.setTitle( self.title )
            yPos = page.setStatementDate( 'Statement produced: ' + str( self.today ) )
            # Each customer gets only one header message so set that now
            # page.setHeader( self.header )
            
            # item = customer.getNextItem()
            # page.setItem( item, 0.875, yPos )
            customerPages.append( page )
            for page in customerPages:
                # now we know the total pages for a customer we can output the statement count
                # page.setStatementCount( 'Statement ' + str( pageNumber ) + ' of '+ str( len( customerPages ) ) )
                pageNumber += 1
                totalPages += 1
                
            # place the customer notice onto the list of notices.
            customerNotices.append( customerPages )
        self.__finalize_notices__( customerNotices, totalPages, isDebug )
        
    def __finalize_notices__( self, customerNotices, totalPages, isDebug ):
        myFile = open( self.fileBaseName + '.ps', 'w' )
        myFile.write( '%!PS-Adobe-2.0\n' )
        myFile.write( '% Created for Edmonton Public Library ' + str( self.today ) + '\n' )
        WARNING_MSG  = "% This file contains personal information about customers of Edmonton Public Library\n" 
        WARNING_MSG += "% This information is protected by EPL's FOIP policy, and must NOT be distributed with expressed\n" 
        WARNING_MSG += "% permission from the management of EPL.\n"
        myFile.write( WARNING_MSG )
        myFile.write( '/' + self.font + ' findfont\n' + str( self.fontSize ) + ' scalefont\nsetfont\n' )
        registrationMarkProcedureCall = ''
        if isDebug == True:
            registrationMarkProcedureCall = self.__add_registration_marks__( myFile )
        # Tell the PS file how many pages in total there will be
        myFile.write( '%%Pages: ' + str( totalPages ) + '\n' ) 
        for customerNotice in customerNotices:
            for page in customerNotice:
                if isDebug == True:
                    myFile.write( registrationMarkProcedureCall )
                myFile.write( str( page ) )
        myFile.close()
    
    # Adds the fold lines as dashed lines, for registration comparison during debugging.        
    def __add_registration_marks__( self, myFile ):
        myFile.write( '/inch {\n\t72.0 mul\n} def\n' )
        myFile.write( '/perfline {\n' )
        myFile.write( '[6 3] 3 setdash\n' )
        myFile.write( 'stroke\n' )
        myFile.write( 'newpath\n' )
        myFile.write( '} def\n' )
        myFile.write( '/fineperfline {\n' )
        myFile.write( 'gsave\n' )
        myFile.write( '0.5 setgray\n' )
        myFile.write( '[4 2] 0 setdash\n' )
        myFile.write( 'stroke\n' )
        myFile.write( 'grestore\n' )
        myFile.write( 'newpath\n' )
        myFile.write( '} def\n' )
        myFile.write( '/pageborder{\n' )
        myFile.write( '0.5 inch 0  inch moveto\n' )
        myFile.write( '0.5 inch 11 inch lineto\n' )
        myFile.write( '8   inch 0  inch moveto\n' )
        myFile.write( '8   inch 11 inch lineto\n' )
        myFile.write( '0.5 setlinewidth\n' )
        myFile.write( 'perfline\n' )
        myFile.write( '0   inch 3.15625 inch moveto\n' )
        myFile.write( '8.5 inch 3.15625 inch lineto\n' )
        myFile.write( '0.25 setlinewidth\n' )
        myFile.write( 'fineperfline\n' )
        myFile.write( '0   inch 3.625 inch moveto\n' )
        myFile.write( '8.5 inch 3.625 inch lineto\n' )
        myFile.write( 'fineperfline\n' )
        myFile.write( '0   inch 4.15625 inch moveto\n' )
        myFile.write( '8.5 inch 4.15625 inch lineto\n' )
        myFile.write( 'fineperfline\n' )
        myFile.write( '0   inch 6.90625 inch moveto\n' )
        myFile.write( '8.5 inch 6.90625 inch lineto\n' )
        myFile.write( 'fineperfline\n' )
        myFile.write( '0   inch 7.3125  inch moveto\n' )
        myFile.write( '8.5 inch 7.3125  inch lineto\n' )
        myFile.write( 'fineperfline\n' )
        myFile.write( '0   inch 10.5    inch moveto\n' )
        myFile.write( '8.5 inch 10.5    inch lineto\n' )
        myFile.write( 'fineperfline\n' )
        myFile.write( '} def\n' )
        return 'pageborder\n'
        
    # def __define_procedure__( self, fName, fBody ):
        # if len( fBody ) == 0:
            # return ''
        # return '/'+fName+' {\n'+'\n'.join( fBody )+'\n} def\n'
    
    # Sets the customer data to be printed to the final notices.
    # Formats customers into multi-sheet notices if necessary.
    # Customers must be valid customers.
    def setCustomer( self, customer ):
        self.customers.append( customer )
        
    def setGlobalTitle( self, text ):
        self.title = text
        
    def setGlobalHeader( self, text ):
        self.header = text
        
    def setGlobalFooter( self, text ):
        self.footer = text

    def __str__( self ):
        return 'Postscript formatter: ' + self.fileName
    
# Initial entry point for program
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    formatter = PostscriptFormatter( 'testFormatPage' )
    formatter.setGlobalTitle( 'Test Page' )
    formatter.setGlobalHeader( 'Statement produced: Friday, August 24 2012\nThis is a test to see if the page break feature works. This line is far too long to fit on one line and should actually appear on two or more!' )
    c = Customer()
    customer = c.__create_customer__()
    formatter.setCustomer( customer )
    formatter.format( True )
