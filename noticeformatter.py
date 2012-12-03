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
from page import POINTS
from customer import Customer


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
        self.kerning         = 12.0         # points
        self.blockSpacing    = self.kerning / POINTS # inches
        self.leftMargin      = 0.875
            
    # this method actually formats the customers data into pages.
    def format( self, isDebug=True ):
        # now we are ready to output pages.
        customerNotices = []
        totalPageCount = 1
        for customer in self.customers:
            customerPages = []
            isFirstPage = True
            while( customer.hasMoreItems() ):
                page = self.__get_additional_page__( totalPageCount, customer, isFirstPage )
                if isFirstPage == True: # First page needs a header, 
                    isFirstPage = False
                customerPages.append( page )
                totalPageCount += 1
            # add the statement page of pages notice
            pageTotal           = len( customerPages )
            customersPageNumber = 1
            for page in customerPages:
                # now we know the total pages for a customer we can output the statement count
                page.setStatementCount( 'Statement ' + str( customersPageNumber ) + ' of '+ str( pageTotal ) )
                customersPageNumber += 1
                # place the customer notice onto the list of notices.
                customerNotices.append( page )
        self.__finalize_notices__( customerNotices, isDebug )
        
    # Returns a minimized string of the first characters an ellipsis and last 10 characters
    # of a line like: 'This is how a very long line would be printed ... end of the line.'
    # param:  string text to shorten
    # param:  Maximum number of characters allowed - default 83. 
    # return: string text shortened
    def __minimize_line__( self, text, maxCharacters=83 ):
        """
        >>> nf = PostscriptFormatter('someFileName')
        >>> print '"' + nf.__minimize_line__('12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890', 40) + '"'
        "1234567890123456789012345 ... 1234567890"
        >>> print '"' + nf.__minimize_line__('1234567890123456789012345678901234567890', 40) + '"'
        "1234567890123456789012345678901234567890"
        >>> print '"' + nf.__minimize_line__('123456789012345678901234567890123456789', 40) + '"'
        "123456789012345678901234567890123456789"
        >>> print '"' + nf.__minimize_line__('12345678901234567890123456789012345678901', 40) + '"'
        "1234567890123456789012345 ... 2345678901"
        """
        if len( text ) <= maxCharacters:
            return text
        ellipsis = len( ' ... ' )
        endLine = 10
        beginLine = maxCharacters - (endLine + ellipsis)
        return text[0:beginLine] + ' ... ' + text[-endLine:]
        
    def __get_additional_page__( self, pageNumber, customer, isFirstPage=False ):
        page = PostscriptPage( pageNumber, self.font, self.fontSize, self.kerning )
        # every page gets these
        page.setTitle( self.title )
        page.setAddress( customer.getAddress() )
        yPos = page.setStatementDate( 'Statement produced: ' + str( self.today ) )
        # Each customer gets only one header message so set that now
        if isFirstPage:
            yPos = page.setHeader( self.header )
        item = customer.getNextItem()
        while len( item ) > 0:
            yPos = page.setItem( item, self.leftMargin, ( yPos - self.blockSpacing ) )
            if page.isRoomForItem( item, yPos ) == False:
                customer.pushItem( item )
                break # we have to make another page to fit it all.
            item = customer.getNextItem()
        return page
        
    def __finalize_notices__( self, customerNotices, isDebug ):
        myFile = open( self.fileBaseName + '.ps', 'w' )
        myFile.write( '%!PS-Adobe-3.0\n' )
        # Tell the PS file how many pages in total there will be
        myFile.write( '%%Pages: ' + str( len( customerNotices ) ) + '\n' )
        myFile.write( '%% Created for Edmonton Public Library ' + str( self.today ) + '\n' )
        WARNING_MSG  = "%% This file contains personal information about customers of Edmonton Public Library\n" 
        WARNING_MSG += "%% This information is protected by EPL's FOIP policy, and must NOT be distributed with expressed\n" 
        WARNING_MSG += "%% permission from the management of EPL.\n"
        myFile.write( WARNING_MSG )
        myFile.write( '%%EndComments\n' )
        myFile.write( '/' + self.font + ' findfont\n' + str( self.fontSize ) + ' scalefont\nsetfont\n' )
        registrationMarkProcedureCall = ''
        if isDebug == True:
            registrationMarkProcedureCall = self.__add_registration_marks__( myFile )
        for page in customerNotices:
            if isDebug == True:
                page.setInstruction( registrationMarkProcedureCall )
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
    formatter.setGlobalHeader( 'Our records indicate that the following amount(s) is outstanding by more than 15 days.  This may block your ability to borrow or to place holds or to renew materials online or via our telephone renewal line. Please go to My Account at http://www.epl.ca/myaccount for full account details.' )
    c = Customer()
    customer = c.__create_customer__()
    formatter.setCustomer( customer )
    formatter.format( True )
