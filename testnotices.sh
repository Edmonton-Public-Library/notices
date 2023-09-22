#!/bin/bash
###########################################################################
#
# Test run all reports.
#
#    Copyright (C) 2023  Andrew Nisbet, Edmonton Public Library
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
# Date:    Thu 21 Sep 2023
#
###########################################################################
###
### Edit this file to include new reports.
###
VERSION="1.01.00"
HOST=$(hostname)

# Activate the virtual environment.
if [ "$HOST" == 'ubuntu' ]; then
   . /home/anisbet/EPL/Notices/venv/bin/activate
   LOCAL_DIR=/home/anisbet/EPL/Notices/notices
else # or on production...
   . /home/ils/notices/venv/bin/activate
   LOCAL_DIR=/home/ils/notices
fi
LOCAL_BIN_DIR="$LOCAL_DIR"
X_ARGS=" -P -R"
APP=notice.py
PRINT_DIR=${LOCAL_DIR}/print
REPORT_DIR=${LOCAL_DIR}/reports
BULLETIN_DIR=${LOCAL_DIR}/bulletins
BILLS=${REPORT_DIR}/bills.prn
# HOLDS=${REPORT_DIR}/holds.prn
OVERDUES=${REPORT_DIR}/overdues.prn
PREREFERRAL=${REPORT_DIR}/prereferral.prn
PRELOST=${REPORT_DIR}/prelost.prn
## Set up logging.
LOG_FILE="$LOCAL_DIR/testnotices.log"
# Logs messages to STDOUT and $LOG_FILE file.
# param:  Message to put in the file.
logit()
{
    local message="$1"
    local TIME=$(date +"%Y-%m-%d %H:%M:%S")
    if [ -t 0 ]; then
        # If run from an interactive shell message STDOUT and LOG_FILE.
        echo -e "[$TIME] $message" | tee -a $LOG_FILE
    else
        # If run from cron do write to log.
        echo -e "[$TIME] $message" >>$LOG_FILE
    fi
}

# Set up test directories 
[ -d "$PRINT_DIR" ] || mkdir -p "$PRINT_DIR"
[ -d "$REPORT_DIR" ] || mkdir -p "$REPORT_DIR"
[ -d "$BULLETIN_DIR" ] || mkdir -p "$BULLETIN_DIR"

### Test data from heredocs ###
## Bulletins
touch "${BULLETIN_DIR}/blankmessage"

cat << EOF > "${BULLETIN_DIR}/eclosing"
If you have any questions or concerns, please contact us through online chat at epl.ca, phone (780-496-7000), text (587-817-0337) or drop by any of our locations.

Thank you,
The Edmonton Public Library
EOF

cat << EOF > "${BULLETIN_DIR}/eclosing8daysprint"
If you have any questions, we're happy to help. Contact us through online chat, phone (780-496-7000) or text (587-817-0337). 
Thank you, Edmonton Public Library
EOF

cat << EOF > "${BULLETIN_DIR}/overdue8daysprint"
ONE WEEK OVERDUE NOTICE

Please return these overdue items as other customers could be waiting. 
You have two weeks before these items are changed to "lost" in our system and a bill is applied to your account for the price of each item.

EOF

cat << EOF > "${BULLETIN_DIR}/prelostoverdue1stprint"
FINAL OVERDUE NOTICE

This is the last overdue notice you will receive reminding you to return the items listed below before replacement charges are billed to your account. 
Please return these items within one week to avoid being billed the price of each item.
EOF

cat << EOF > "${BULLETIN_DIR}/prelostoverdueclosingprint"
If you have any questions, we're happy to help. Contact us through online chat, phone (780-496-7000) or text (587-817-0337). 
Thank you, Edmonton Public Library
EOF

cat << EOF > "${BULLETIN_DIR}/prereferralbillclosing"
You owe over \$39.99. Please return these item(s) or pay the outstanding balance within 60 days from the bill date to avoid your account being referred to a third-party materials recovery company. 
Please note that a \$15 non-refundable referral fee will be charged to your account at the time of referral.
If you have any questions or concerns, please contact us through online chat at epl.ca, phone (780-496-7000), text (587-817-0337) or drop by any of our locations.
For your convenience, you may choose to pay online at epl.ca/myaccount.
Thank you, The Edmonton Public Library
EOF

## Example Bill
cat << EOF > "$BILLS"
.folddata
.report
.col 5l,1,73
.language ENGLISH
Thursday, September 21, 2023










.block
          Kathy Swasey
          DEAN MOM
          10003 123 Avenue NW
          Edmonton, AB
          T7M 1S4
.endblock


.read /software/EDPL/Unicorn/Notices/blankmessage

.block
  1   Incredible hockey records / by Tom Glave.
      Glave, Tom.
      date billed:9/6/2023     bill reason:LOST         amount due:    \$30.20
.endblock

.block
      =======================================================================

                                 TOTAL FINES/FEES AND UNPAID BILLS:    \$30.20
.endblock

.block
.read /software/EDPL/Unicorn/Notices/eclosing
.endblock

.report
.col 5l,1,73
.language ENGLISH
Thursday, September 21, 2023










.block
          Hamish Hosh
          1654 203 Street NW
          Edmonton, AB
          T7M 1K8
.endblock


.read /software/EDPL/Unicorn/Notices/blankmessage

.block
  1   Layla's luck / Jo Rooks.
      Rooks, Jo.
      date billed:9/6/2023     bill reason:LOST         amount due:    \$21.12
.endblock

.block
  2   The nice dream truck / by Beth Ferry ; illustrated by Brigette Barrager.
      Ferry, Beth.
      date billed:9/6/2023     bill reason:LOST         amount due:    \$20.97
.endblock

.block
  3   Home : a peek-through picture book / [text by Patricia Hegarty] ;
      illustrated by Britta Teckentrup.
      Hegarty, Patricia.
      date billed:9/6/2023     bill reason:LOST         amount due:    \$21.56
.endblock

.block
      =======================================================================

                                 TOTAL FINES/FEES AND UNPAID BILLS:    \$63.65
.endblock

.block
.read /software/EDPL/Unicorn/Notices/eclosing
.endblock
EOF

## Example Overdues
cat << EOF > "$OVERDUES"
.folddata
.report
.col 5l,1,73
.language ENGLISH
Thursday, September 21, 2023










.block
          Billy G Beaks
          5554 107 Street NW
          Edmonton, AB
          T7J 2R9
.endblock


.read /software/EDPL/Unicorn/Notices/overdue8daysprint

  1  call number:613.2 BUE                                 ID:31221122339448  
     The Blue Zones challenge : a 4-week plan for a longer, better life / Dan
     Buettner.
     Buettner, Dan.
     due:9/13/2023,23:59 

  2  call number:613.25 PAS                                ID:31221108058897  
     The body reset diet : power your metabolism, blast fat, and shed pounds
     in just 15 days / Harley Pasternak with Laura Moser.
     Pasternak, Harley.
     due:9/13/2023,23:59 

.read /software/EDPL/Unicorn/Notices/eclosing8daysprint
.report
.col 5l,1,73
.language ENGLISH
Thursday, September 21, 2023










.block
          Wren Potatoe
          1100 93 Street NW
          Edmonton, AB
          T5C 3T4
.endblock


.read /software/EDPL/Unicorn/Notices/overdue8daysprint

  1  call number:DVD TWO                                   ID:31221318205858  
     2 days in New York [videorecording] / directed by Julie Delpy.
     Delpy, Julie, 1969-
     due:9/13/2023,23:59 

  2  call number:306.7662 SAV                              ID:31221108459830  
     American Savage : insights, slights, and fights on faith, sex, love, and
     politics / Dan Savage. --.
     Savage, Dan.
     due:9/13/2023,23:59 

  3  call number:DVD I                                     ID:31221113455450  
     I am Michael [videorecording] / director, Justin Kelly.
     Kelly, Justin, 1992-
     due:9/13/2023,23:59 

  4  call number:DVD NUR                                   ID:31221217715809  
     Nurse Jackie. Season one [videorecording].
     Falco, Edie.
     due:9/13/2023,23:59 

  5  call number:DVD PEO                                   ID:31221118134936  
     People like us [videorecording] / directed by Alex Kurtzman.
     Kurtzman, Alex.
     due:9/13/2023,23:59 

  6  call number:DVD PLA                                   ID:31221317803281  
     Planes, trains and automobiles [videorecording] / written, produced and
     directed by John Hughes.
     Hughes, John, 1950-2009.
     due:9/13/2023,23:59 

  7  call number:DVD WOM                                   ID:31221217737894  
     The woman king [videorecording] / directed by Gina Prince-Bythewood.
     Prince-Bythewood, Gina.
     due:9/13/2023,23:59 

.read /software/EDPL/Unicorn/Notices/eclosing8daysprint
EOF

## Example Prereferral
cat << EOF > "$PREREFERRAL"
.folddata
.report
.col 5l,1,73
.language ENGLISH
Thursday, September 21, 2023










.block
          Everytime McBoatface
          12223- 107 A Avenue NW
          Edmonton, AB
          T7P 0Z4
.endblock


.read /software/EDPL/Unicorn/Notices/blankmessage

.block
  1   No one wins alone : a memoir / Mark Messier with Jimmy Roberts.
      Messier, Mark, 1961-
      date billed:9/7/2023     bill reason:LOST         amount due:    \$31.59
.endblock

.block
  2   Freezing cold takes : NFL : football media's most inaccurate
      predictions--and the fascinating stories behind them / Fred Segal.
      Segal, Fred (Sports blogger)
      date billed:9/7/2023     bill reason:LOST         amount due:    \$22.74
.endblock

.block
      =======================================================================

                                 TOTAL FINES/FEES AND UNPAID BILLS:    \$54.33
.endblock

.block
.read /software/EDPL/Unicorn/Notices/prereferralbillclosing
.endblock

.report
.col 5l,1,73
.language ENGLISH
Thursday, September 21, 2023










.block
          Sarah NotMyName Smith
          1234 151 Street NW
          Edmonton, AB
          T7R 1J7
.endblock


.read /software/EDPL/Unicorn/Notices/blankmessage

.block
  1   Myths / Agatha Gregson.
      Gregson, Agatha.
      date billed:9/7/2023     bill reason:LOST         amount due:    \$26.67
.endblock

.block
  2   Room on our rock : there are two sides to every story / Kate & Jol
      Temple ; [illustrated by] Terri Rose Baynton.
      Temple, Kate.
      date billed:9/7/2023     bill reason:LOST         amount due:    \$18.02
.endblock

.block
  3   Asha and Baz meet Mary Sherman Morgan / by Caroline Fernandez ;
      illustrated by Dharmali Patel.
      Fernandez, Caroline (Blogger)
      date billed:9/7/2023     bill reason:LOST         amount due:     \$6.89
.endblock

.block
  4   The cake escape / Swapna Haddow ; [illustrated by] Sheena Dempsey.
      Haddow, Swapna.
      date billed:9/7/2023     bill reason:LOST         amount due:    \$10.41
.endblock

.block
  5   Big problemas / Juana Medina.
      Medina, Juana, 1980-
      date billed:9/7/2023     bill reason:LOST         amount due:     \$7.48
.endblock

.block
      =======================================================================

                                 TOTAL FINES/FEES AND UNPAID BILLS:    \$69.47
.endblock

.block
.read /software/EDPL/Unicorn/Notices/prereferralbillclosing
.endblock

EOF

## Example Prelost
cat << EOF > "$PRELOST"
.folddata
.report
.col 5l,1,73
.language ENGLISH
Thursday, September 21, 2023










.block
          Sharon M Forster
          12345 156 Street
          Edmonton, AB
          T4R 1J4
.endblock


.read /software/EDPL/Unicorn/Notices/prelostoverdue1stprint

  1  call number:CON                                       ID:31221320513224  
     Desert star / Michael Connelly.
     Connelly, Michael, 1956-
     due:9/13/2023,23:59     price:\$29.83    

.read /software/EDPL/Unicorn/Notices/prelostoverdueclosingprint
.report
.col 5l,1,73
.language ENGLISH
Thursday, September 21, 2023










.block
          Joanne Calabrowski
          11843 74 Avenue NW
          Edmonton, AB
          T7G 1V4
.endblock


.read /software/EDPL/Unicorn/Notices/prelostoverdue1stprint

  1  call number:KIN                                       ID:31221318287120  
     Demon Copperhead : a novel / Barbara Kingsolver.
     Kingsolver, Barbara.
     due:9/13/2023,23:59     price:\$31.90    

  2  call number:338.2728 BEA                              ID:31221320517308  
     Ducks : two years in the oil sands / Kate Beaton.
     Beaton, Kate, 1983-
     due:9/13/2023,23:59     price:\$31.57    

.read /software/EDPL/Unicorn/Notices/prelostoverdueclosingprint

EOF

## Run the tests
logit "TEST SCRIPT: == Starting $0 version: $VERSION on $HOST"
logit "TEST: compiling bill notices"
python ${LOCAL_BIN_DIR}/${APP} -s -b10.0 -i${BILLS} $X_ARGS >>${LOG_FILE}
logit " "
logit "TEST: compiling overdue notices"
python ${LOCAL_BIN_DIR}/${APP} -o -s     -i${OVERDUES} $X_ARGS >>${LOG_FILE}
logit " "
logit "TEST: compiling pre-referral notices"
python ${LOCAL_BIN_DIR}/${APP} -r -s     -i${PREREFERRAL} $X_ARGS >>${LOG_FILE}
logit " "
logit "TEST: compiling pre-lost notices"
python ${LOCAL_BIN_DIR}/${APP} -p -s     -i${PRELOST} $X_ARGS >>${LOG_FILE}
logit " "
logit "Cleaning up. The script can be run repeatedly."
# remove the test_report and test_bulletin directories. They will be rebuilt next run.
rm "$BILLS"
# rm $HOLDS
rm "$OVERDUES"
rm "$PREREFERRAL"
rm "$PRELOST"
rm "${BULLETIN_DIR}/blankmessage"
rm "${BULLETIN_DIR}/eclosing"
rm "${BULLETIN_DIR}/eclosing8daysprint"
rm "${BULLETIN_DIR}/overdue8daysprint"
rm "${BULLETIN_DIR}/prelostoverdue1stprint"
rm "${BULLETIN_DIR}/prelostoverdueclosingprint"
rm "${BULLETIN_DIR}/prereferralbillclosing"
deactivate
logit "Done, check the $PRINT_DIR for results."
