#!/usr/bin/env python
###########################################################################
#
# Purpose: Notice object definition, from which sub-classes such as
# pre-referral, and bill notices can be generated.
#
#    Copyright (C) 2012 - 2023 Andrew Nisbet, Edmonton Public Library
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
# Author:  Andrew Nisbet, Edmonton Public Library
# Date:    November 7, 2012
# Version: Added 'PreLost Overdue Notice - HTG Print' and 
#          convert 'Overdue Notices - Weekdays' to 
#          'Overdue Reminder - 8 Days Print'
###########################################################################

import os  # for os specific file bulletin reading.
import sys # for exit
from customer import Customer
from datetime import date
from noticeformatter import NoticeFormatter
import re

## Global name of the file that contains broken snail-mail addresses.
UNMAILABLE_REPORT_FILE = 'unmailable_customers.txt'
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

############## Base Class ####################
class Notice:
    def __init__( self, inFile, bulletinDir, printDir, outFilePrefix ):
        self.today            = date.today()
        self.reportDate       = ''
        self.iFileName        = inFile
        self.oFileName        = printDir + os.sep + outFilePrefix + str( self.today ) # If we see this file the subclass screwed up.
        self.bulletinDir      = bulletinDir # path of the open bulletin
        self.printDir         = printDir
        self.startNoticePath  = ''
        self.endNoticePath    = ''
        # All the customers to be contacted by this report.
        self.customers        = []
        self.pagesPrinted     = 0
        self.customersWithBadAddress = []

    def getReportDate(self):
        return self.reportDate

    # Prints out key information about the running report such as total pages printed
    # number of customers mailed and outputs a list of customers that need to have
    # street addresses corrected.
    # param:
    # return:
    def reportResults( self ):
        dateToday = self.today.strftime("%A, %B %d, %Y")
        print(f"========= {dateToday}")
        print(f"notice: {self.iFileName} report date: {self.reportDate}")
        # output the results
        print('total pages printed: %d' % self.pagesPrinted)
        print('customers mailed:    %d' % len( self.customers ))
        print('bad addresses:       %d' % len( self.customersWithBadAddress ))
        if len( self.customersWithBadAddress ) == 0:
            return
        f = open( UNMAILABLE_REPORT_FILE, 'w' )
        for c in self.customersWithBadAddress:
            f.write( str( c ) )
        f.close()

    # Reads the report and parses it into customer related notices.
    # Returns number of pages that will be printed.
    def parseReport( self, suppress_malformed_customer=True ):
        return self.pagesPrinted

    def writeToFile( self, formatter:NoticeFormatter, debug=False ):
        # Title
        formatter.setGlobalTitle( self.title )
        # read the opening bulletin
        self.__read_Bulletin__( self.startNoticePath, formatter.setGlobalHeader )
        # read the closing bulletin
        self.__read_Bulletin__( self.endNoticePath, formatter.setGlobalFooter )
        self.totalCustomers   = len( self.customers )
        for customer in self.customers:
            formatter.setCustomer( customer )
        formatter.format( debug )
        formatter.outputNotices()
        # after formatting we collect pages printed.
        for customer in self.customers:
            self.pagesPrinted += customer.getPagesPrinted()

    # Returns the base path and name of the final output file 
    # For example; /foo/bar for /foo/bar.ps or /foo/bar.pdf. 
    def getOutFileBaseName( self ):
        return self.oFileName

    # Takes a string, determines if it matches a long date and returns it.
    # Symphony uses two types of date strings in reports; 
    # $<wednesday:u>, $<april:u> 13, 2022
    # and 
    # Friday, December 7, 2012
    # param: report line string.
    # return: the cleaned date from the string or None of the string doesn't have a long date.
    def __get_report_date__(self, rpt_lines:list) ->str:
        for line in rpt_lines:
            if len(line.split(', ')) == 3:
                for day in DAYS:
                    if day in line.lower():
                        line = re.sub(r'(\$<)', "", line)
                        return re.sub(r'(:u>)', "", line).title().rstrip()
        print(f"I get called but don't find anything in this report!")
        return ''

    def __get_lines__( self ):
        # read in the report and parse it.
        iFile = open( self.iFileName, 'r' )
        # print 'reading reading reading .... '
        lines = iFile.readlines()
        iFile.close()
        self.reportDate = self.__get_report_date__(lines)
        # reverse the order so we just use
        lines.reverse()
        return lines

    # Adds item text from the report to the customer.
    # param:  the remainder of the lines from the report as a list
    # param:  function to be called. Data dependant.
    # param:  the rtf tag that terminates data collection, usually an '.endblock'.
    # param:  ignoreFirstEndBlock - if set to true the first endBlockTag specified above is ignored This
    #         is used to handle nested rtf tags.
    def __set_customer_data__( self, lines, customerFunc, endBlockTag, ignoreFirstEndblock=False ):
        haveSeenFirstEndblock = False
        while( len( lines ) > 0  ):
            line = lines.pop()
            if line.startswith( '.read' ): # There may be another .read tag inside the customer block; it's the footer.
                self.endNoticePath = line.split()[1]
                continue
            if line.startswith( endBlockTag ):
                if ignoreFirstEndblock:
                    if haveSeenFirstEndblock == True:
                        return
                    haveSeenFirstEndblock = True
                    continue
                else:
                    return
            customerFunc( line )

    def __str__( self ):
        custs = [str(x) for x in self.customers]
        return f"{type(self).__name__} Notice using: {self.iFileName}\n{custs}"

    # Reads a bulletin, or Notice, to be used as a header or footer for a notice.
    # param:  path - path to file. Looks in the local bulletin directory.
    # return: Message from file as a single string.
    def __read_Bulletin__( self, path, func ):
        if len( path ) == 0: # This happens if there is no footertext mentioned in the report.
            return ''
        newPath = self.bulletinDir + os.sep + path.split( os.sep )[-1]
        try:
            with open( newPath, 'r' ) as f:
                for line in f.readlines():
                    func( line )
                f.close()

        except IOError:
            sys.stderr.write( 'error: failed to find Notice file: "' + newPath + '".' )
            sys.exit( 2 )

############## Holds ####################
class Hold( Notice ):
    def __init__( self, inFile, bulletinDir, printDir ):
        Notice.__init__( self, inFile, bulletinDir, printDir, 'print_holds_' )
        self.title = 'PICKUP NOTICE'

    # Reads the report and parses it into customer related notices.
    # Returns number of pages that will be printed.
    def parseReport( self, suppress_malformed_customer=False ):
        # .folddata
        # .report
        # .language ENGLISH
        # .col 5l,1,73
        # Friday, December 7, 2012
        # .block
        # Whitemud Crossing Branch
        # .endblock
        # .block
                  # Georgia I Grant
                  # 11227 58 Avenue
                  # Edmonton, AB
                  # T6H 1C3
        # .endblock
        # .read /s/sirsi/Unicorn/Notices/1stpickup
        # .block
        # .block
          # 1   Holiday crafts.
        # .endblock
              # $<call_num:3>745.5941 HOL 2004                           $<copy:3>1
                # $<pickup_by:3>1/20/2013
        # .endblock
        # .block
        # .block
          # 2   Holiday crafts.
        # .endblock
              # $<call_num:3>745.5941 HOL 2005                           $<copy:3>2
                # $<pickup_by:3>1/20/2013
        # .endblock
        # .block
        # .block
          # 3   Holiday crafts.
        # .endblock
              # $<call_num:3>745.5941 HOL 2006                           $<copy:3>2
                # $<pickup_by:3>1/20/2013
        # .endblock
        # .block
        # .block
          # 4   Holiday crafts.
        # .endblock
              # $<call_num:3>745.5941 HOL 2008                           $<copy:3>1
                # $<pickup_by:3>1/20/2013
        # .endblock
        # .report
        # ...
        #
        lines = self.__get_lines__()
        # now pop off each line from the file and form it into a block of data
        customer         = None
        hasEmail         = False
        isPickupLocation = False
        isAddress        = False
        while( len( lines ) > 0 ):
            line = lines.pop()
            if line.startswith( '.read' ): # message read instruction not in block. Thanks Sirsi.
                # print 'opening message and customer items'
                isItemsBlocks = True
                self.startNoticePath = line.split()[1]
                # print self.startNoticePath
            elif line.startswith( '.block' ):
                line = lines.pop()
                if isAddress:
                    customer.setAddressText( line )
                    self.__set_customer_data__( lines, customer.setAddressText, '.endblock' )
                    isAddress   = False
                    isItemBlock = True
                elif isPickupLocation:
                    customer.setHeader( line )
                    isPickupLocation = False
                    isAddress        = True
                elif isItemsBlocks:
                    self.__set_customer_data__( lines, customer.setItemText, '.endblock', True )
            elif line.startswith( '.report' ):
                if customer != None and hasEmail == False:
                    if not customer.isWellFormed() and suppress_malformed_customer:
                        pass
                    else:
                        self.customers.append( customer )
                customer = Customer()
                isPickupLocation = True
                isItemsBlocks    = False
                hasEmail         = False
            elif line.startswith( '.email' ):
                # this customer doesn't get added because they have an email.
                hasEmail = True
                customer.setEmail( line )
        # print self.customers[0]
        return len(self.customers) > 0

############## Overdue Reminder #################### 
class Overdue( Notice ):
    def __init__( self, inFile, bulletinDir, printDir ):
        Notice.__init__( self, inFile, bulletinDir, printDir, 'print_overdues_' )
        self.title = 'OVERDUE REMINDER'

    # Reads the report and parses it into customer related notices.
    # Returns number of pages that will be printed.
    def parseReport( self, suppress_malformed_customer=False ):
        #######################
        ## OLD NOTICE
        # .folddata
        # .report
        # .col 5l,1,73
        # .language ENGLISH
        # $<wednesday:u>, $<august:u> 1, 2018
        # <blank lines>
        # .block
                  # Mary Madeleine Bennett
                  # 1162 Rutherford Close SW
                  # Edmonton AB
                  # T6W 1H6
        # .endblock
        # <blank lines>
        # .read /s/sirsi/Unicorn/Notices/1stoverdue.print
        # <blank lines>
          # 1  $<call_num:3>CD WOO                                    $<id:3U>312211045160                                                                                            62
             # Bellwether revivals [sound recording] / Benjamin Wood.
             # Wood, Benjamin, 1981-
             # $<due:3>7/17/2018,23:59
             # <blank lines>
        # .read /s/sirsi/Unicorn/Notices/eplmailclosing
        ## END OLD OVERDUE NOTICE
        #########################
        ## NEW OVERDUE REMINDER NOTICE (kxri.prn)
        # .folddata
        # .report
        # .col 5l,1,73
        # .language ENGLISH
        # $<wednesday:u>, $<april:u> 13, 2022
        # <blank lines>
        # .block
        #           Arbry Adult
        #           1234 5678 Saskatchewan DR NW
        #           Edmonton, AB
        #           T6T 4R7
        # .endblock
        # <blank lines>
        # .read /software/EDPL/Unicorn/Notices/overdue8daysprint
        # <blank lines>
        #   1  $<call_num:3>927.8242 JON                              $<id:3U>31221317743289  
        #      Last chance Texaco : chronicles of an American troubadour / Rickie Lee
        #      Jones.
        #      Jones, Rickie Lee.
        #      $<due:3>4/5/2022,23:59  
        # <blank lines>
        # .read /software/EDPL/Unicorn/Notices/eclosing8daysprint
        ## End OVERDUE REMINDER prn data.

        lines = self.__get_lines__()
        # now pop off each line from the file and form it into a block of data
        customer         = Customer()
        hasEmail         = False
        isPickupLocation = False
        isAddress        = False
        readTagsPerCustomer = 2
        while( len( lines ) > 0 ):
            line = lines.pop()
            if line.startswith( '.read' ): # message read instruction not in block.
                # print 'opening message and customer items'
                self.startNoticePath = line.split()[1]
                # The rest of the text until the next .report tag is items for the customer
                self.__set_customer_data__( lines, customer.setItemText, '.report' )
                if hasEmail == False:
                    if not customer.isWellFormed() and suppress_malformed_customer:
                        pass
                    else:
                        self.customers.append( customer )
                hasEmail = False
                customer = Customer()
            elif line.startswith( '.block' ):
                self.__set_customer_data__( lines, customer.setAddressText, '.endblock' )
            elif line.startswith( '.email' ):
                # this customer doesn't get added because they have an email.
                hasEmail = True
                customer.setEmail( line )
        return True

############## Bills ####################
class Bill( Notice ):
    def __init__( self, inFile, bulletinDir, printDir, billLimit=10.0 ):
        Notice.__init__( self, inFile, bulletinDir, printDir, 'print_bills_' )
        self.minimumBillValue = billLimit
        self.title            = 'NEW BILLINGS' # we set this since the report doesn't have it explicitely.

    # Reads the report and parses it into customer related notices.
    # Returns number of pages that will be printed.
    def parseReport( self, suppressMalformedCustomer=False ):
        # .report
        # .col 5l,1,73
        # .language ENGLISH
        # $<wednesday:u>, $<may:u> 31, 2023

        # .block
        #         Booker Tunerville
        #         JOELLE Tunerville-Bontemp
        #         13990 162 A Avenue NW
        #         Edmonton, AB
        #         T6V 1W1
        # .endblock

        # .read /software/EDPL/Unicorn/Notices/blankmessage

        # .block
        # 1   Back to the past / by Cigdem Knebel.
        #     Knebel, Cigdem.
        #     $<date_billed:3>5/16/2023    $<bill_reason:3>LOST         $<amt_due:3>    $22.24
        # .endblock

        # .block
        #     =======================================================================

        #                                 $<total_fines_bills:3>    $22.24
        # .endblock

        # .block
        # .read /software/EDPL/Unicorn/Notices/eclosing
        # .endblock
        # read in the report and parse it.
        lines = self.__get_lines__()
        # now pop off each line from the file and form it into a block of data
        customer = Customer()
        isItemsBlocks = False
        while( len( lines ) > 0 ):
            line = lines.pop()
            if line.startswith( '.read' ): # message read instruction not in block. Thanks Sirsi.
                # print 'opening message and customer items'
                isItemsBlocks = True
                self.startNoticePath = line.split()[1]
            elif line.startswith( '.block' ):
                line = lines.pop()
                if line.startswith( '.read' ): # closing message and end of customer.
                    # print 'found end message and end of customer'
                    # get the message and pass it to the noticeFormatter.
                    self.endNoticePath = line.split()[1]
                    # Test if the customer should even receive mailed notices.
                    if customer.isWellFormed() == False:
                        # save these to report to staff for corrective action.
                        self.customersWithBadAddress.append( customer )
                    if customer.getsPrintedNotices() and customer.getTotalBills() >= self.minimumBillValue:
                        if customer.isWellFormed():
                            self.customers.append( customer )
                        # The customer has a bad postal code but do we care? Can we mail it anyway?
                        elif suppressMalformedCustomer == False:
                            self.customers.append( customer )
                    customer = Customer()
                    isItemsBlocks = False
                    # break
                elif line.find( '=====' ) > 0: # summary block.
                    # print 'found summary'
                    customer.setSummaryText( line )
                    self.__set_customer_data__( lines, customer.setSummaryText, '.endblock' )
                elif isItemsBlocks == True:
                    customer.setItemText( line )
                    self.__set_customer_data__( lines, customer.setItemText, '.endblock' )
                else:
                    customer.setAddressText( line )
                    self.__set_customer_data__( lines, customer.setAddressText, '.endblock' )
            elif line.startswith( '.email' ):
                customer.setEmail( line )
            # ignore everything else it's just dross.
        return True

############## PreReferral ####################
class PreReferral( Notice ):
    def __init__( self, inFile, bulletinDir, printDir ):
        Notice.__init__( self, inFile, bulletinDir, printDir, 'print_prereferral_' )
        self.title = 'PRE-REFERRAL NOTICE' # PreReferral Bill notice for mailing.

    # Reads the report and parses it into customer related notices.
    # Returns number of pages that will be printed.
    def parseReport( self, suppressMalformedCustomer=False ):
        # .folddata
        # .report
        # .email jackyo@gmail.com
        # .col 5l,1,73
        # .language ENGLISH
        # Tuesday, August 22, 2017
        # .block
        # Jacqueline Onasis
        # 403-12345 Saskatchewan Drive NW
        # Edmonton, AB
        # T6E 4R9
        # .endblock
        # .read /s/sirsi/Unicorn/Notices/blankmessage
        # .block
        # 1   Vikings. Season 4, Volume 1 [videorecording].
        # Fimmel, Travis, 1979-
        # date billed:8/8/2017     bill reason:OVERDUE      amount due:     $5.00
        # .endblock
        # .block
        # 2   Outlander. Season two [videorecording].
        # Balfe, Caitriona.
        # date billed:8/8/2017     bill reason:OVERDUE      amount due:     $5.00
        # .endblock
        # .block
        # =======================================================================
        # TOTAL FINES/FEES AND UNPAID BILLS:    $10.00
        # .endblock
        # .block
        # .read /s/sirsi/Unicorn/Notices/prereferralbillclosing
        # .endblock
        # .endemail
        # .report
        # .col 5l,1,73
        # .language ENGLISH
        # Tuesday, August 22, 2017
        # .block
        # Some customer
        # SOME CUSTOMER'S        PRESTON
        # 25-1655 49 Street NW
        # Edmonton, AB
        # T6L 2R8
        # .endblock
        # .read /s/sirsi/Unicorn/Notices/blankmessage
        # .block
        # 1   Grammy nominees. 2015 [sound recording].
        # date billed:8/8/2017     bill reason:LOST         amount due:    $24.49
        # .endblock
        # .block
        # 2   Big Hero 6 [videorecording] / directors, Don Hall, Chris Williams.
        # Hall, Don.
        # date billed:8/8/2017     bill reason:LOST         amount due:    $30.49
        # .endblock
        # .block
        # 3   Tony Hawk's pro skater 5 [game] / Robomodo.
        # Hawk, Tony.
        # date billed:8/8/2017     bill reason:LOST         amount due:    $55.99
        # .endblock
        # .block
        # 4   Grammy nominees. 2017 [sound recording].
        # date billed:8/8/2017     bill reason:LOST         amount due:    $22.24
        # .endblock
        # .block
        # =======================================================================
        # TOTAL FINES/FEES AND UNPAID BILLS:   $133.21
        # .endblock
        # .block
        # .read /s/sirsi/Unicorn/Notices/prereferralbillclosing
        # .endblock
        # ...
        lines = self.__get_lines__()
        # now pop off each line from the file and form it into a block of data
        customer = Customer()
        isItemsBlocks = False
        while( len( lines ) > 0 ):
            line = lines.pop()
            if line.startswith( '.read' ): # message read instruction not in block. Thanks Sirsi.
                # print 'opening message and customer items'
                isItemsBlocks = True
                self.startNoticePath = line.split()[1]
            elif line.startswith( '.block' ):
                line = lines.pop()
                if line.startswith( '.read' ): # closing message and end of customer.
                    # print 'found end message and end of customer'
                    # get the message and pass it to the noticeFormatter.
                    self.endNoticePath = line.split()[1]
                    # Test if the customer can even be emailed notices.
                    if customer.isWellFormed() == False:
                        # save these to report to staff for corrective action.
                        self.customersWithBadAddress.append( customer )
                    # All customers get pre-referal notices snail-mailed to them 
                    # to ensure there are mix-ups April 30, 2018.
                    if customer.isWellFormed():
                        self.customers.append( customer )
                        # The customer has a bad postal code but do we care? Can we mail it anyway?
                    elif suppressMalformedCustomer == False:
                        self.customers.append( customer )
                    customer = Customer()
                    isItemsBlocks = False
                    # break
                elif line.find( '=====' ) > 0: # summary block.
                    # print 'found summary'
                    customer.setSummaryText( line )
                    self.__set_customer_data__( lines, customer.setSummaryText, '.endblock' )
                elif isItemsBlocks == True:
                    customer.setItemText( line )
                    self.__set_customer_data__( lines, customer.setItemText, '.endblock' )
                else:
                    customer.setAddressText( line )
                    self.__set_customer_data__( lines, customer.setAddressText, '.endblock' )
            elif line.startswith( '.email' ):
                customer.setEmail( line )
            # ignore everything else it's just dross.
        return True

############## Pre-Lost #################### 
class PreLost( Notice ):
    def __init__( self, inFile, bulletinDir, printDir ):
        Notice.__init__( self, inFile, bulletinDir, printDir, 'print_prelost_' )
        # Report name change as requested by staff April 27, 2022. Was PRE-LOST NOTICE.
        self.title = 'OVERDUE NOTICE'

    # Reads the report and parses it into customer related notices.
    # Returns number of pages that will be printed.
    def parseReport( self, suppress_malformed_customer=False ):
        ## PRE-LOST OVERDUE REMINDER NOTICE (kxrk.prn)
        # .folddata
        # .report
        # .col 5l,1,73
        # .language ENGLISH
        # $<wednesday:u>, $<april:u> 13, 2022
        # <blank lines>
        # .block
        #           Arbry Adult
        #           1234 5678 Saskatchewan DR NW
        #           Edmonton, AB
        #           T6T 4R7
        # .endblock
        # <blank lines>
        # .read /software/EDPL/Unicorn/Notices/prelostoverdue1stprint
        # <blank lines>
        # 1  $<call_num:3>OSM                                       $<id:3U>31221317323405  
        #      The Thursday murder club / Richard Osman.
        #      Osman, Richard, 1970-
        #      $<due:3>4/5/2022,23:59      $<price:3>$28.65    
        # <blank lines>
        # .read /software/EDPL/Unicorn/Notices/prelostoverdueclosingprint
        ## PRE-LOST OVERDUE REMINDER NOTICE (kxrk.prn)

        lines = self.__get_lines__()
        # now pop off each line from the file and form it into a block of data
        customer         = Customer()
        hasEmail         = False
        isPickupLocation = False
        isAddress        = False
        readTagsPerCustomer = 2
        while( len( lines ) > 0 ):
            line = lines.pop()
            if line.startswith( '.read' ): # message read instruction not in block.
                # print 'opening message and customer items'
                self.startNoticePath = line.split()[1]
                # The rest of the text until the next .report tag is items for the customer
                self.__set_customer_data__( lines, customer.setItemText, '.report' )
                if hasEmail == False:
                    if not customer.isWellFormed() and suppress_malformed_customer:
                        pass
                    else:
                        self.customers.append( customer )
                hasEmail = False
                customer = Customer()
            elif line.startswith( '.block' ):
                self.__set_customer_data__( lines, customer.setAddressText, '.endblock' )
            elif line.startswith( '.email' ):
                # this customer doesn't get added because they have an email.
                hasEmail = True
                customer.setEmail( line )
        return True

# Initial entry point for program
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("reportreader.tst")
