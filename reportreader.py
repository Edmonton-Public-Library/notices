#!/usr/bin/env python
###########################################################################
# Purpose: Notice object.
#
# Author:  Andrew Nisbet, Edmonton Public Library
# Date:    November 7, 2012
# Rev:     
#          0.0 - Dev.
###########################################################################

import os  # for os specific file bulletin reading.
import sys # for exit
from customer import Customer
from datetime import date
from noticeformatter import PostscriptFormatter

############## Base Class ####################
class Notice:
    def __init__( self, inFile, bulletinDir, printDir, outFilePrefix ):
        self.today            = date.today()
        self.humanDate        = self.today.strftime("%A, %B %d, %Y")
        self.iFileName        = inFile
        self.oFileName        = printDir + os.sep + outFilePrefix + str( self.today ) # If we see this file the subclass screwed up.
        self.statementDate    = 'Statement produced: ' + self.humanDate
        self.bulletinDir      = bulletinDir # path of the open bulletin  
        self.printDir         = printDir
        self.startNoticePath  = ''
        self.endNoticePath    = ''
        # All the customers to be contacted by this report.
        self.customers        = []
        self.pagesPrinted     = 0
        self.customersWithBadAddress = []
    
    # Prints out key information about the running report such as total pages printed
    # number of customers mailed and outputs a list of customers that need to have 
    # street addresses corrected.
    # param:  
    # return:
    def outputReport( self ):
        print '========='
        print 'notice report for ' + self.iFileName + ' for ' + self.humanDate
        # output the results
        print 'total pages printed: %d' % self.pagesPrinted
        print 'customers mailed:    %d' % len( self.customers )
        print 'bad addresses:       %d' % len( self.customersWithBadAddress )
        if len( self.customersWithBadAddress ) == 0:
            return
        # f = open( 'malformed_addr.lst', 'w+' )
        f = open( 'malformed_addr.lst', 'w' )  # for testing clobber the old list.
        for c in self.customersWithBadAddress:
            f.write( str( c ) )
        f.close()  
        
    # Reads the report and parses it into customer related notices.
    # Returns number of pages that will be printed.
    def parseReport( self, suppress_malformed_customer=True ):
        return self.pagesPrinted
        
    def setOutputFormat( self, formatter ):
        self.formatter = formatter
        
    def writeToFile( self, debug=False ):
        # get the formatter to set up the postscript
        formatter = PostscriptFormatter( self.oFileName )
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
        # after formatting we collect pages printed.
        for customer in self.customers:
            self.pagesPrinted += customer.getPagesPrinted()
    
    def getOutFileBaseName( self ):
        return self.oFileName
        
    def __get_lines__( self ):
        # read in the report and parse it.
        iFile = open( self.iFileName, 'r' )
        # print 'reading reading reading .... '
        lines = iFile.readlines()
        iFile.close()
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
        outstring  = '   report: ' + self.iFileName + '\n'
        return outstring
    
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
        
    def __str__( self ):
        return 'Hold Notice using: ' + self.iFileName
        
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
                    isAddress = False
                    isItemBlock = True
                elif isPickupLocation:
                    customer.setHeader( line )
                    isPickupLocation = False
                    isAddress = True
                elif isItemsBlocks:
                    self.__set_customer_data__( lines, customer.setItemText, '.endblock', True )
            elif line.startswith( '.report' ):
                if customer != None and hasEmail == False:
                    if not customer.isWellFormed() and suppress_malformed_customer:
                        pass
                    else:
                        self.customers.append( customer )
                    hasEmail = False
                customer = Customer()
                isPickupLocation = True
                isItemsBlocks = False
            elif line.startswith( '.email' ):
                # this customer doesn't get added because they have an email.
                hasEmail = True
                customer.setEmail( line )
        # print self.customers[0]
        return True

############## Overdues ####################
class Overdue( Notice ):
    def __init__( self, inFile, bulletinDir, printDir ):
        Notice.__init__( self, inFile, bulletinDir, printDir, 'print_overdues_' )
        self.title = 'OVERDUE NOTICE'
        
    def __str__( self ):
        return 'Overdue Notice using: ' + self.iFileName
        
    # Reads the report and parses it into customer related notices.
    # Returns number of pages that will be printed.
    def parseReport( self, suppress_malformed_customer=False ):
        # .folddata
        # .report
        # .col 5l,1,73
        # .language ENGLISH
        # Friday, December 7, 2012
        # .block
                  # Gerald Haekel
                  # 3528 108 Street
                  # Edmonton, AB
                  # T6J 1B4
        # .endblock
        # .read /s/sirsi/Unicorn/Notices/1stoverdue
          # 1  call number:PERIODICAL                                ID:31221091576145  
             # ADULT PERIODICAL
             # due:11/22/2012,23:59
        # .report
        lines = self.__get_lines__()
        # now pop off each line from the file and form it into a block of data
        customer         = Customer()
        hasEmail         = False
        isPickupLocation = False
        isAddress        = False
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
        
    def __str__( self ):
        return 'Bill Notice using: ' + self.iFileName + '\nminimum bill value = ' + str( self.minimumBillValue )
        
    # Reads the report and parses it into customer related notices.
    # Returns number of pages that will be printed.
    def parseReport( self, suppressMalformedCustomer=False ):
        # .block
        # Luckie Luke
        # 12345 120 Street
        # Edmonton, AB
        # T5X 5N8
        # .endblock
        # .read /s/sirsi/Unicorn/Notices/blankmessage
        # .block
        # 1   A woman betrayed / Barbara Delinsky.
        # Delinsky, Barbara.
        # $<date_billed:3>10/23/2012   $<bill_reason:3>OVERDUE      $<amt_due:3>     $0.75
        # .endblock
        # .block
        # 2   Jump! / Jilly Cooper.
        # Cooper, Jilly.
        # $<date_billed:3>10/23/2012   $<bill_reason:3>OVERDUE      $<amt_due:3>     $0.75
        # .endblock
        # .block
        # 3   A perfect proposal / Katie Fforde.
        # Fforde, Katie.
        # $<date_billed:3>10/23/2012   $<bill_reason:3>OVERDUE      $<amt_due:3>     $0.75
        # .endblock
        # .block
        # 4   Looking for Peyton Place : a novel / Barbara Delinsky.
        # Delinsky, Barbara.
        # $<date_billed:3>10/23/2012   $<bill_reason:3>OVERDUE      $<amt_due:3>     $0.75
        # .endblock
        # .block
        # =======================================================================
        #
        #                    $<total_fines_bills:3>     $3.00
        # .endblock
        # .block
        # .read /s/sirsi/Unicorn/Notices/eclosing
        # .endblock
        # read in the report and parse it.
        # TODO - add the rest of the blocks to capture customer data
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
        # for testing print out the customers and what you have set.
        # print self.customers[0]
        return True
            
# Initial entry point for program
if __name__ == "__main__":
    import doctest
    doctest.testmod()