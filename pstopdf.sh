#!/bin/bash
###########################################################################
#
# Converts the PS files in the print/ directory to PDF
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
#
# Dependencies: Ghostscript.
# =======================================
# *** Requires the use of Ghostscript ***
# =======================================
#

PRINT_DIR=/home/ilsdev/projects/notices/print
PS_LIST=${PRINT_DIR}/ps_files.lst
# convert all the PS files in print using
# basic format: ps2pdf14 testFormatPage.ps test.pdf

cd ${PRINT_DIR}
ls -c1 *.ps >$PS_LIST

for psFile in $(cat $PS_LIST)
do
	printf "converting: %s\n" "${psFile}"
	/usr/bin/ps2pdf14 ${PRINT_DIR}/${psFile}
done

rm $PS_LIST
