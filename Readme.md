# Changes
| **File** | **Changes** |
|:---|:---|
| notices.sh | Added `--pdf` switch. |
| Makefile.remote | No change. |
| report.sh | Added `--reprint` and `--code` switches for printing reports from dates other than today. |
| notice.py | Added `--pdf` and `--font` switches. |
| reportreader.py | Cleaned code and added `PdfNoticeFormatter`. Uses report date not current date. |
| bulletin.sh | No change. |
| Makefile | Added `test` and `clean` rules. |
| pstopdf.sh | Made optional if using `notice.py --pdf`. |
| noticeformatter.py | No change. |
| page.py | Now included debugging registration marks and `PdfPage`. |
| customer.py | No change. |

## Testing
There are several levels of tests that can be done on this application and its components. 
* `notices.sh` has a `-t` switch which overrides the default mailing address, so you can run in the production setting and have them mailed. **Running this script will remove any existing \*.ps and \*.pdf so back them up so you can compare output.**
* You can run `testnotices.sh` which will create some test directories add some canned reports, and smoke test the system without fetching reports from the ILS.
* At the lowest level you can run the doctests on all the files (except `notice.py`). That is done as follows.
  1) Change into the bin directory.
  2) Activate the virtual environment with `. ../venv/bin/activate`.
  3) On the command line run `python page.py`... repeating for `*.py` files (except `notice.py`).
  5) `reportreader.py` has canned reports as dependencies. They can be found in `bin_tests.tar`. Just untar the file in the current directory to install them, then run `python reportreader.py`. 
  6) Optional: clean up these directories after checking the output. 

## Deploying
There are two `Makefile`s; one called `Makefile` which manages deployment to a remote production server. The other, `Makefile.remote` gets renamed and copied to production. Its job is to document and perform all tests. 

To deploy this application, change the destination server hostname and from the command line type the following.
```bash 
make # Fires the default rule: 'production'.
     # Copies all the required files to the production server 
     # and renames 'Makefile.remote' to 'Makefile' on the remote server.
     # To test ssh to the production server and type the following.
make test
make test_pdf
```

# Customer Notices
**August 22, 2023**
Added argument handling for `report.sh` to allow it to process a specific report by sched ID. See `--reprint` and `--code` in `report.sh`.
Changed the code in the report generator to use the report date, not the current date.

**December 21, 2012**
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
- ```Makefile(.remote)``` - **Required** prepares the notices from the command line if required. Normally ```report.sh``` would be scheduled to do this.
- ```report.sh``` - **Required** fetches the latest mail notice reports, translates them and 'scp's them to the 'reports' directory.
- ```bulletin.sh``` - **Required** checks any reports in the 'report' directory for all the bulletins that are needed for the reports and 'scp's them to the 'bulletins' directory.
- ```pstopdf.sh``` - Optional, converts any PS file in the 'print' directory into PDF. Not required if `--pdf` switch is used on `notice.py`.

## Installation
1) The current version uses `reportlab` pdf libraries with `pip install reportlab`. This can be done in a virtual environment.
2) Clone the [git repo from here](https://github.com/Edmonton-Public-Library/notices).
3) Configure the `Makefile` to suit your site.
4) Test the application with `make test`.
5) Type `make production`.


The project is managed from the repos server, which at this time is ```ilsdev1.epl.ca```. The Makefile is used to install the scripts into ```ils@epl-ils.epl.ca:/home/ils/notices/bin```. The Makefile.remote is used to run the process by hand on ```ils@epl-ils.epl.ca``` should that be necessary for testing if the scripts need to be re-run. Re-running notices.sh is not dangerous but it will email the PDFs to the mail clerks so let them know before you run it, or just use the ```--test``` switch, and the PDFs will be sent to an alternate address of your choice. See ```notice.sh --help``` for more details.

## Dependencies
If you are generating PDFs from an intermediate PS files the server will need `ps2pdf` which is part of `GhostScript`. It can be installed as follows.
```bash
$> sudo apt install ghostscript
```

If you are generating PDFs directly, install [reportlab as described here](#installation).

## Debugging Tips
* Many of the python files contain unit tests to check their own integrity. You can run them with 'python <file>.py [-c]', `make test` from the cloned repo directory. 

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
