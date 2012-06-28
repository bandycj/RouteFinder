import  re, os
import urllib2, urllib
import subprocess
from lxml.html import parse
from lxml.cssselect import CSSSelector

DOWNLOAD_LINKS = CSSSelector('td.swa_feature_flightSchedules_download_table_data_downloadLink a')
SCHEDULE_URL = "http://www.southwest.com/flight/view-schedule.html?"

# 0.00
JUNK_DATA_RE = re.compile(r'\s\d\.\d{2}')
# 1628       6:15A  7:15A   12345__ N/S
FLIGHT_RE = re.compile(r'\s([0-9]{1,4})\s+(\d{1,2}:\d{1,2}[A|P]{1})\s{1,2}(\d{1,2}:\d{1,2}[A|P]{1}).*')
#(Effective June 17, 2012 - June 23, 2012)
EFFECTIVE_DATE_RE = re.compile(r'Effective\s(.*)\s-\s(.*)\)')
#To  Houston Hobby (HOU)
DESTINATION_RE = re.compile(r'^\s+To\s+\w+.*\(([A-Z]{3})\)')
#  From  Houston Hobby (HOU)
ORIGIN_RE = re.compile(r'\s+From\s+\w+.*\(([A-Z]{3})\)')
#Dallas Love (DAL)
CURRENT_CITY_RE = re.compile(r'\s+(?!(?:To|From)$).*\(([A-Z]{3})\)')
#http://www.southwest.com/assets/pdfs/schedules/20120701_20120619_1500/bwi.pdf
PDF_LINK_RE = re.compile(r'\/(\d{8}_\d{8}_\d{4})\/([a-z]{3}.pdf)')

def getSchedule(iataCode, date):
    params = {
        'downloadOriginAirport': iataCode,
        'dateFrom': date,
        'dateTo': date,
        }
    urlEncodedParams = urllib.urlencode(params);
    url = SCHEDULE_URL + urlEncodedParams;
    print url
    page = parse(url).getroot()
    page.make_links_absolute()

    schedule = []
    for a in DOWNLOAD_LINKS(page):
        link = a.attrib['href']
        matched = PDF_LINK_RE.search(link)
        if matched is not None:
            fileName = "/tmp/" + matched.group(1) + matched.group(2)
            if os.path.isfile(fileName) is False:
                pdfData = urllib2.urlopen(link).read()
                pdfFile = open(fileName, "wb")
                pdfFile.write(pdfData)
                pdfFile.close()

            schedule.extend(sort(readPdf(fileName)))

    return schedule


def sort(lines=[]):
    data = []
    fromDate = None
    toDate = None
    currentCity = None
    mode = None
    modeCity = None

    for line in lines:
        try:
            matched = JUNK_DATA_RE.search(line)
            if matched is not None:
                continue

            matched = FLIGHT_RE.search(line)
            if matched is not None:
                # Matched flight line
                flight = matched.group(1)
                skd = matched.group(2) + "M"
                if len(skd) < 7:
                    skd = "0" + skd
                ska = matched.group(3) + "M"
                if len(ska) < 7:
                    ska = "0" + ska

                origin = currentCity
                destination = modeCity
                if mode == "from":
                    origin = modeCity
                    destination = currentCity

                data.append({
                    'origin': origin,
                    'destination': destination,
                    'flightNum': flight,
                    'fromDate': fromDate,
                    'toDate': toDate,
                    'skd': skd,
                    'ska': ska,
                    })
                continue

            matched = EFFECTIVE_DATE_RE.search(line)
            if matched is not None:
                # Matched date range
                fromDate = matched.group(1)
                toDate = matched.group(2)
                continue

            matched = DESTINATION_RE.match(line)
            if matched is not None:
                # Matched destination city
                mode = "to"
                modeCity = matched.group(1)
                continue

            matched = ORIGIN_RE.match(line)
            if matched is not None:
                # Matched origin city
                mode = "from"
                modeCity = matched.group(1)
                continue

            matched = CURRENT_CITY_RE.match(line)
            if matched is not None:
                # Matched current city
                currentCity = matched.group(1)
                continue
        except:
            print "Error"
    return data


def readPdf(fileName=None):
    lines = []

    pdfData = ""
    if fileName is not None:
        app = "/usr/bin/pdftotext"

        command = [app, "-layout", fileName, "-"]
        lines.extend(getData(command, CURRENT_CITY_RE))

        columns = ["0", "150", "300", "440"]
        for column in columns:
            command = [
                app,
                "-x", column,
                "-y", "0",
                "-W", "100",
                "-H", "5000",
                "-layout",
                fileName,
                "-"
            ]
            lines.extend(getData(command))
    return lines


def getData(command=None, re=None):
    out = subprocess.check_output(command)
    lines = []
    for line in out.split("\n"):
        lines.append(line)
        if re is not None:
            if re.match(line):
                break
    return lines
