import re, urllib.request, datetime
from bs4 import BeautifulSoup

## set modem's IP Address
ip = 'http://192.168.100.1/cmSignalData.htm'

date = ('Data logged: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))

dashed_line = '--------------------------------------------\n'

## adjust signal level tolerance - if not high set to 100

downstream_high = 10
downstream_low = -10
upstream_high = 53
upstream_low = 37
snr_high = 100
snr_low = 32

class Scraper(object):

    def set_data(self, target, start):
        for data in self.td[start:]:
            rawData = data.string
            finishedData = int(re.sub("[^-?\d+(\.\d+)?$]", "", rawData))
            target.append(finishedData)

    def get_average(self, data):
        average = sum(data[1:]) / len(data)
        return average

    def check_limits(self, results, high, low, target):
        for result in results[1:]:
            if result <= low:
                target.append(results[0] + ' ' + str(result) + ' dB(mV) -- WARNING TOO LOW MINIMUM LEVEL: ' + str(low))
            elif result >= high:
                target.append(results[0] + ' ' + str(result) + ' dB(mV) -- WARNING TOO HIGH MAXIMUM LEVEL: ' + str(high))
            else:
                target.append(results[0] + ' ' + str(result) + ' dB(mV) -- in spec')

    def get_errors(self, unerrored, uncorrected, corrected, store):
        percentage = unerrored / (unerrored + uncorrected + corrected)
        percentage = percentage * 100
        errors.append(str(percentage) + ' % Unerrored Codewords')

    def write_to_log(self, entries, title):
        with open("modem.log", "a") as f:
            title = title
            f.write('--  ' + title + '  --\n')
            for entry in entries:
                f.write('Channel ' + str(entry[1]) + ' : ' + str(entry[0]) + '\n')
            f.write(dashed_line)



    def parse_page(self):
        with urllib.request.urlopen(ip) as f:
            soup = BeautifulSoup(f, 'html.parser')
            tables = soup.findAll('table')

            self.snr = ['Signal to Noise Ratio']
            self.downstream = ['Downstream Signal']
            self.upstream = ['Upstream Signal']
            self.up_channels = ['Upstream Channel']
            self.down_channels = ['Downstream Channel']
            self.unerrored = ['Unerrored Codewords']
            self.correctable = ['Corrected']
            self.uncorrectable = ['Uncorrected']

            self.down = []
            self.up = []
            self.noise = []

            for table in tables:
                rows = table.findAll('tr')
                for tr in rows:
                    self.td = tr.findAll('td')
                    for data in self.td:
                        check = data.string

                        if check == 'Signal to Noise Ratio':
                            self.set_data(self.snr, 1)

                        elif data.has_attr('align'):
                            self.set_data(self.downstream, 2)

                        elif check == 'Power Level':
                            self.set_data(self.upstream, 1)

                        elif check == 'Channel ID':
                            if len(self.td) == 9:
                                if len(self.down_channels) < 9:
                                    self.set_data(self.down_channels, 1)
                                    print(self.down_channels)
                            elif len(self.td) == 5:
                                self.set_data(self.up_channels, 1)

                        elif check == 'Total Unerrored Codewords':
                            self.set_data(self.unerrored, 1)

                        elif check == 'Total Correctable Codewords':
                            self.set_data(self.correctable, 1)

                        elif check == 'Total Uncorrectable Codewords':
                            self.set_data(self.uncorrectable, 1)


            with open("modem.log", "a") as f:
                f.write(dashed_line)
                f.write(dashed_line)
                f.write('-- ' + date + ' --\n')
                f.write(dashed_line)
                f.write(dashed_line)

if __name__ == "__main__":

    scraper = Scraper()
    scraper.parse_page()

    downstream = scraper.downstream
    upstream = scraper.upstream

    down = scraper.down
    up = scraper.up

    down_channels = scraper.down_channels
    up_channels = scraper.up_channels

    snr = scraper.snr
    noise = scraper.noise
    unerrored = scraper.unerrored
    correctable = scraper.correctable
    uncorrectable = scraper.uncorrectable

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
        f.write(dashed_line)
