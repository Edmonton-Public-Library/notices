#!/bin/bash
###########################################################################
#
# Collects all the reports required for the reports in the reports / directory.
#
#    Copyright (C) 2012 - 2021 Andrew Nisbet, Edmonton Public Library
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
### Computes what today's various reports are by code and copies those to 
### the local directory for consumption by other processes. See notices.sh
### for more information.
###
SERVER=sirsi\@edpl.sirsidynix.net
REMOTE_PRINT_DIR=/software/EDPL/Unicorn/Rptprint
REMOTE_SCATCH_DIR=/software/EDPL/Unicorn/EPLwork/anisbet/Reports
REPORT_DIR=/home/ils/notices/reports
BILL_REPORT=bills
HOLD_REPORT=holds
ODUE_REPORT=overdues
PRER_REPORT=prereferral
VERSION="1.00.03"
HOST=$(hostname)
ERROR_COUNT=0
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

################ Bills ###############
logit "== Starting $0 version: $VERSION on $HOST"
logit "looking for today's bills report"
REPORT_CODE=$(ssh $SERVER 'echo "Generalized Bill Notices - Weekday" | rptstat.pl -oc | cut -d"|" -f1')
if [ -z "$REPORT_CODE" ]; then
    logit "**error, failed to find  today's 'Generalized Bill Notices - Weekday'. Check that you can run rptstat.pl via ssh."
    ERROR_COUNT=$(($ERROR_COUNT + 1))
fi
# Translate the report to replace the Sirsi Internationalization codes with English text.
if ssh $SERVER "cat ${REMOTE_PRINT_DIR}/${REPORT_CODE}.prn | translate >${REMOTE_SCATCH_DIR}/${BILL_REPORT}.prn"; then
    # Get the file from the production server.
    logit "translated ${REPORT_CODE}.prn into human readable format (${REMOTE_SCATCH_DIR}/${BILL_REPORT}.prn)."
    if scp $SERVER:${REMOTE_SCATCH_DIR}/${BILL_REPORT}.prn ${REPORT_DIR}/ ; then
        logit "${BILL_REPORT}.prn copied from the ILS to ${REPORT_DIR}/ on $HOST"
    else
        logit "**error, failed to copy $SERVER:${REMOTE_SCATCH_DIR}/${BILL_REPORT}.prn to ${REPORT_DIR}/"
        ERROR_COUNT=$(($ERROR_COUNT + 1))
    fi
else
    logit "**error, failed to translate ${REMOTE_PRINT_DIR}/${REPORT_CODE}.prn"
    ERROR_COUNT=$(($ERROR_COUNT + 1))
fi


################ Overdue ###############
logit "looking for today's overdue notice report"
REPORT_CODE=`ssh $SERVER 'echo "Overdue Notices - Weekday" | rptstat.pl -oc | cut -d"|" -f1'`
if [ -z "$REPORT_CODE" ]; then
    logit "**error, failed to find  today's 'Overdue Notices - Weekday'. Check that you can run rptstat.pl via ssh."
    ERROR_COUNT=$(($ERROR_COUNT + 1))
fi 
if ssh $SERVER "cat ${REMOTE_PRINT_DIR}/${REPORT_CODE}.prn | translate >${REMOTE_SCATCH_DIR}/${ODUE_REPORT}.prn"; then
    logit "${ODUE_REPORT}.prn translated to human readable form (${REMOTE_SCATCH_DIR}/${ODUE_REPORT}.prn)."
    if scp $SERVER:${REMOTE_SCATCH_DIR}/${ODUE_REPORT}.prn ${REPORT_DIR}/ ; then
        logit "${ODUE_REPORT}.prn copied from the ILS to ${REPORT_DIR}/"
    else
        logit "**error, failed to copy $SERVER:${REMOTE_SCATCH_DIR}/${ODUE_REPORT}.prn to ${REPORT_DIR}/"
        ERROR_COUNT=$(($ERROR_COUNT + 1))
    fi
else
    logit "**error, failed to translate ${REMOTE_PRINT_DIR}/${REPORT_CODE}.prn"
    ERROR_COUNT=$(($ERROR_COUNT + 1))
fi

################ PreReferral ###############
logit "looking for today's pre-referral bill notice report"
REPORT_CODE=`ssh $SERVER 'echo "PreReferral Bill Notice - Weekdays" | rptstat.pl -oc | cut -d"|" -f1'`
if [ -z "$REPORT_CODE" ]; then
    logit "**error, failed to find  today's 'PreReferral Bill Notice - Weekdays'. Check that you can run rptstat.pl via ssh."
    ERROR_COUNT=$(($ERROR_COUNT + 1))
fi 
if ssh $SERVER "cat ${REMOTE_PRINT_DIR}/${REPORT_CODE}.prn | translate >${REMOTE_SCATCH_DIR}/${PRER_REPORT}.prn"; then
    logit "${PRER_REPORT}.prn translated to human readable form (${REMOTE_SCATCH_DIR}/${PRER_REPORT}.prn)."
    if scp $SERVER:${REMOTE_SCATCH_DIR}/${PRER_REPORT}.prn ${REPORT_DIR}/ ; then
        logit "${PRER_REPORT}.prn copied from the ILS to ${REPORT_DIR}/"
    else
        logit "**error, failed to copy $SERVER:${REMOTE_SCATCH_DIR}/${PRER_REPORT}.prn to ${REPORT_DIR}/"
        ERROR_COUNT=$(($ERROR_COUNT + 1))
    fi
else
    logit "**error, failed to translate ${REMOTE_PRINT_DIR}/${REPORT_CODE}.prn"
    ERROR_COUNT=$(($ERROR_COUNT + 1))
fi
logit "             finished with $ERROR_COUNT error(s)."
## EOF
