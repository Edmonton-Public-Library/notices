#!/bin/bash
###########################################################################
#
# Parses each report to determine which notices are referenced in the reports
# then SCPs them over from the ILS.
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
# Dependency: Must have SSH public key in the sirsi/.ssh/authorized_keys file
# to allow password-less transfer of notice files.
#
# The files are copied fresh each day, ensuring that any changes to the files
# are reflected on the next run.
SERVER=edpl.sirsidynix.net
USER=sirsi
REMOTE="/software/EDPL/Unicorn/Notices"
LIST_OF_BULLETINS="bulletins.lst"
LIST_OF_BULLETIN_FILES="notice.lst"
REPORT_DIR="reports"
BULLETIN_DIR="bulletins"
VERSION="1.00.01"
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

################ script starts here ###############
logit "== Starting $0 version: $VERSION on $HOST"
# Get a list every time a report makes reference to a .read tag:
logit "compiling list of report prn files."
grep "\.read " $REPORT_DIR/*.prn | cut -d":" -f2 >$LIST_OF_BULLETINS
# remove the spaces and get back the last field
sed -e 's/\// /g' $LIST_OF_BULLETINS | awk '{print $NF}' | sort | uniq -c | cut -c9- >$LIST_OF_BULLETIN_FILES

for i in $(cat $LIST_OF_BULLETIN_FILES)
do
	# printf "%s\n" "$i"
	if scp $USER\@$SERVER:$REMOTE/$i $BULLETIN_DIR; then
		logit "scp'ed $REMOTE/$i to $BULLETIN_DIR."
	else
		logit "**error scp'ing $REMOTE/$i to $BULLETIN_DIR."
		ERROR_COUNT=$(($ERROR_COUNT + 1))
	fi
done
logit "cleaning up"
rm ${LIST_OF_BULLETIN_FILES}
rm ${LIST_OF_BULLETINS}
logit "             finished with $ERROR_COUNT error(s)."
