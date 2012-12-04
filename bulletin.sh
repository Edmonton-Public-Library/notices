#!/bin/bash

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
