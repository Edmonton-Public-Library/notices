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
# Collects all the notices required for the day and coordinates convertion to PDF.
#
export HOME=/home/ilsdev
export LOGNAME=ilsdev
export PATH=$PATH:/usr/bin:/bin
export LANG=en_US.UTF-8
export SHELL=/bin/sh
export PWD=/home/ilsdev

LOCAL=/home/ilsdev/projects/notices
APP=notice.py
PRINT_DIR=${LOCAL}/print
REPORT_DIR=${LOCAL}/reports
BILLS=${REPORT_DIR}/bills.prn
HOLDS=${REPORT_DIR}/holds.prn
OVERDUES=${REPORT_DIR}/overdues.prn

rm ${PRINT_DIR}/*.ps
rm ${PRINT_DIR}/*.pdf
rm ${REPORT_DIR}/*.prn
${LOCAL}/report.sh   # getting today's reports
# ${LOCAL}/bulletin.sh # getting Notices for today's reports.
/usr/bin/python ${LOCAL}/${APP} -h     -i${HOLDS}
/usr/bin/python ${LOCAL}/${APP} -b10.0 -i${BILLS}
/usr/bin/python ${LOCAL}/${APP} -o     -i${OVERDUES}
${LOCAL}/pstopdf.sh
cd ${PRINT_DIR}
for name in $(ls *.pdf)
do
	# printf "%s\n" "$name"
	/usr/bin/uuencode $name $name | /usr/bin/mailx -s "Print Notices" "ilsteam@epl.ca"
done

