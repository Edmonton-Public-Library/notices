#!/usr/bin/python

###########################################################################
#
#    Copyright (C) 2022  Andrew Nisbet, Edmonton Public Library
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
# Version: Added 'PreLost Overdue Notice - HTG Print' and 
#          convert 'Overdue Notices - Weekdays' to 
#          'Overdue Reminder - 8 Days Print'
###########################################################################

import sys
import getopt
import os
# from reportreader import Notice # for base class calls.
from reportreader import Hold
from reportreader import Bill
from reportreader import Overdue
from reportreader import PreReferral
from reportreader import PreLost
from noticeformatter import PostscriptFormatter

LOCAL_BULLETIN_FOLDER = 'bulletins'
LOCAL_PRINT_FOLDER    = 'print'

def usage():
    sys.stderr.write( 'Usage:\n' )
    sys.stderr.write( '  notice.py [-b[10]hors] -i <inputfile>\n' )
    sys.stderr.write( '  Processes Symphony reports into printable notice format\n' )
    sys.stderr.write( '  -b[n] - Produce bill notices using bill threshold \'n\', as an integer\n' )
    sys.stderr.write( '  dollar value, like \'10\' for $10.00.\n' )
    sys.stderr.write( '  -h - Produce hold notices. We don\'t send these by mail anymore.\n' )
    sys.stderr.write( '  -i --ifile - Argument file shall contain the raw report data to consume.\n' )
    sys.stderr.write( '  -o - Produce overdue report.\n' )
    sys.stderr.write( '  -p - Produce pre-lost report.\n' )
    sys.stderr.write( '  -r - Produce pre-referral report.\n' )
    sys.stderr.write( '  -s - Turns the \'isCustomerSuppressionDesired\' flag on.\n' )
    sys.stderr.write( '  In this mode customers with malformed mailing addresses are not printed\n' )
    sys.stderr.write( '  since it just costs to print and mail, just to be returned by the post office.\n' )
    
# Take valid command line arguments -b'n', -h, -i, -o, -r, -p, and -s.
def main( argv ):
    inputFile  = ''
    noticeType = 'INIT'
    billLimit  = 10.0
    isCustomerSuppressionDesired = False
    try:
        opts, args = getopt.getopt( argv, "ohb:i:rps", [ "dollars=", "ifile=" ] )
    except getopt.GetoptError:
        usage()
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            noticeType = 'HOLD' # holds.
        elif opt == '-o':
            # overdues
            noticeType = 'ODUE' # overdues.
        elif opt == '-r':
            # pre-referral; notices that customers are about to be sent to collections.
            noticeType = 'REFR' # pre-referral.
        elif opt in ( "-b", "--dollars" ): # bills
            billLimit = float( arg )
            noticeType = 'BILL' # bills.
        elif opt in ( "-i", "--ifile" ):
            inputFile = arg
        elif opt == '-p':
            # pre-lost; notices that charges are old enough to be thought of as LOST and a bill may be in their future.
            noticeType = 'PLOS' # pre-lost.
        elif opt == '-s': # Suppress customers with malformed addresses.
            # suppress malformed customers.
            isCustomerSuppressionDesired = True
    print('Input file is = ', inputFile)
    sys.stderr.write('running file ' + inputFile + '\n')
    if os.path.isfile( inputFile ) == False:
        sys.stderr.write( 'error: input report file ' + inputFile + ' does not exist. Did the report run?\n' )
        sys.exit()
    if os.path.getsize( inputFile ) == 0:
        sys.stderr.write( 'error: input report file ' + inputFile + ' is empty. Did the report run?\n' )
        sys.exit()
    
    # basic checks done, let's get down to business.
    noticeReader = None
    if noticeType == 'HOLD':
        noticeReader = Hold( inputFile, LOCAL_BULLETIN_FOLDER, LOCAL_PRINT_FOLDER )
    elif noticeType == 'BILL':
        noticeReader = Bill( inputFile, LOCAL_BULLETIN_FOLDER, LOCAL_PRINT_FOLDER, billLimit )
    elif noticeType == 'ODUE':
        noticeReader = Overdue( inputFile, LOCAL_BULLETIN_FOLDER, LOCAL_PRINT_FOLDER )
    elif noticeType == 'REFR':
        noticeReader = PreReferral( inputFile, LOCAL_BULLETIN_FOLDER, LOCAL_PRINT_FOLDER )
    elif noticeType == 'PLOS':
        noticeReader = PreLost( inputFile, LOCAL_BULLETIN_FOLDER, LOCAL_PRINT_FOLDER )
    else:
        sys.stderr.write( 'nothing to do; notice type not selected\n' )
        usage()
        sys.exit()
    print(noticeReader)
    psFormatter = PostscriptFormatter( noticeReader.getOutFileBaseName() )
    noticeReader.setOutputFormat( psFormatter )
    if noticeReader.parseReport( isCustomerSuppressionDesired ) == False:
        sys.stderr.write( 'error: unable to parse report\n' )
        sys.exit()
    noticeReader.writeToFile()
    noticeReader.outputReport()

# Initial entry point for program
if __name__ == "__main__":
    main( sys.argv[1:] )
