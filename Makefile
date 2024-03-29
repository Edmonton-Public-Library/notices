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
## To install this application from repo, type:
## make -f makefile 
## or 
## make -f makefile production
SERVER=ils@epl-ils.epl.ca
REMOTE_DIR=/home/ils/notices
REMOTE_BIN_DIR=${REMOTE_DIR}/bin
CODE_FILES=notice.py customer.py reportreader.py page.py noticeformatter.py report.sh bulletin.sh pstopdf.sh notices.sh page.tst reportreader.tst testnotices.sh
HELPER_FILES=Readme.md Makefile.remote
PYTHON=../venv/bin/python
PS2PDF=/usr/bin/ps2pdf

.PHONY: clean production test

production: ${CODE_FILES} ${HELPER_FILES}
	scp ${CODE_FILES} ${SERVER}:${REMOTE_BIN_DIR}
	scp Readme.md ${SERVER}:${REMOTE_DIR}
	scp Makefile.remote ${SERVER}:${REMOTE_DIR}/Makefile

test: clean page.tst reportreader.tst
	${PYTHON} page.py 
	${PYTHON} noticeformatter.py 
	${PYTHON} reportreader.py 
	${PYTHON} customer.py
	-${PS2PDF} testpagePS.ps testpagePS.pdf
	-${PS2PDF} testformatpagePS.ps testformatpagePS.pdf

clean:
	-rm *.pdf
	-rm *.ps