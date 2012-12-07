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

LOCAL=/home/ilsdev/projects/notices
APP=notice.py
RELATED=customer.py reportreader.py page.py noticeformatter.py
PRINT_DIR=${LOCAL}/print
REPORT_DIR=${LOCAL}/reports
BILLS=${REPORT_DIR}/bills.prn
HOLDS=${REPORT_DIR}/holds.prn
OVERDUES=${REPORT_DIR}/overdues.prn
ARGS= -b 10.0 --ifile=${BILLS}

test: ${RELATED}
	clear
	python ${LOCAL}/${APP} ${ARGS}
run: ${RELATED}
	clear
	# -rm ${PRINT_DIR}/*.ps
	# -rm ${PRINT_DIR}/*.pdf
	-rm ${REPORT_DIR}/*.prn
	${LOCAL}/report.sh   # getting today's reports
	${LOCAL}/bulletin.sh # getting Notices for today's reports.
	# python ${LOCAL}/${APP} -h     -i${HOLDS}
	# python ${LOCAL}/${APP} -b12.0 -i${BILLS}
	# python ${LOCAL}/${APP} -o     -i${OVERDUES}
	${LOCAL}/pstopdf.sh

page:
	python ${LOCAL}/page.py
format:
	python ${LOCAL}/noticeformatter.py
customer:
	python ${LOCAL}/customer.py
clean:
	-rm *.pyc
