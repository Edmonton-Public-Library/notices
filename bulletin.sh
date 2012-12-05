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
# Collects all the notices required for the reports in the reports/ directory
#
REPORT_DIR=reports
BULLETIN_DIR=bulletins
SERVER=eplapp.library.ualberta.ca
USER=sirsi
REMOTE=/s/sirsi/Unicorn/Notices/
LIST_OF_BULLETINS=$BULLETIN_DIR/bulletins.lst
# Get a list every time a report makes reference to a .read tag:
grep "\.read " $REPORT_DIR/*.prn | cut -d":" -f2 >$LIST_OF_BULLETINS
# remove the spaces and get back the last field
sed -e 's/\// /g' notices.txt | awk '{print $NF}' | sort | uniq -c | cut -c9- >$LIST_OF_BULLETINS

for i in $(cat $LIST_OF_BULLETINS)
do
	# printf "%s\n" "$i"
	scp $USER\@$SERVER:$REMOTE$i $BULLETIN_DIR
done
