#!/usr/bin/python
###########################################################################
# Purpose: Format notices from reports into printable format.
# Method:  
# Find the prn report for corresponding bills, holds, or overdues. 
# Remove headers and footers of report (or ignore).
# Split report into chunks by customer boundary.
#   Split customer data into page chunks
#       Add Header with '.read /s/sirsi/Unicorn/Notices/blankmessage'
#       Optionally add additional graphic (HOLDs)
#       Add page item details
#       Add 'Statement 1 of n'
#       Add User name address
#   Format each page into PS and append to file
#
# Author:  Andrew Nisbet, Edmonton Public Library
# Date:    November 7, 2012
# Rev:     
#          0.0 - Dev.
###########################################################################

import sys
import getopt
import os
from notice import Notice # for base class calls.
from notice import Hold
from notice import Bill
from notice import Overdue
from noticeformatter import PostscriptFormatter

def usage():
    print 'Usage:'
    print '  notice.py [-b[10]dh] -i <inputfile> -o <outputfile>'
    print '  Processes Symphony reports into printable notice format'
    
# Take valid command line arguments -b'n', -o, -i, -d, and -h.
def main( argv ):
    inputFile  = ''
    noticeType = 'INIT'
    billLimit  = 10.0
    try:
        opts, args = getopt.getopt( argv, "ohb:i:", [ "dollars=", "ifile=" ] )
    except getopt.GetoptError:
        usage()
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            noticeType = 'HOLD' # holds.
        elif opt == '-o':
            # overdues
            noticeType = 'ODUE' # overdues.
        elif opt in ( "-b", "--dollars" ): # bills
            billLimit = arg 
            noticeType = 'BILL' # bills.
        elif opt in ( "-i", "--ifile" ):
            inputFile = arg
    print 'Input file is = ', inputFile
    if os.path.isfile( inputFile ) == False:
        print 'error: ' + inputFile + ' is empty or does not exist.'
        sys.exit()
    notice = None
    if noticeType == 'HOLD':
        notice = Hold( inputFile )
    elif noticeType == 'BILL':
        notice = Bill( inputFile, billLimit )
    elif noticeType == 'ODUE':
        notice = Overdue( inputFile )
    else:
        print 'nothing to do; notice type not selected'
        usage()
        sys.exit()
    print notice
    # TODO: allow report to be written to an independant directory.
    psFormatter = PostscriptFormatter( notice.getOutFileBaseName() )
    notice.setOutputFormat( psFormatter )
    if notice.parseReport() == False:
        print 'error: unable to parse the report'
        sys.exit()
    notice.writeToFile()

# Initial entry point for program
if __name__ == "__main__":
    main(sys.argv[1:])
