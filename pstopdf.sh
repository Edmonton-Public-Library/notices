#!/bin/bash
###########################################################################
#
# Converts the PS files in the print/ directory to PDF
#
#    Copyright (C) 2012 - 2021  Andrew Nisbet, Edmonton Public Library
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
#
# Dependencies: Ghostscript.
# =======================================
# *** Requires the use of Ghostscript ***
# =======================================
#

PRINT_DIR=/home/ils/notices/print
PS_LIST=${PRINT_DIR}/ps_files.lst
# convert all the PS files in print using
# basic format: ps2pdf14 testFormatPage.ps test.pdf
VERSION="1.00.02"
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
if ! cd ${PRINT_DIR}; then
	logit "**error, failed to cd into $PRINT_DIR."
	exit 1
fi
ls -c1 *.ps >$PS_LIST

for psFile in $(cat $PS_LIST)
do
	if /usr/bin/ps2pdf14 ${PRINT_DIR}/${psFile}; then
		logit "converted: ${psFile}"
	else
		logit "**error, converting ${psFile}"
		ERROR_COUNT=$(($ERROR_COUNT + 1))
	fi
done
logit "conversion to PDF finished, cleaning up."
rm $PS_LIST
logit "             finished with $ERROR_COUNT error(s)."
