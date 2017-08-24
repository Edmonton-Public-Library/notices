#!/bin/bash
###########################################################################
#
# Parses each report to determine which notices are referenced in the reports
# then SCPs them over from the ILS.
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
# Dependency: Must have SSH public key in the sirsi/.ssh/authorized_keys file
# to allow password-less transfer of notice files.
#
# The files are copied fresh each day, ensuring that any changes to the files
# are reflected on the next run.
SERVER=eplapp.library.ualberta.ca
USER=sirsi
REMOTE="/s/sirsi/Unicorn/Notices"
LIST_OF_BULLETINS="bulletins.lst"
LIST_OF_BULLETIN_FILES="notice.lst"
REPORT_DIR="reports"
BULLETIN_DIR="bulletins"

# Get a list every time a report makes reference to a .read tag:
grep "\.read " $REPORT_DIR/*.prn | cut -d":" -f2 >$LIST_OF_BULLETINS
# remove the spaces and get back the last field
sed -e 's/\// /g' $LIST_OF_BULLETINS | awk '{print $NF}' | sort | uniq -c | cut -c9- >$LIST_OF_BULLETIN_FILES

for i in $(cat $LIST_OF_BULLETIN_FILES)
do
	# printf "%s\n" "$i"
	scp $USER\@$SERVER:$REMOTE/$i $BULLETIN_DIR
done

rm ${LIST_OF_BULLETIN_FILES}
rm ${LIST_OF_BULLETINS}
