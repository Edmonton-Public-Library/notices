#!/bin/bash
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
# Collects all the reports required for the reports in the reports/ directory
#
export HOME=/home/ilsdev
export LOGNAME=ilsdev
export PATH=$PATH:/usr/bin:/bin
export LANG=en_US.UTF-8
export SHELL=/bin/sh
export PWD=/home/ilsdev

REPORT_DIR=reports
SERVER=eplapp.library.ualberta.ca
USER=sirsi
REMOTE_PRINT_DIR=/s/sirsi/Unicorn/Rptprint
REMOTE_SCATCH_DIR=/s/sirsi/Unicorn/EPLwork/anisbet/Reports
REPORT_DIR=reports
BILL_REPORT=bills
HOLD_REPORT=holds
ODUE_REPORT=overdues
# Get the reports from rptstat.pl:

################ Bills ###############
# Find the bills report for today
REPORT_CODE=`ssh $USER\@$SERVER 'echo "Generalized" | rptstat.pl -oc | cut -d"|" -f1'`
# Translate the report to replace the Sirsi Internationalization codes with English text.
CMD="cat /s/sirsi/Unicorn/Rptprint/${REPORT_CODE}.prn | translate >${REMOTE_SCATCH_DIR}/${BILL_REPORT}.prn"
echo $CMD
/usr/bin/ssh $USER\@$SERVER $CMD
# Get the file from the production server.
/usr/bin/scp $USER\@$SERVER:${REMOTE_SCATCH_DIR}/${BILL_REPORT}.prn ${REPORT_DIR}/


################ Overdue ###############
REPORT_CODE=`ssh $USER\@$SERVER 'echo "Overdue Notices" | rptstat.pl -oc | cut -d"|" -f1'`
CMD="cat /s/sirsi/Unicorn/Rptprint/${REPORT_CODE}.prn | translate >${REMOTE_SCATCH_DIR}/${ODUE_REPORT}.prn"
echo $CMD
/usr/bin/ssh $USER\@$SERVER $CMD
/usr/bin/scp $USER\@$SERVER:${REMOTE_SCATCH_DIR}/${ODUE_REPORT}.prn ${REPORT_DIR}/


################ Holds ###############
REPORT_CODE=`ssh $USER\@$SERVER 'echo "Hold Pickup Notices" | rptstat.pl -oc | cut -d"|" -f1'`
CMD="cat /s/sirsi/Unicorn/Rptprint/${REPORT_CODE}.prn | translate >${REMOTE_SCATCH_DIR}/${HOLD_REPORT}.prn"
echo $CMD
/usr/bin/ssh $USER\@$SERVER $CMD
/usr/bin/scp $USER\@$SERVER:${REMOTE_SCATCH_DIR}/${HOLD_REPORT}.prn ${REPORT_DIR}/


