#!/usr/bin/env python 
###########################################################################
#
#    Copyright (C) 2012  Andrew Nisbet, Edmonton Public Library
# The Edmonton Public Library respectfully acknowledges that we sit on
# Treaty 6 territory, traditional lands of First Nations and Metis people.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#
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
#          1.0 - Added licensing changes and pre-referral report processing.
#          0.0 - Dev.
###########################################################################
from datetime import date
from page import PostscriptPage
from page import POINTS
from customer import Customer

SENTINAL = '#PICKUP_LIBRARY#'

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
        self.header          = [] # text string for header
        self.footer          = [] # text strings for footer
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
        totalPageCount  = 1
        for customer in self.customers:
            customerPages = []
            # make the customers initial page - they all have at least one.
            page = self.__get_additional_page__( totalPageCount, customer, True )
            customerPages.append( page )
            totalPageCount += 1
            # but if the page was incomplete, create a new one and keep going until it is complete.
            while( page.isIncomplete ):
                page = self.__get_additional_page__( totalPageCount, customer )
                customerPages.append( page )
                totalPageCount += 1
            # add the statement page of pages notice
            pageTotal           = len( customerPages )
            customersPageNumber = 1
            customersPageCount  = 0
            for page in customerPages:
                # now we know the total pages for a customer we can output the statement count
                page.setStatementCount( 'Statement ' + str( customersPageNumber ) + ' of '+ str( pageTotal ) )
                customersPageNumber += 1
                customersPageCount  += 1
                # place the customer notice onto the list of notices.
                customerNotices.append( page )
            customer.setPageTotal( customersPageCount );
        self.__finalize_notices__( customerNotices, isDebug )
    
    # Creates additional pages of a customer notice.
    # param:  pageNumber - Integer, over-all page number used by PS and PDF to deliniate pages.
    # param:  Customer object - is valid and gets printed notices.
    # param:  isFirstPage - True if the call is for the first page of multi-page customer notice and False otherwise.
    # return: A Page object in valid Postscript.
    def __get_additional_page__( self, pageNumber, customer, isFirstPage=False ):
        page = PostscriptPage( pageNumber, self.font, self.fontSize, self.kerning )
        # every page gets these
        page.setTitle( self.title )
        page.setAddress( customer.getAddress() )
        yPos = page.setStatementDate( 'Statement produced: ' + str( self.today ) ) - self.blockSpacing
        # Each customer gets only one header message so set that now
        if isFirstPage:
            # This code replaces what ever is defined as a sentinal with the customer's pickup library.
            header = []
            if len( customer.header ) > 0:
                for line in self.header:
                    header.append( line.replace( SENTINAL, customer.header ) )
            else:
                header = self.header
            if len( header ) > 0:
                yPos = page.setItem( header, self.leftMargin, yPos ) - self.blockSpacing
        # Output all the items for a customer
        while ( customer.hasMoreItems() ):
            item = customer.getNextItem()
            if page.isRoomForItem( item, yPos ) == False:
                customer.pushItem( item )
                return page # we have to make another page to fit it all.
            yPos = page.setItem( item, self.leftMargin, yPos ) - self.blockSpacing
        # Add any footer the customer has, usually a bill summary.
        if customer.hasFooter():
            item = customer.getFooter()
            if page.isRoomForItem( item, yPos ) == False:
                customer.pushFooter( item )
                return page # we have to make another page to fit it all.
            yPos = page.setItem( item, self.leftMargin, yPos ) - self.blockSpacing
        # Add the page's footer
        if page.isRoomForItem( self.footer, yPos ):
            page.setItem( self.footer, self.leftMargin, yPos ) # This sets the page complete flag.
            page.finalize()
        return page
    
    # Finalizes all the pages into a single PS file.
    # param:  customerNotices - array of pages all notice pages.
    # return: 
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
        # Outline of the page
        myFile.write( '0.5 inch 0  inch moveto\n' )
        myFile.write( '0.5 inch 11 inch lineto\n' )
        myFile.write( '8   inch 0  inch moveto\n' )
        myFile.write( '8   inch 11 inch lineto\n' )
        myFile.write( '0.5 setlinewidth\n' )
        myFile.write( 'perfline\n' )
        # Lowest perferation line
        myFile.write( '0   inch 3.09375 inch moveto\n' )
        myFile.write( '8.5 inch 3.09375 inch lineto\n' )
        myFile.write( '0.25 setlinewidth\n' )
        myFile.write( 'fineperfline\n' )
        # Fold line lower 1/3
        myFile.write( '0   inch 3.5625 inch moveto\n' )
        myFile.write( '8.5 inch 3.5625 inch lineto\n' )
        myFile.write( 'perfline\n' )
        # Fine perforation above fold lower fold line.
        myFile.write( '0   inch 4.09375 inch moveto\n' )
        myFile.write( '8.5 inch 4.09375 inch lineto\n' )
        myFile.write( 'fineperfline\n' )
        # Fine perferation below top fold line.
        myFile.write( '0   inch 6.84375 inch moveto\n' )
        myFile.write( '8.5 inch 6.84375 inch lineto\n' )
        myFile.write( 'fineperfline\n' )
        # Top fold line
        myFile.write( '0   inch 7.275  inch moveto\n' )
        myFile.write( '8.5 inch 7.275  inch lineto\n' )
        myFile.write( 'perfline\n' )
        # Top-most tear line perferation.
        myFile.write( '0   inch 10.4375    inch moveto\n' )
        myFile.write( '8.5 inch 10.4375    inch lineto\n' )
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
        self.header.append( text )
        
    def setGlobalFooter( self, text ):
        self.footer.append( text )

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
    print '=>' + str(customer.getPagesPrinted())
