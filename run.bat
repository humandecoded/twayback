@ECHO off

:Input
ECHO Enter Twitter username:
SET /P username=
ECHO Download Tweets from what date? (YYYYMMDD).
ECHO If you don"t care, just leave it blank and press Enter:
SET /P start1=
 IF /i "%start1%"=="" GOTO blankstart
 IF /i NOT "%start1%"=="" GOTO startexists

:blankstart
ECHO Download Tweets until what date? (YYYYMMDD).
ECHO If you don"t care, just leave it blank and press Enter:
SET /P end2=
 IF /i "%end2%"=="" GOTO limitonly
 IF /i NOT "%end2%"=="" GOTO blankstartendexists

:startexists
ECHO Download Tweets until what date? (YYYYMMDD).
ECHO If you don"t care, just leave it blank and press Enter:
SET /P end1=
 IF /i "%end1%"=="" GOTO blankend
 IF /i NOT "%end1%"=="" GOTO startandendexist

:blankstartendexists
ECHO. Do you like a limit on how many Tweets? If so, type the number then press Enter:
SET /P limit4=
 IF /i "%limit4%"=="" GOTO endonly
 IF /i NOT "%limit4%"=="" GOTO endexistslimitexists

:endexistslimitexists
curl.exe web.archive.org/cdx/search/cdx?url=twitter.com/%username%/status^&matchType=prefix^&limit=%limit4%^&to=%end2%^&filter=statuscode:200^&filter=mimetype:text/html -o sample.txt

:startandendexist
ECHO. Do you like a limit on how many Tweets? If so, type the number then press Enter:
SET /P limit1=
 IF /i "%limit1%"=="" GOTO juststartandend
 IF /i NOT "%limit1%"=="" GOTO limited

:juststartandend
curl.exe web.archive.org/cdx/search/cdx?url=twitter.com/%username%/status^&matchType=prefix^&from=%start1%^&to=%end1%^&filter=statuscode:200^&filter=mimetype:text/html -o sample.txt

:limited
curl.exe web.archive.org/cdx/search/cdx?url=twitter.com/%username%/status^&matchType=prefix^&limit=%limit1%^&from=%start1%^&to=%end1%^&filter=statuscode:200^&filter=mimetype:text/html -o sample.txt
:endonly
curl.exe web.archive.org/cdx/search/cdx?url=twitter.com/%username%/status^&matchType=prefix^&to=%end2%^&filter=statuscode:200^&filter=mimetype:text/html -o sample.txt

:blankend
ECHO Do you like a limit on how many Tweets? If so, type the number then press Enter:
SET /P limit2=
 IF /i "%limit2%"=="" GOTO startonly
 IF /i NOT "%limit2%"=="" GOTO startandlimitexist
:startonly
curl.exe web.archive.org/cdx/search/cdx?url=twitter.com/%username%/status^&matchType=prefix^&from=%start1%^&filter=statuscode:200^&filter=mimetype:text/html -o sample.txt

:limitonly
ECHO I see you didn't specify dates. This means the program will download all available deleted Tweets.
ECHO Do you like a limit on how many Tweets? If so, type the number then press Enter:
ECHO If no limit, just leave blank and press Enter. (Beware this might take a long time.)
SET /P limit3=
 IF /i "%limit3%"=="" GOTO all
 IF /i NOT "%limit3%"=="" GOTO justlimit

:startandlimitexist
curl.exe web.archive.org/cdx/search/cdx?url=twitter.com/%username%/status^&matchType=prefix^&from=%start1%^&limit=%limit2%^&filter=statuscode:200^&filter=mimetype:text/html -o sample.txt



:all
curl.exe web.archive.org/cdx/search/cdx?url=twitter.com/%username%/status^&matchType=prefix^&filter=statuscode:200^&filter=mimetype:text/html -o sample.txt

:justlimit
curl.exe web.archive.org/cdx/search/cdx?url=twitter.com/%username%/status^&matchType=prefix^&limit=%limit3%^&filter=statuscode:200^&filter=mimetype:text/html -o sample.txt

:End

python ./tweets1.py

del sample.txt

pip install requests

ECHO Please wait. Twayback is searching far and wide for deleted tweets from %username%. Depending on the number of Tweets, this step might take several minutes, so you can drink some coffee while this is done.

python ./tweets2.py


del temp1.txt
del temp2.txt

@echo off

SET deltw=%username%_deleted_tweets

for /f "delims=" %%a in (temp5.txt) do (
>>"%deltw%.txt" echo wayback_machine_downloader %%a
)

del temp3.txt
del temp4.txt
del temp5.txt

rename %deltw%.txt %deltw%1.txt

copy %deltw%1.txt temp6.txt

@echo off
cls
setlocal EnableDelayedExpansion
set "cmd=findstr /R /N "^^" temp6.txt | find /C ":""

for /f %%a in ('!cmd!') do set number=%%a

@ECHO OFF
:start
SET choice=
SET /p choice=%number% deleted Tweets have been found. Would you like to download them all? [Y or N]:
IF NOT "%choice%"=="" SET choice=%choice:~0,1%
 IF /i "%choice%"=="Y" GOTO yes
 IF /i "%choice%"=="N" GOTO no
IF "%choice%"=="" GOTO no
ECHO "%choice%" is not valid
ECHO.
GOTO start

:no
ECHO Goodbye.
PAUSE
EXIT

:yes
ECHO Sounds good. Here we go.
for /F "tokens=*" %%A in (temp6.txt) do %%A
PAUSE
EXIT

del temp6.txt

ECHO

SetLocal EnableDelayedExpansion

set input=%deltw%1.txt
set output=%deltw%.txt
set "substr=wayback_machine_downloader "

(
    FOR /F "usebackq delims=" %%G IN ("%input%") DO (
        set line=%%G
        echo. !line:%substr%=!
    )
) > "%output%"

EndLocal
exit /b 0

ECHO Yay. Everything's been downloaded. You can find the HTML files for the Tweets inside the folder "websites" in this directory. Also, there's a list of URLs for the deleted Tweets in the text file %deltw$.txt. Have a good day.