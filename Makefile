# copies most rescent files from eplapp for updating to git.
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



clean:
	-rm *.pyc
