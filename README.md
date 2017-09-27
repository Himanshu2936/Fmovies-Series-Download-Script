# Fmovies-Series-Download-Script
Using this script you can download your favorite TV series from Fmovies season by season in single run.

Steps to Run the script

    1- make sure you have installed selenuim,clint and beautifulsoup(bs4) libraries from pip.
    2- download gekodriver and chromedriver from internet and place them into your python36-32 folder.
    gekodriver -- https://github.com/mozilla/geckodriver/releases/tag/v0.19.0
    chromedriver -- https://sites.google.com/a/chromium.org/chromedriver/downloads
    3- Run the script and fill the details.


    NOTE: 1.Enter URL as shown in picture(without clicking the play button).
          2.Enter subtitle no as shown in picture. If there are no subtitles on the page just enter n for subtitles.
          3.If you have slow internet connection then double the time in webdriverwait in line 107 from 30 to 60.
          4.If you get error like ""(_ssl.c:749)"
            run this command   pip install -U requests[security]
