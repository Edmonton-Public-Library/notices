#!/bin/bash
###########################################################################
#
# Collects all the reports required for the reports in the reports / directory.
#
#    Copyright (C) 2012  Andrew Nisbet, Edmonton Public Library
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
#          1.0 - Added licensing changes and pre-referral report processing.
#          0.0 - Dev.
# 
###########################################################################
###
### Computes what today's various reports are by code and copies those to 
### the local directory for consumption by other processes. See notices.sh
### for more information.
###
export HOME=/home/ilsdev
export LOGNAME=ilsdev
export PATH=$PATH:/usr/bin:/bin
export LANG=en_US.UTF-8
export SHELL=/bin/sh
export PWD=/home/ilsdev

SERVER=eplapp.library.ualberta.ca
USER=sirsi
REMOTE_PRINT_DIR=/s/sirsi/Unicorn/Rptprint
REMOTE_SCATCH_DIR=/s/sirsi/Unicorn/EPLwork/anisbet/Reports
LOCAL_DIR=/home/ilsdev/projects/notices
REPORT_DIR=${LOCAL_DIR}/reports
LOG_FILE=${LOCAL_DIR}/notice.log
BILL_REPORT=bills
HOLD_REPORT=holds
ODUE_REPORT=overdues
PRER_REPORT=prereferral
# Get the reports from rptstat.pl:

################ Bills ###############
# Find the bills report for today
REPORT_CODE=`ssh $USER\@$SERVER 'echo "Generalized Bill Notices - Weekday" | rptstat.pl -oc | cut -d"|" -f1'`
# Translate the report to replace the Sirsi Internationalization codes with English text.
CMD="cat /s/sirsi/Unicorn/Rptprint/${REPORT_CODE}.prn | translate >${REMOTE_SCATCH_DIR}/${BILL_REPORT}.prn"
# echo $CMD >>${LOG_FILE}
echo "ssh $USER\@$SERVER '$CMD'" >>${LOG_FILE}
ssh $USER\@$SERVER "$CMD"
# Get the file from the production server.
echo "scp $USER\@$SERVER:${REMOTE_SCATCH_DIR}/${BILL_REPORT}.prn ${REPORT_DIR}/" >>${LOG_FILE}
scp $USER\@$SERVER:${REMOTE_SCATCH_DIR}/${BILL_REPORT}.prn ${REPORT_DIR}/


################ Overdue ###############
REPORT_CODE=`ssh $USER\@$SERVER 'echo "Overdue Notices - Weekday" | rptstat.pl -oc | cut -d"|" -f1'`
CMD="cat /s/sirsi/Unicorn/Rptprint/${REPORT_CODE}.prn | translate >${REMOTE_SCATCH_DIR}/${ODUE_REPORT}.prn"
# echo $CMD >>${LOG_FILE}
ssh $USER\@$SERVER "$CMD"
echo "scp $USER\@$SERVER:${REMOTE_SCATCH_DIR}/${ODUE_REPORT}.prn ${REPORT_DIR}/" >>${LOG_FILE}
scp $USER\@$SERVER:${REMOTE_SCATCH_DIR}/${ODUE_REPORT}.prn ${REPORT_DIR}/


################ Holds ###############
### No longer used, since we don't mail customers hold notices because they are too expensive.
#REPORT_CODE=`ssh $USER\@$SERVER 'echo "Hold Pickup Notices" | rptstat.pl -oc | cut -d"|" -f1'`
#CMD="cat /s/sirsi/Unicorn/Rptprint/${REPORT_CODE}.prn | translate >${REMOTE_SCATCH_DIR}/${HOLD_REPORT}.prn"
## echo $CMD >>${LOG_FILE}
#ssh $USER\@$SERVER "$CMD"
#echo "scp $USER\@$SERVER:${REMOTE_SCATCH_DIR}/${HOLD_REPORT}.prn ${REPORT_DIR}/" >>${LOG_FILE}
#scp $USER\@$SERVER:${REMOTE_SCATCH_DIR}/${HOLD_REPORT}.prn ${REPORT_DIR}/


################ PreReferral ###############
REPORT_CODE=`ssh $USER\@$SERVER 'echo "PreReferral Bill Notice - Weekdays" | rptstat.pl -oc | cut -d"|" -f1'`
CMD="cat /s/sirsi/Unicorn/Rptprint/${REPORT_CODE}.prn | translate >${REMOTE_SCATCH_DIR}/${PRER_REPORT}.prn"
# echo $CMD >>${LOG_FILE}
ssh $USER\@$SERVER "$CMD"
echo "scp $USER\@$SERVER:${REMOTE_SCATCH_DIR}/${PRER_REPORT}.prn ${REPORT_DIR}/" >>${LOG_FILE}
scp $USER\@$SERVER:${REMOTE_SCATCH_DIR}/${PRER_REPORT}.prn ${REPORT_DIR}/

## EOF
