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


# SERVER=edpl-t.library.ualberta.ca
SERVER=eplapp.library.ualberta.ca
USER=sirsi
REMOTE=~/Unicorn/EPLwork/anisbet/
LOCAL=./
APP=notice.py
RELATED=customer.py reportreader.py
ARGS= -h --ifile=testdata/Gen_bills.prn 

run: ${RELATED}
	clear
	python ${LOCAL}${APP} -h     -itestdata/Gen_bills.prn
	#
	#
	python ${LOCAL}${APP} -b12.0 -itestdata/Gen_bills.prn
	#
	#
	python ${LOCAL}${APP} -o     -itestdata/Gen_bills.prn
	#
	#
test: ${RELATED}
	clear
	python ${LOCAL}${APP} -v
put: test 
	scp ${LOCAL}*.py ${USER}@${SERVER}:${REMOTE}
page:
	python ${LOCAL}page.py
format:
	python ${LOCAL}noticeformatter.py
customer:
	python ${LOCAL}customer.py
convert:
	ps2pdf14 testFormatPage.ps test.pdf
clean:
	-rm *.pyc
