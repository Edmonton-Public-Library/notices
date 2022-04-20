# Customer Notices
'''December 21, 2012'''
The process of running print notices is a series of steps, all of which have been automated with scripts in this directory.

Normally the ILS team receives the notices in their inbox at ilsteam@epl.ca. The notices are produced each weekday moring and sent as an attachment by cron. To see if the job is scheduled type ```crontab -l```.

If that failed for some reason, the whole process with the exception of emailing the results, can be done from the command line using the commands below. The notice PDFs can be found in ```/home/ils/notices/print``` directory.
```bash
ils@epl-ils $ cd /home/ils/notices
ils@epl-ils $ make # or make run
```

## The Process at a Glance
1) Find the necessary reports needed for bills, overdues, and pre-lost for the day and copy then to ilsdev 'reports' directory.
2) Find the bulletins that need to be included in the header or footer of the notices, and copy them to ildsdev 'bulletins' directory.
3) Format the reports with notice.py. Just this step of the conversion can be done by typing 'make test'. This will create PS files 
   in the 'print' directory.
4) Convert PS files to PDF using ghostscript.
5) Optional: email reports. You will need uuencode in the sharutils package to do this.

## Helper scripts
- ```Makefile(.remote)``` - prepares the notices from the command line if required. Normally ```report.sh``` would be scheduled to do this.
- ```report.sh``` - fetches the latest mail notice reports, translates them and 'scp's them to the 'reports' directory.
- ```bulletin.sh``` - checks any reports in the 'report' directory for all the bulletins that are needed for the reports and 'scp's them to the 'bulletins' directory.
- ```pstopdf.sh``` - converts any PS file in the 'print' directory into PDF.

## Installation
The project is managed from the repos server, which at this time is ```ilsdev1.epl.ca```. The Makefile is used to install the scripts into ```ils@epl-ils.epl.ca:/home/ils/notices/bin```. The Makefile.remote is used to run the process by hand on ```ils@epl-ils.epl.ca``` should that be necessary for testing if the scripts need to be re-run. Re-running notices.sh is not dangerous but it will email the PDFs to the mail clerks so let them know before you run it, or just use the ```--test``` switch, and the PDFs will be sent to an alternate address of your choice. See ```notice.sh --help``` for more details.

## Dependencies
The server where this runs as production needs '''ps2pdf14''' which is part of '''GhostScript'''.
```bash
$> sudo apt install ghostscript
```

## Debugging Tips
* Many of the python files contain unit tests to check their own integrity. You can run them with 'python <file>.py [-c]'.

* Some useful tests already exist in the make file. 

* REMEMBER: when debugging esp. bills, the script will withhold bills that are less than $10.00. This can be confusing because
The sirsi report contains all bills - the results from notice.py will be different. 

* To find details about a report check the report name in Workflows >> Reports >> Finished Reports tab. Then on the command line use rptstat to get report info.
```bash
echo "Overdue Notices - Weekdays" | rptstat.pl -t -oDrcC
2022-04-19 05:40:00|Overdue Notices - Weekdays|kyil|/software/EDPL/Unicorn/Rptprint/kyil.prn
```

## Update New Reports HTG and Non-HTG Notices
April 19, 2022  
New notices in effect **April 26**. There _may_ be a requirement to conditionally process reports until then, depending on how missing reports are managed.

1) Create '**Overdue Reminder - 8 Days Print**' which uses 'overdue8daysprint' and 'eclosing8daysprint' as notice text.
2) Create '**PreLost Overdue Notice - HTG Print**' Which uses 'prelostoverdue1stprint' and 'prelostoverdueclosingprint'.
3) Retire '**Overdue Notices - Weekdays**' which used 'stoverdue.print' and 'eplmailclosing'.

### Changes
| **File** | **Changes** |
|:---|:---|
| notices.sh | Modify overdues, add pre-lost. See pre-referral as template. |
| Makefile.remote | Add ```PRE_LOST``` handling. ```ARGS_OVERD``` becomes 8 day notice. |
| report.sh | Modify Overdues, add new section for Pre-Lost. |
| notice.py | Add new report and update overdue code. See pre-referral as template. |
| reportreader.py | Add new report, change overdues. |
| bulletin.sh | no change |
| Makefile | no change |
| pstopdf.sh | no change |
| noticeformatter.py | no change |
| page.py | no change |
| customer.py | no change |