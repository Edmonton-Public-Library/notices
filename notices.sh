#!/bin/bash
###########################################################################
#
# Driver to coordinate the running of all reports.
#
#    Copyright (C) 2019  Andrew Nisbet, Edmonton Public Library
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
# Rev:     
#          2.0 - Updated driver to use python3.
#          1.1 - Added new address for mail clerks to get rid of public folders
#                'printednotices@epl.ca'
#          1.0 - Added licensing changes and pre-referral report processing.
#          0.0 - Dev.
#
###########################################################################
###
### Edit this file to include new reports.
###
export HOME=/home/ilsdev
export LOGNAME=ilsdev
export PATH=$PATH:/usr/bin:/bin:/home/ilsdev/projects/notices
export LANG=en_US.UTF-8
export SHELL=/bin/sh
export PWD=/home/ilsdev
# export PYTHONPATH=/home/ilsdev/projects/notices:/usr/lib/python2.7:/usr/lib/python2.7/plat-linux2:/usr/lib/python2.7/lib-tk:/usr/lib/python2.7/lib-old:/usr/lib/python2.7/lib-dynload:/usr/local/lib/python2.7/dist-packages:/usr/lib/python2.7/dist-packages:/usr/lib/python2.7/dist-packages/gtk-2.0
export PYTHONPATH=/home/ilsdev/projects/notices
export EXCEPTIONS=/home/ilsdev/projects/notices/malformed_addr.txt
# The next line is all the addresses that should be receiving the notices. Make sure it is not commented in production.
EMAIL_ADDRESSES="printednotices@epl.ca,mailclerks@epl.ca,ilsadmins@epl.ca"
# Testing only make sure this is commented out when going to production.
# EMAIL_ADDRESSES="andrew.nisbet@epl.ca"

LOCAL_DIR=/home/ilsdev/projects/notices
APP=notice.py
PRINT_DIR=./print
REPORT_DIR=./reports
BULLETIN_DIR=./bulletins
BILLS=${REPORT_DIR}/bills.prn
HOLDS=${REPORT_DIR}/holds.prn
OVERDUES=${REPORT_DIR}/overdues.prn
PREREFERRAL=${REPORT_DIR}/prereferral.prn
LOG_FILE=${LOCAL_DIR}/notices.log
# Clean up any existing reports.
cd ${LOCAL_DIR}
rm ${PRINT_DIR}/*.ps
echo "" >> ${LOG_FILE}
date >>${LOG_FILE}
echo "rm ${PRINT_DIR}/*.ps" >>${LOG_FILE}
rm ${PRINT_DIR}/*.pdf
echo "rm ${PRINT_DIR}/*.pdf" >>${LOG_FILE}
rm ${REPORT_DIR}/*.prn
echo "rm ${REPORT_DIR}/*.prn" >>${LOG_FILE}
rm ${BULLETIN_DIR}/*
echo "rm ${BULLETIN_DIR}/*" >>${LOG_FILE}
${LOCAL_DIR}/report.sh   # getting today's reports
${LOCAL_DIR}/bulletin.sh # getting Notices for today's reports.
#${LOCAL_DIR}/${APP} -h -s    -i${HOLDS}  >>${LOG_FILE}
#echo "${LOCAL_DIR}/${APP} -h -s    -i${HOLDS}" >>${LOG_FILE}
python3 ${LOCAL_DIR}/${APP} -s -b10.0 -i${BILLS}  >>${LOG_FILE}
echo "python3 ${LOCAL_DIR}/${APP} -s -b10.0 -i${BILLS}" >>${LOG_FILE}
python3 ${LOCAL_DIR}/${APP} -o -s    -i${OVERDUES} >>${LOG_FILE}
echo "python3 ${LOCAL_DIR}/${APP} -o -s    -i${OVERDUES}" >>${LOG_FILE}
python3 ${LOCAL_DIR}/${APP} -r -s    -i${PREREFERRAL}  >>${LOG_FILE}
echo "python3 ${LOCAL_DIR}/${APP} -r -s -i${PREREFERRAL}" >>${LOG_FILE}
${LOCAL_DIR}/pstopdf.sh
cd ${PRINT_DIR}
for name in $(ls *.pdf)
do
	# printf "%s\n" "$name"
	/usr/bin/uuencode $name $name | /usr/bin/mailx -a'From:ilsdev@ilsdev1.epl.ca' -s "Print Notices `date`" "$EMAIL_ADDRESSES"
done
# Now mail the exceptions list to Vicky and I
#/usr/bin/uuencode $EXCEPTIONS $EXCEPTIONS | /usr/bin/mailx -a'From:ilsdev@ilsdev1.epl.ca' -s "Print Notice Address Exceptions `date`" "ilsadmins@epl.ca vvarga@epl.ca"
