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
1) Find the necessary reports needed for bills, overdues, and holds for the day and copy then to ilsdev 'reports' directory.
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

## Debugging
Many of the python files contain unit tests to check their own integrity. You can run them with 'python <file>.py [-c]'.
Some useful tests already exist in the make file. 

REMEMBER: when debugging esp. bills, the script will withhold bills that are less than $10.00. This can be confusing because
The sirsi report contains all bills - the results from notice.py will be different. 
