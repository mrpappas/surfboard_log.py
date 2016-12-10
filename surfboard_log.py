import re, itertools, urllib.request, datetime
from bs4 import BeautifulSoup

## set modem's IP Address
ip = 'http://192.168.100.1/cmSignalData.htm'

date = ('Data logged: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))

## adjust signal level tolerance - if not high set to 100

downstream_high = 15
downstream_low = -15
upstream_high = 55
upstream_low = 37
snr_high = 100
snr_low = 30

class Scraper:

    def set_data(target, start):
        for data in td[start:]:
            rawData = data.string
            finishedData = int(re.sub("[^-?\d+(\.\d+)?$]", "", rawData))
            target.append(finishedData)

    def get_average(data):
        average = sum(data[1:]) / len(data)
        return average

    def check_limits(results, high, low, target):
        for result in results[1:]:
            if result <= low:
                target.append(results[0] + ' ' + str(result) + ' dBmV -- WARNING TOO LOW MINIMUM LEVEL: ' + str(low))
            elif result >= high:
                target.append(results[0] + ' ' + str(result) + ' dB -- WARNING TOO HIGH MAXIMUM LEVEL: ' + str(high))
            else:
                target.append(results[0] + ' ' + str(result) + ' DBmV -- in spec')

    def get_errors(unerrored, uncorrected, corrected, store):
        percentage = unerrored / (unerrored + uncorrected + corrected)
        percentage = percentage * 100
        errors.append(str(percentage) + ' % Unerrored Codewords')

    def write_to_log(entries, title):
        with open("modem.log", "a") as f:
            title = title
            f.write('--  ' + title + '  --\n')
            for entry in entries:
                f.write('Channel ' + str(entry[1]) + ' : ' + str(entry[0]) + '\n')
            f.write('--------------------------------------------\n')



try:
    with urllib.request.urlopen(ip) as f:

        soup = BeautifulSoup(f, 'html.parser')
        tables = soup.findAll('table')

        snr = ['Signal to Noise Ratio']
        downstream = ['Downstream Signal']
        upstream = ['Upstream Signal']
        up_channels = ['Upstream Channel']
        down_channels = ['Downstream Channel']
        unerrored = ['Unerrored Codewords']
        correctable = ['Corrected']
        uncorrectable = ['Uncorrected']

        down = []
        up = []
        noise = []

        scraper = Scraper

        for table in tables:
            rows = table.findAll('tr')
            for tr in rows:
                td = tr.findAll('td')
                for data in td:
                    check = data.string

                    if check == 'Signal to Noise Ratio':
                        scraper.set_data(snr, 1)

                    elif data.has_attr('align'):
                        scraper.set_data(downstream, 2)

                    elif check == 'Power Level':
                        scraper.set_data(upstream, 1)

                    elif check == 'Channel ID':
                        if len(td) == 9:
                            if len(down_channels) < 5:
                                scraper.set_data(down_channels, 1)
                                print(down_channels)
                        elif len(td) == 5:
                            scraper.set_data(up_channels, 1)

                    elif check == 'Total Unerrored Codewords':
                        scraper.set_data(unerrored, 2)

                    elif check == 'Total Correctable Codewords':
                        scraper.set_data(correctable, 2)

                    elif check == 'Total Uncorrectable Codewords':
                        scraper.set_data(uncorrectable, 2)


        ##Check results are within specs then write to .log
        with open("modem.log", "a") as f:
            f.write('--------------------------------------------\n')
            f.write('--------------------------------------------\n')
            f.write('-- ' + date + ' --\n')
            f.write('--------------------------------------------\n')
            f.write('--------------------------------------------\n')

        scraper.check_limits(downstream, downstream_high, downstream_low, down)
        down = list(zip(down, down_channels[1:]))
        scraper.write_to_log(down, str(downstream[0]))


        scraper.check_limits(upstream, upstream_high, upstream_low, up)
        up = list(zip(up, up_channels[1:]))
        scraper.write_to_log(up, str(upstream[0]))


        scraper.check_limits(snr, snr_high, snr_low, noise)
        noise = list(zip(noise, down_channels[1:]))
        scraper.write_to_log(noise, str(snr[0]))

        unerrored = scraper.get_average(unerrored)
        correctable = scraper.get_average(correctable)
        uncorrectable = scraper.get_average(uncorrectable)

        errors= []
        scraper.get_errors(unerrored, correctable, uncorrectable, errors)
        with open("modem.log", "a") as f:
            f.write('-- Error Correction --\n')
            f.write(errors[0] + '\n')
            f.write('--------------------------------------------\n')
except:
    with open("modem.log", "a") as f:
        f.write('--------------------------------------------\n')
        f.write('--Something went wrong ' + date + ' --\n')
        f.write('--------------------------------------------\n')
