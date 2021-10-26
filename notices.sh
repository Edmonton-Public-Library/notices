#!/bin/bash
###########################################################################
#
# Driver to coordinate the running of all reports.
#
#    Copyright (C) 2019 - 2021  Andrew Nisbet, Edmonton Public Library
# The Edmonton Public Library respectfully acknowledges that we sit on
# Treaty 6 territory, traditional lands of First Nations and Metis people.
# Collects all the notices required for the day and coordinates convertion to PDF.
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
#
###########################################################################
###
### Edit this file to include new reports.
###
LOCAL_DIR=/home/ils/notices
LOCAL_BIN_DIR=/home/ils/notices/bin
export PATH=$PATH:/usr/bin:/bin:/home/ils/notices/bin
# export PYTHONPATH=/home/ils/notices:/usr/lib/python2.7:/usr/lib/python2.7/plat-linux2:/usr/lib/python2.7/lib-tk:/usr/lib/python2.7/lib-old:/usr/lib/python2.7/lib-dynload:/usr/local/lib/python2.7/dist-packages:/usr/lib/python2.7/dist-packages:/usr/lib/python2.7/dist-packages/gtk-2.0
export PYTHONPATH=${LOCAL_BIN_DIR}
export EXCEPTIONS=${LOCAL_DIR}/unmailable_customers.txt
IS_TEST=false
VERSION="1.01.04"
HOST=$(hostname)

## Set up logging.
LOG_FILE=/home/ils/notices/notices.log
# Logs messages to STDOUT and $LOG_FILE file.
# param:  Message to put in the file.
logit()
{
    local message="$1"
    local time=$(date +"%Y-%m-%d %H:%M:%S")
    if [ -t 0 ]; then
        # If run from an interactive shell message STDOUT and LOG_FILE.
        echo -e "[$time] $message" | tee -a $LOG_FILE
    else
        # If run from cron do write to log.
        echo -e "[$time] $message" >>$LOG_FILE
    fi
}
# Usage message then exits.
# param:  none.
# return: exits with status 99
# Prints out usage message.
usage()
{
    cat << EOFU!
 Usage: $0 [-h -x -t -v]
  Creates the notice reports that are snail-mailed to customers by
  the mail clerks.
   
  Flags:
    -h, -help, --help - prints this help message and exits.
    -t, -test, --test - Run notices in test mode. The script
      runs as normal, but changes \$EMAIL_ADDRESSES and \$ADDR_FIX_STAFF
      to ILS staff instead of the mail clerks.
    -x, -xhelp, --xhelp - prints this help message and exits
	  (default action) from a given date.
             
EOFU!
}
### Check input parameters.
# $@ is all command line parameters passed to the script.
# -o is for short options like -v
# -l is for long options with double dash like --version
# the comma separates different long options
# -a is for long options with single dash like -version
options=$(getopt -l "help,test,version,xhelp" -o "htvx" -a -- "$@")
if [ $? != 0 ] ; then echo "Failed to parse options...exiting." >&2 ; exit 1 ; fi
# set --:
# If no arguments follow this option, then the positional parameters are unset. Otherwise, the positional parameters
# are set to the arguments, even if some of them begin with a ‘-’.
eval set -- "$options"

while true
do
    case $1 in
    -h|--help)
        usage
        exit 0
        ;;
	-t|--test)
        export IS_TEST=true
		logit "=== TEST MODE"
		;;
    -v|--version)
        echo "$0 version: $VERSION"
        exit 0
        ;;
    -x|--xhelp)
        usage
        exit 0
        ;;
    --)
        shift
        break
        ;;
    esac
    shift
done
### Setup globals for the script
if [ "$IS_TEST" == true ]; then
    # Testing only make sure this is commented out when going to production.
    EMAIL_ADDRESSES="andrew.nisbet@epl.ca"
    ADDR_FIX_STAFF="andrew.nisbet@epl.ca"
else
    # The next line is all the addresses that should be receiving the notices. Make sure it is not commented in production.
    EMAIL_ADDRESSES="printednotices@epl.ca,mailclerks@epl.ca,ilsadmins@epl.ca"
    ADDR_FIX_STAFF="ilsadmins@epl.ca"
fi

APP=notice.py
PRINT_DIR=${LOCAL_DIR}/print
REPORT_DIR=${LOCAL_DIR}/reports
BULLETIN_DIR=${LOCAL_DIR}/bulletins
BILLS=${REPORT_DIR}/bills.prn
HOLDS=${REPORT_DIR}/holds.prn
OVERDUES=${REPORT_DIR}/overdues.prn
PREREFERRAL=${REPORT_DIR}/prereferral.prn
################ script starts here ###############
logit "DRIVER SCRIPT: == Starting $0 version: $VERSION on $HOST"
# Clean up any existing reports.
if ! cd ${LOCAL_DIR}; then
	logit "DRIVER SCRIPT: **error, failed to cd into $LOCAL_DIR."
	exit 1
fi
logit "DRIVER SCRIPT: cleaning up old PS files."
rm ${PRINT_DIR}/*.ps
logit "DRIVER SCRIPT: cleaning up old PDF files."
rm ${PRINT_DIR}/*.pdf
logit "DRIVER SCRIPT: cleaning up old PRN files."
rm ${REPORT_DIR}/*.prn
logit "DRIVER SCRIPT: cleaning up bulletin directory."
rm ${BULLETIN_DIR}/*
logit " "
${LOCAL_BIN_DIR}/report.sh   # get today's reports.
logit " "
${LOCAL_BIN_DIR}/bulletin.sh # get Notices for today.
logit "DRIVER SCRIPT: compiling bill notices"
python3 ${LOCAL_BIN_DIR}/${APP} -s -b10.0 -i${BILLS}  >>${LOG_FILE}
logit " "
logit "DRIVER SCRIPT: compiling overdue notices"
python3 ${LOCAL_BIN_DIR}/${APP} -o -s     -i${OVERDUES} >>${LOG_FILE}
logit " "
logit "DRIVER SCRIPT: compiling pre-referral notices"
python3 ${LOCAL_BIN_DIR}/${APP} -r -s     -i${PREREFERRAL}  >>${LOG_FILE}
logit " "
${LOCAL_BIN_DIR}/pstopdf.sh
logit " "
cd ${PRINT_DIR}
RUN_DATE=$(date +'%Y-%m-%d')
for name in $(ls *.pdf)
do
	logit "DRIVER SCRIPT: mailing $name."
    # using echo command makes sure that mailx will not ask you to enter subject and message body manually.
    # When you are using -a option, the mailx program will do all the necessary conversions to base64 and 
    # then to MIME format for you. No need to use uuencode. 
    # https://unix.stackexchange.com/questions/394283/how-to-send-email-attachment-using-mailx-a-with-a-different-attachment-name
	echo | /usr/bin/mailx -a"From:ils@epl-ils.epl.ca" -A ${name} -s "Print Notices $name for $RUN_DATE" "$EMAIL_ADDRESSES"
done
if [ -r "$EXCEPTIONS" ]; then
    # Now mail the exceptions list to someone who can fix the addresses.
    echo | /usr/bin/mailx -a'From:ils@epl-ils.epl.ca' -A ${EXCEPTIONS} -s "Unmailable customers due to broken addresses $RUN_DATE" "$ADDR_FIX_STAFF"
fi
logit "== Notice production complete."
