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
- report.sh - fetches the latest mail notice reports, translates them and 'scp's them to the 'reports' directory.
- bulletin.sh - checks any reports in the 'report' directory for all the bulletins that are needed for the reports and 'scp's them
            to the 'bulletins' directory.
- pstopdf.sh - converts any PS file in the 'print' directory into PDF.

## Debugging
Many of the python files contain unit tests to check their own integrity. You can run them with 'python <file>.py [-c]'.
Some useful tests already exist in the make file. 

REMEMBER: when debugging esp. bills, the script will withhold bills that are less than $10.00. This can be confusing because
The sirsi report contains all bills - the results from notice.py will be different. 
