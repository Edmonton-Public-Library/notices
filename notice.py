#!/usr/bin/python

###########################################################################
#
#    Copyright (C) 2023  Andrew Nisbet, Edmonton Public Library
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
from reportreader import Hold, Bill, Overdue, PreReferral, PreLost
from noticeformatter import PostScriptFormatter, PdfFormatter
# Test to see if fonts are available to both Ghostscript and reportlab 
# before adding to this dictionary.
FONTS = {'courier': 'Courier', 'helvetica': 'Helvetica', 'times': 'Times', 'dejavusans': 'DejaVuSans'}
LOCAL_BULLETIN_FOLDER = 'bulletins'
LOCAL_PRINT_FOLDER    = 'print'

def usage():
    message = """
Usage:
    
  notice.py [-b[10]hors] -i <inputfile>
  Processes Symphony reports into printable notice format. Currently 
  notices are created in PostScript (PS) and then converted to PDF.

    -b[n] --dollars=n - Produce bill notices using bill threshold 'n', as an integer
      dollar value, like '10' for $10.00.
    --font='font_name' - Sets a different font for notices. Currently supported:
         Helvetica, Times, Courier, and DejaVuSans.
    -h - Produce hold notices. We don't send these by mail anymore.
    -i --ifile - Argument file shall contain the raw report data to consume.
    -o - Produce overdue report.
    -p - Produce pre-lost report.
    -r - Produce pre-referral report.
    -R - Add registration marks to the files (for debugging formatting).
    -s - Turns the 'isCustomerSuppressionDesired' flag on.
    -P - Output notice as a PDF directly (skip the PS conversion).
    -x - Outputs this usage message.
  
  In this mode customers with malformed mailing addresses are not printed
  since it just costs to print and mail, just to be returned by the post office.
    """
    print(f"{message}")
    
# Take valid command line arguments -b'n', --font='font_name', -h, -i, -o, -p, -P, -r, -R, -s, and -x.
def main(argv):
    inputFile  = ''
    noticeType = 'INIT'
    billLimit  = 10.0
    isCustomerSuppressionDesired = False
    isPdfOutput = False
    configsDict = {}
    configsDict['font'] = 'Courier'
    # configsDict['font'] = 'DejaVuSans'
    debugMode = False
    try:
        opts, args = getopt.getopt(argv, "ohb:f:i:rpPRs", [ "dollars=", "font=", "ifile=" ])
    except getopt.GetoptError:
        usage()
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            noticeType = 'HOLD' # holds.
        elif opt == '-R':
            debugMode = True
        elif opt == '-o':
            # overdues
            noticeType = 'ODUE' # overdues.
        elif opt == '-r':
            # pre-referral; notices that customers are about to be sent to collections.
            noticeType = 'REFR' # pre-referral.
        elif opt in ("-b", "--dollars"): # bills
            billLimit = float(arg)
            noticeType = 'BILL' # bills.
        elif opt in ("-i", "--ifile"):
            inputFile = arg
        elif opt == '-p':
            # pre-lost; notices that charges are old enough to be thought of as LOST and a bill may be in their future.
            noticeType = 'PLOS' # pre-lost.
        elif opt == '-s': # Suppress customers with malformed addresses.
            # suppress malformed customers.
            isCustomerSuppressionDesired = True
        elif opt in ('-P'): # output pdf directly to the provided path.
            isPdfOutput = True
        elif opt in ('-f', '--font'): # Change font in notices. Some care and testing should be used.
            preferredFont = FONTS.get(arg.lower())
            if preferredFont:
                configsDict['font'] = preferredFont
        elif opt == '-x':
            usage()
            sys.exit()
    print(f"Input file is = '{inputFile}'")
    if not os.path.isfile(inputFile) or os.path.getsize(inputFile) == 0:
        sys.stderr.write(f"error: report {inputFile} not specified, doesn't exist, or is empty. Were the report have snail-mail customers?\n")
        sys.exit()
    
    # basic checks done, let's get down to business.
    noticeReader = None
    if noticeType == 'HOLD':
        noticeReader = Hold(inputFile, LOCAL_BULLETIN_FOLDER, LOCAL_PRINT_FOLDER)
    elif noticeType == 'BILL':
        noticeReader = Bill(inputFile, LOCAL_BULLETIN_FOLDER, LOCAL_PRINT_FOLDER, billLimit)
    elif noticeType == 'ODUE':
        noticeReader = Overdue(inputFile, LOCAL_BULLETIN_FOLDER, LOCAL_PRINT_FOLDER)
    elif noticeType == 'REFR':
        noticeReader = PreReferral(inputFile, LOCAL_BULLETIN_FOLDER, LOCAL_PRINT_FOLDER)
    elif noticeType == 'PLOS':
        noticeReader = PreLost(inputFile, LOCAL_BULLETIN_FOLDER, LOCAL_PRINT_FOLDER)
    else:
        sys.stderr.write(f"nothing to do; notice type not selected\n")
        usage()
        sys.exit()
    if not noticeReader:
        usage()
        sys.exit()

    fPrefix = noticeReader.getOutFileBaseName()
    rptDate = noticeReader.getReportDate()
    print(f"TESTING: Report date = {rptDate}")
    if isPdfOutput:
        noticeFormatter = PdfFormatter(fileBaseName=fPrefix, configs=configsDict, reportDate=rptDate, debug=debugMode)
    else:
        noticeFormatter = PostScriptFormatter(fileBaseName=fPrefix, configs=configsDict, reportDate=rptDate, debug=debugMode)
    if not noticeReader.parseReport(isCustomerSuppressionDesired):
        sys.stderr.write(f"*warning, not data parsed from {noticeType}\n")
    else:
        noticeReader.writeToFile(noticeFormatter)
    noticeReader.reportResults()

# Initial entry point for program
if __name__ == "__main__":
    main(sys.argv[1:])
