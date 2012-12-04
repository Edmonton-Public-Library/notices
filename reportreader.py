#!/usr/bin/python
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

LOCAL_NOTICE_FOLDER = 'notices'

class Notice:
    def __init__( self, inFile ):
        self.today            = date.today()
        self.humanDate        = self.today.strftime("%A, %B %d, %Y")
        self.iFileName        = inFile
        self.oFileName        = 'delete_' + str( self.today ) # If we see this file the subclass screwed up.
        self.oFile            = None
        self.statementDate    = 'Statement produced: ' + self.humanDate
        self.formatter        = None
        self.startNoticePath  = '' # path of the open bulletin
        self.endNoticePath    = '' # path of the close bulletin
        # reporting values
        self.pagesPrinted     = 0
        self.noticeCount      = 0  # number of customers notices processed.
        self.incorrectAddress = []  # number of notices that couldn't be printed because customer data was malformed.
        # All the customers to be contacted by this report.
        self.customers        = []
        
    # Reads the report and parses it into customer related notices.
    # Returns number of pages that will be printed.
    def parseReport( self, suppress_malformed_customer=True ):
        return self.pagesPrinted
        
    def setOutputFormat( self, formatter ):
        self.formatter = formatter
        
    def writeToFile( self, debug=False ):
        self.formatter.format()
        
    def getOutFileBaseName( self ):
        return self.oFileName
        
    def __get_lines__( self ):
        # read in the report and parse it.
        iFile = open( self.iFileName, 'r' )
        print 'reading reading reading .... '
        lines = iFile.readlines()
        iFile.close()
        blocks = []
        # reverse the order so we just use 
        lines.reverse()
        return lines
        
    # Adds item text from the report to the customer.
    # param:  the remainder of the lines from the report as a list
    # param:  function to be called. Data dependant.
    def __set_customer_data__( self, lines, customerFunc ):
        while( len( lines ) > 0  ):
            line = lines.pop()
            if line.startswith( '.endblock' ):
                return
            customerFunc( line )
        
    def __str__( self ):
        outstring  = '   report: ' + self.iFileName + '\n'
        return outstring
    
    # Reads a bulletin to be used as a header or footer for a notice.
    # param:  path - path to file (see useLocalFile)
    # param:  useLocalFile - True to use a file in the local directory.
    #         example: /foo/bar.txt with useLocalFile=True will open ./bar.txt, False opens /foo/bar.txt.
    # return: Message from file as a single string.
    def __read_Bulletin__( self, path, useLocalFile=False ):
        newPath = path
        if useLocalFile == True:
            newPath = LOCAL_NOTICE_FOLDER + os.sep + path.split( os.sep )[-1]
        try:
            with open( path, 'r' ) as f:
                bulletin = f.readlines()
                f.close()
                return ''.join( bulletin )
        except IOError as e:
            sys.stderr.write( repr( e ) + ' "' + path + '"' )
            sys.exit( 2 )
        
class Hold( Notice ):
    def __init__( self, inFile ):
        Notice.__init__( self, inFile )
        self.oFileName = 'notices_hold_' + str( self.today ) 
        self.title = 'PICKUP NOTICE'
        
    def __str__( self ):
        return 'Hold Notice using: ' + self.iFileName
        
    # Reads the report and parses it into customer related notices.
    # Returns number of pages that will be printed.
    def parseReport( self, suppress_malformed_customer=True ):
        return False
        
class Overdue( Notice ):
    def __init__( self, inFile ):
        Notice.__init__( self, inFile )
        self.oFileName = 'notices_overdue_' + str( self.today )
        self.title = 'OVERDUE NOTICE'
        
    def __str__( self ):
        return 'Overdue Notice using: ' + self.iFileName
        
    # Reads the report and parses it into customer related notices.
    # Returns number of pages that will be printed.
    def parseReport( self, suppress_malformed_customer=True ):
        return False
        
class Bill( Notice ):
    def __init__( self, inFile, billLimit=10.0 ):
        Notice.__init__( self, inFile )
        self.oFileName        = 'notices_bills_' + str( self.today )
        self.minimumBillValue = billLimit
        self.title            = 'NEW BILLINGS'
        
    def __str__( self ):
        return 'Bill Notice using: ' + self.iFileName + '\nminimum bill value = ' + str( self.minimumBillValue )
        
    # Reads the report and parses it into customer related notices.
    # Returns number of pages that will be printed.
    def parseReport( self, suppress_malformed_customer=True ):
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
                print 'opening message and customer items'
                isItemsBlocks = True
                self.startNoticePath = line.split()[1]
            elif line.startswith( '.block' ):
                line = lines.pop()
                if line.startswith( '.read' ): # closing message and end of customer.
                    print 'found end message and end of customer'
                    # get the message and pass it to the noticeFormatter.
                    self.endNoticePath = line.split()[1]
                    self.customers.append( customer )
                    customer = Customer()
                    isItemsBlocks = False
                    # break
                elif line.find( '=====' ) > 0: # summary block.
                    print 'found summary'
                    customer.setSummaryText( line )
                    self.__set_customer_data__( lines, customer.setSummaryText )
                elif isItemsBlocks == True:
                    customer.setItemText( line )
                    self.__set_customer_data__( lines, customer.setItemText )
                else:
                    customer.setAddressText( line )
                    self.__set_customer_data__( lines, customer.setAddressText )
            elif line.startswith( '.email' ):
                customer.setEmail( line )
            # ignore everything else it's just dross.
        # for testing print out the customers and what you have set.
        print self.customers[0]
        return True
        
    def writeToFile( self, debug=False ):
        # get the formatter to set up the postscript
        formatter = PostscriptFormatter( self.oFileName )
        # Title
        formatter.setGlobalTitle( self.title )
        # read the opening bulletin
        boilerPlateHeaderText = self.__read_Bulletin__( self.startNoticePath )
        formatter.setGlobalHeader( boilerPlateHeaderText )
        # read the closing bulletin
        boilerPlateFooterText = self.__read_Bulletin__( self.endNoticePath )
        formatter.setGlobalFooter( boilerPlateFooterText )
        for customer in self.customers:
            formatter.setCustomer( customer )
        formatter.format( debug )
            
# Initial entry point for program
if __name__ == "__main__":
    import doctest
    doctest.testmod()