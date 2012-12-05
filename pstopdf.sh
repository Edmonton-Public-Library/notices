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
# Converts the PS files in the print/ directory to PDF
# =======================================
# *** Requires the use of Ghostscript ***
# =======================================
#

PRINT_DIR="print"
PS_LIST="ps_files.lst"
# convert all the PS files in print using
# basic format: ps2pdf14 testFormatPage.ps test.pdf

cd ${PRINT_DIR}
ls -c1 *.ps >$PS_LIST

for psFile in $(cat $PS_LIST)
do
	printf "converting: %s\n" "${psFile}"
	ps2pdf14 ${psFile}
done

rm $PS_LIST
