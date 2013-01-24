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
RELATED=customer.py reportreader.py page.py noticeformatter.py report.sh bulletin.sh pstopdf.sh notices.sh
PRINT_DIR=${LOCAL}/print
REPORT_DIR=${LOCAL}/reports
BULLETINS_DIR=${LOCAL}/bulletins
BILLS=${REPORT_DIR}/bills.prn
HOLDS=${REPORT_DIR}/holds.prn
OVERDUES=${REPORT_DIR}/overdues.prn
ARGS_BILLS= -b 10.0 --ifile=${BILLS}
ARGS_HOLDS= -h --ifile=${HOLDS}
ARGS_OVERD= -o --ifile=${OVERDUES}

run: ${RELATED} clean
	${LOCAL}/report.sh   # getting today's reports
	${LOCAL}/bulletin.sh # getting Notices for today's reports.
	python ${LOCAL}/${APP} ${ARGS_BILLS}
	python ${LOCAL}/${APP} ${ARGS_HOLDS}
	python ${LOCAL}/${APP} ${ARGS_OVERD}
	${LOCAL}/pstopdf.sh

test: ${RELATED}
	python ${LOCAL}/${APP} ${ARGS_BILLS}
	python ${LOCAL}/${APP} ${ARGS_HOLDS}
	python ${LOCAL}/${APP} ${ARGS_OVERD}
	
pdf:
	${LOCAL}/pstopdf.sh
	
page:
	python ${LOCAL}/page.py
	
format:
	python ${LOCAL}/noticeformatter.py

customer:
	python ${LOCAL}/customer.py
	
clean:
	-rm ${PRINT_DIR}/*.ps
	-rm ${PRINT_DIR}/*.pdf
	-rm ${REPORT_DIR}/*.prn
	-rm ${BULLETINS_DIR}/*
	
proper: clean
	-rm *.pyc
