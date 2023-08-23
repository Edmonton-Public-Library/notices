#!/bin/bash
###########################################################################
#
# Collects all the reports required for the reports in the reports / directory.
#
#    Copyright (C) 2012 - 2023 Andrew Nisbet, Edmonton Public Library
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
# Version: Added 'PreLost Overdue Notice - HTG Print' and 
#          convert 'Overdue Notices - Weekdays' to 
#          'Overdue Reminder - 8 Days Print'
# 
###########################################################################
###
### Computes what today's various reports are by code and copies those to 
### the local directory for consumption by other processes. See notices.sh
### for more information.
###
APP=$(basename -s .sh $0)
SERVER=sirsi\@edpl.sirsidynix.net
REMOTE_PRINT_DIR=/software/EDPL/Unicorn/Rptprint
REMOTE_SCATCH_DIR=/software/EDPL/Unicorn/EPLwork/anisbet/Reports
REPORT_DIR=/home/ils/notices/reports
BILL_REPORT=bills
ODUE_REPORT=overdues
PRER_REPORT=prereferral
PLOS_REPORT=prelost
VERSION="1.02.05"
HOST=$(hostname)
ERROR_COUNT=0
## Set up logging.
LOG_FILE=/home/ils/notices/notices.log
# Logs messages to STDOUT and $LOG_FILE file.
# param:  Message to put in the file.
logit()
{
    local message="$1"
    local TIME=''
    TIME=$(date +"%Y-%m-%d %H:%M:%S")
    if [ -t 0 ]; then
        # If run from an interactive shell message STDOUT and LOG_FILE.
        echo -e "[$TIME] $message" | tee -a $LOG_FILE
    else
        # If run from cron do write to log.
        echo -e "[$TIME] $message" >>$LOG_FILE
    fi
}

# Prints out usage message.
usage()
{
    cat << EOFU!
 Usage: $APP [flags]

Starts and monitors status of arbitrary scripts, either as daemon(s)
or shorter running applications.

Flags:
-c, --code='code': Used with --reprint to reprint a given report type with
  the sched ID of 'code' where sched IDs are 4 alphabet lower-case characters long.
-h, --help: This help message.
-r, --reprint='bills|prereferral|overdues|prelost': Type of report to reprint, 
  used with --code.
-v, --version: Print $APP version and exits.
 Example:
    ${0} --reprint='bills' --code='pcrf'
EOFU!
}

################ Bills ###############
function bill_notices() 
{
    local special_report_code="$1"
    local which_report="$2"
    if [ -n "$special_report_code" ]; then
        logit "looking for $which_report report with sched ID of '$special_report_code'"
        REPORT_CODE="$special_report_code"
    else
        logit "looking for today's bills report"
        REPORT_CODE=$(ssh $SERVER 'echo "Generalized Bill Notices - Weekday" | rptstat.pl -oc | cut -d"|" -f1')
    fi
    if [ -z "$REPORT_CODE" ]; then
        logit "**error, failed to find 'Generalized Bill Notices - Weekday'. Check that you can run rptstat.pl via ssh."
        ERROR_COUNT=$((ERROR_COUNT + 1))
    fi
    # Translate the report to replace the Sirsi Internationalization codes with English text.
    if ssh $SERVER "cat ${REMOTE_PRINT_DIR}/${REPORT_CODE}.prn | translate >${REMOTE_SCATCH_DIR}/${BILL_REPORT}.prn"; then
        # Get the file from the production server.
        logit "translated ${REPORT_CODE}.prn into human readable format (${REMOTE_SCATCH_DIR}/${BILL_REPORT}.prn)."
        if scp $SERVER:${REMOTE_SCATCH_DIR}/${BILL_REPORT}.prn ${REPORT_DIR}/ ; then
            logit "${BILL_REPORT}.prn copied from the ILS to ${REPORT_DIR}/ on $HOST"
        else
            logit "**error, failed to copy $SERVER:${REMOTE_SCATCH_DIR}/${BILL_REPORT}.prn to ${REPORT_DIR}/"
            ERROR_COUNT=$((ERROR_COUNT + 1))
        fi
    else
        logit "**error, failed to translate ${REMOTE_PRINT_DIR}/${REPORT_CODE}.prn"
        ERROR_COUNT=$((ERROR_COUNT + 1))
    fi
}

################ Overdue ###############
function overdue_reminder_notices()
{
    local special_report_code="$1"
    local which_report="$2"
    if [ -n "$special_report_code" ]; then
        logit "looking for $which_report report with sched ID of '$special_report_code'"
        REPORT_CODE="$special_report_code"
    else
        logit "looking for today's Overdue Reminder - 8 Days Print report"
        REPORT_CODE=$(ssh $SERVER 'echo "Overdue Reminder - 8 Days Print" | rptstat.pl -oc | cut -d"|" -f1')
    fi
    if [ -z "$REPORT_CODE" ]; then
        logit "**error, failed to find  today's 'Overdue Reminder - 8 Days Print'. Check that you can run rptstat.pl via ssh."
        ERROR_COUNT=$((ERROR_COUNT + 1))
    fi 
    if ssh $SERVER "cat ${REMOTE_PRINT_DIR}/${REPORT_CODE}.prn | translate >${REMOTE_SCATCH_DIR}/${ODUE_REPORT}.prn"; then
        logit "${ODUE_REPORT}.prn translated to human readable form (${REMOTE_SCATCH_DIR}/${ODUE_REPORT}.prn)."
        if scp $SERVER:${REMOTE_SCATCH_DIR}/${ODUE_REPORT}.prn ${REPORT_DIR}/ ; then
            logit "${ODUE_REPORT}.prn copied from the ILS to ${REPORT_DIR}/"
        else
            logit "**error, failed to copy $SERVER:${REMOTE_SCATCH_DIR}/${ODUE_REPORT}.prn to ${REPORT_DIR}/"
            ERROR_COUNT=$((ERROR_COUNT + 1))
        fi
    else
        logit "**error, failed to translate ${REMOTE_PRINT_DIR}/${REPORT_CODE}.prn"
        ERROR_COUNT=$((ERROR_COUNT + 1))
    fi
}

################ PreReferral ###############
function prereferral_notices()
{
    local special_report_code="$1"
    local which_report="$2"
    if [ -n "$special_report_code" ]; then
        logit "looking for $which_report report with sched ID of '$special_report_code'"
        REPORT_CODE="$special_report_code"
    else
        logit "looking for today's pre-referral bill notice report"
        REPORT_CODE=$(ssh $SERVER 'echo "PreReferral Bill Notice - Weekdays" | rptstat.pl -oc | cut -d"|" -f1')
    fi
    if [ -z "$REPORT_CODE" ]; then
        logit "**error, failed to find  today's 'PreReferral Bill Notice - Weekdays'. Check that you can run rptstat.pl via ssh."
        ERROR_COUNT=$((ERROR_COUNT + 1))
    fi 
    if ssh $SERVER "cat ${REMOTE_PRINT_DIR}/${REPORT_CODE}.prn | translate >${REMOTE_SCATCH_DIR}/${PRER_REPORT}.prn"; then
        logit "${PRER_REPORT}.prn translated to human readable form (${REMOTE_SCATCH_DIR}/${PRER_REPORT}.prn)."
        if scp $SERVER:${REMOTE_SCATCH_DIR}/${PRER_REPORT}.prn ${REPORT_DIR}/ ; then
            logit "${PRER_REPORT}.prn copied from the ILS to ${REPORT_DIR}/"
        else
            logit "**error, failed to copy $SERVER:${REMOTE_SCATCH_DIR}/${PRER_REPORT}.prn to ${REPORT_DIR}/"
            ERROR_COUNT=$((ERROR_COUNT + 1))
        fi
    else
        logit "**error, failed to translate ${REMOTE_PRINT_DIR}/${REPORT_CODE}.prn"
        ERROR_COUNT=$((ERROR_COUNT + 1))
    fi
}

################ PreLost ###############
function prelost_notices()
{
    local special_report_code="$1"
    local which_report="$2"
    if [ -n "$special_report_code" ]; then
        logit "looking for $which_report report with sched ID of '$special_report_code'"
        REPORT_CODE="$special_report_code"
    else
        logit "looking for today's pre-lost overdue notice report"
        REPORT_CODE=$(ssh $SERVER 'echo "PreLost Overdue Notice - HTG Print" | rptstat.pl -oc | cut -d"|" -f1')
    fi
    if [ -z "$REPORT_CODE" ]; then
        logit "**error, failed to find  today's 'PreLost Overdue Notice - HTG Print'. Check that you can run rptstat.pl via ssh."
        ERROR_COUNT=$((ERROR_COUNT + 1))
    fi 
    if ssh $SERVER "cat ${REMOTE_PRINT_DIR}/${REPORT_CODE}.prn | translate >${REMOTE_SCATCH_DIR}/${PLOS_REPORT}.prn"; then
        logit "${PLOS_REPORT}.prn translated to human readable form (${REMOTE_SCATCH_DIR}/${PLOS_REPORT}.prn)."
        if scp $SERVER:${REMOTE_SCATCH_DIR}/${PLOS_REPORT}.prn ${REPORT_DIR}/ ; then
            logit "${PLOS_REPORT}.prn copied from the ILS to ${REPORT_DIR}/"
        else
            logit "**error, failed to copy $SERVER:${REMOTE_SCATCH_DIR}/${PLOS_REPORT}.prn to ${REPORT_DIR}/"
            ERROR_COUNT=$((ERROR_COUNT + 1))
        fi
    else
        logit "**error, failed to translate ${REMOTE_PRINT_DIR}/${REPORT_CODE}.prn"
        ERROR_COUNT=$((ERROR_COUNT + 1))
    fi
}

### Check input parameters.
# $@ is all command line parameters passed to the script.
# -o is for short options like -v
# -l is for long options with double dash like --version
# the comma separates different long options
# -a is for long options with single dash like -version
options=$(getopt -l "code:,help,reprint:,version" -o "c:hr:v" -a -- "$@")
if [ $? != 0 ] ; then echo "Failed to parse options...exiting." >&2 ; exit 1 ; fi
# set --:
# If no arguments follow this option, then the positional parameters are unset. Otherwise, the positional parameters
# are set to the arguments, even if some of them begin with a ‘-’.
eval set -- "$options"

while true
do
    case $1 in
    -c|--code)
        shift
        REPRINT_REPORT_CODE="$1"
        ;;
    -h|--help)
        usage
        exit 0
        ;;
    -r|--reprint)
        shift
        REPRINT_REPORT="$1"
        ;;
    -v|--version)
        echo "$APP version: $VERSION"
        exit 0
        ;;
    --)
        shift
        break
        ;;
    esac
    shift
done


logit "== Starting $0 version: $VERSION on $HOST"
if [ -z "$REPRINT_REPORT" ]; then
    if [ -z "$REPRINT_REPORT_CODE" ]; then
        bill_notices
        overdue_reminder_notices
        prereferral_notices
        prelost_notices
    else
        logit "*error use both --reprint and --code for a special report reprint"
        exit 1
    fi
else
    if [ -n "$REPRINT_REPORT_CODE" ]; then
        logit "special report reprint of '$REPRINT_REPORT' with code '$REPRINT_REPORT_CODE"
        if [ "$REPRINT_REPORT" = 'bills' ]; then
            bill_notices "$REPRINT_REPORT_CODE" "$REPRINT_REPORT"
        elif [ "$REPRINT_REPORT" = 'overdues' ]; then
            overdue_reminder_notices "$REPRINT_REPORT_CODE" "$REPRINT_REPORT"
        elif [ "$REPRINT_REPORT" = 'prereferral' ]; then
            prereferral_notices "$REPRINT_REPORT_CODE" "$REPRINT_REPORT"
        elif [ "$REPRINT_REPORT" = 'prelost' ]; then
            prelost_notices "$REPRINT_REPORT_CODE" "$REPRINT_REPORT"
        else
            logit "*error, no such report type: '$REPRINT_REPORT'"
            exit 1
        fi
        logit "*************************************************************"
        logit "* NOTE: Dates are automatically added to *.ps files by the"
        logit "* report generator. This will be fixed, but until then if"
        logit "* you are reprinting from a day that isn't the day the report"
        logit "* was run, find-and-replace the date in the PS file(s) before"
        logit "* running ps2pdf.sh."
        logit "*************************************************************"
    else
        logit "*error use both --reprint and --code for a special report reprint"
        exit 1
    fi
fi
logit "             finished with $ERROR_COUNT error(s)."
## EOF
