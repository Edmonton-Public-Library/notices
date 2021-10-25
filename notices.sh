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
export EXCEPTIONS=${LOCAL_DIR}/malformed_addr.txt
# The next line is all the addresses that should be receiving the notices. Make sure it is not commented in production.
EMAIL_ADDRESSES="printednotices@epl.ca,mailclerks@epl.ca,ilsadmins@epl.ca"
# Testing only make sure this is commented out when going to production.
# EMAIL_ADDRESSES="andrew.nisbet@epl.ca"


APP=notice.py
PRINT_DIR=${LOCAL_DIR}/print
REPORT_DIR=${LOCAL_DIR}/reports
BULLETIN_DIR=${LOCAL_DIR}/bulletins
BILLS=${REPORT_DIR}/bills.prn
HOLDS=${REPORT_DIR}/holds.prn
OVERDUES=${REPORT_DIR}/overdues.prn
PREREFERRAL=${REPORT_DIR}/prereferral.prn
VERSION="1.00.02"
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
${LOCAL_BIN_DIR}/report.sh   # get today's reports.
${LOCAL_BIN_DIR}/bulletin.sh # get Notices for today.
logit "DRIVER SCRIPT: compiling bill notices"
python3 ${LOCAL_BIN_DIR}/${APP} -s -b10.0 -i${BILLS}  >>${LOG_FILE}
logit "DRIVER SCRIPT: compiling overdue notices"
python3 ${LOCAL_BIN_DIR}/${APP} -o -s     -i${OVERDUES} >>${LOG_FILE}
logit "DRIVER SCRIPT: compiling pre-referral notices"
python3 ${LOCAL_BIN_DIR}/${APP} -r -s     -i${PREREFERRAL}  >>${LOG_FILE}
${LOCAL_BIN_DIR}/pstopdf.sh
cd ${PRINT_DIR}
for name in $(ls *.pdf)
do
	logit "DRIVER SCRIPT: mailing $name."
	echo "Notice report $name is ready for mailing." | /usr/bin/mailx -a"From:ils@epl-ils.epl.ca" -A ${name} -s "Print Notices `date`" "$EMAIL_ADDRESSES"
done
# Now mail the exceptions list to Vicky and I
#/usr/bin/uuencode $EXCEPTIONS $EXCEPTIONS | /usr/bin/mailx -a'From:ils@epl-ils.epl.ca' -s "Print Notice Address Exceptions `date`" "ilsadmins@epl.ca"
