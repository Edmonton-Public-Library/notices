#!/usr/bin/env python
###########################################################################
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
# from reportreader import Notice # for base class calls.
from reportreader import Hold
from reportreader import Bill
from reportreader import Overdue
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
        sys.stderr.write( 'error: input report file ' + inputFile + ' does not exist. Did the report run?' )
        sys.exit()
    if os.path.getsize( inputFile ) == 0:
        sys.stderr.write( 'error: input report file ' + inputFile + ' is empty. Did the report run?' )
        sys.exit()
    
    # basic checks done, let's get down to business.
    noticeReader = None
    if noticeType == 'HOLD':
        noticeReader = Hold( inputFile )
    elif noticeType == 'BILL':
        noticeReader = Bill( inputFile, billLimit )
    elif noticeType == 'ODUE':
        noticeReader = Overdue( inputFile )
    else:
        sys.stderr.write( 'nothing to do; notice type not selected' )
        usage()
        sys.exit()
    print noticeReader
    psFormatter = PostscriptFormatter( noticeReader.getOutFileBaseName() )
    noticeReader.setOutputFormat( psFormatter )
    if noticeReader.parseReport() == False:
        sys.stderr.write( 'error: unable to parse the report' )
        sys.exit()
    noticeReader.writeToFile()

# Initial entry point for program
if __name__ == "__main__":
    main( sys.argv[1:] )
