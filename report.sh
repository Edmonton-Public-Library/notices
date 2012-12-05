#!/bin/bash

# Collects all the reports required for the reports in the reports/ directory
#
REPORT_DIR=reports
SERVER=eplapp.library.ualberta.ca
USER=sirsi
REMOTE_PRINT_DIR="/s/sirsi/Unicorn/Rptprint"
REMOTE_SCATCH_DIR="/s/sirsi/Unicorn/EPLwork/anisbet/Reports"
REPORT_DIR="reports"
BILL_REPORT="bills"
HOLD_REPORT="holds"
ODUE_REPORT="overdues"
# Get the reports from rptstat.pl:

################ Bills ###############
# Find the bills report for today
REPORT_CODE=`ssh $USER\@$SERVER 'echo "Generalized" | rptstat.pl -oc | cut -d"|" -f1'`
# Translate the report to replace the Sirsi Internationalization codes with English text.
CMD="cat /s/sirsi/Unicorn/Rptprint/${REPORT_CODE}.prn | translate >${REMOTE_SCATCH_DIR}/${BILL_REPORT}.prn"
ssh $USER\@$SERVER $CMD
# Get the file from the production server.
scp $USER\@$SERVER:${REMOTE_SCATCH_DIR}/${BILL_REPORT}.prn ${REPORT_DIR}/


################ Overdue ###############
REPORT_CODE=`ssh $USER\@$SERVER 'echo "Overdue Notices" | rptstat.pl -oc | cut -d"|" -f1'`
CMD="cat /s/sirsi/Unicorn/Rptprint/${REPORT_CODE}.prn | translate >${REMOTE_SCATCH_DIR}/${ODUE_REPORT}.prn"
ssh $USER\@$SERVER $CMD
scp $USER\@$SERVER:${REMOTE_SCATCH_DIR}/${ODUE_REPORT}.prn ${REPORT_DIR}/


################ Holds ###############
REPORT_CODE=`ssh $USER\@$SERVER 'echo "Hold Pickup Notices" | rptstat.pl -oc | cut -d"|" -f1'`
CMD="cat /s/sirsi/Unicorn/Rptprint/${REPORT_CODE}.prn | translate >${REMOTE_SCATCH_DIR}/${HOLD_REPORT}.prn"
ssh $USER\@$SERVER $CMD
scp $USER\@$SERVER:${REMOTE_SCATCH_DIR}/${HOLD_REPORT}.prn ${REPORT_DIR}/


