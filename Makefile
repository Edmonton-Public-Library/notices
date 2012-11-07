# copies most rescent files from eplapp for updating to git.
# SERVER=edpl-t.library.ualberta.ca
SERVER=eplapp.library.ualberta.ca
USER=sirsi
REMOTE=~/Unicorn/EPLwork/anisbet/
LOCAL=~/projects/notices/
APP=notice.py
ARGS= --oFile=myOutFile --iFile=myInFile 


run:
	clear
	python ${LOCAL}${APP} ${ARGS}
test:
	clear
	python ${LOCAL}${APP} -v
put: test 
	scp ${LOCAL}${APP} ${USER}@${SERVER}:${REMOTE}
