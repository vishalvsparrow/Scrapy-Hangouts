import scrapy
import re
# import urllib
import pandas as pd

# files = os.listdir(os.getcwd())
# print(files[0])

url_1 = 'file:///C:/cool/hello.txt'
url_2 = 'file:///C:/Users/vishal/PycharmProjects/scrape_hangouts/hangouts_scrape/hangouts_scrape/spiders/frame2.htm'

team_a_5_7_730p = 'file:///C:/Users/vishal/PycharmProjects/scrape_hangouts/hangouts_scrape/hangouts_scrape/spiders' \
                  '/TEAM_A_5_10_730p.htm '
team_b_5_7_730p = 'file:///C:/Users/vishal/PycharmProjects/scrape_hangouts/hangouts_scrape/hangouts_scrape/spiders/TEAM_B_5_10_730p.htm'


# response = urllib.urlopen(team_a_5_7_730p)
# print(response.read())


# path_name = 'C:\Users\vishal\PycharmProjects\scrape_hangouts\hangouts_scrape\hangouts_scrape\spiders\frame2.htm'


class HangoutSpider(scrapy.Spider):
    name = "hangout"

    # def start_requests(self):
    #     urls = [team_a_5_7_730p, team_b_5_7_730p]
    #
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    start_urls = [team_b_5_7_730p]

    def parse(self, response):

        # a = response.xpath('//span[@class = "lWfe2d"]/text()')
        # x = response.xpath('//span[@class = "tL8wMe EMoHub"]/text()')

        a = response.xpath('//span[@class = "lWfe2d"]')
        x = response.xpath('//span[@class = "tL8wMe EMoHub"]')

        my_len = len(x)

        final = dict()

        for i in range(0, my_len):

            speech_temp = x[i].re('left;">(.*)</span>')[0]

            if not speech_temp.find('<br>') == -1:
                speech_temp = re.sub('<br>', ". ", speech_temp)

            # speech_temp = re.sub('\u00a0', " ", speech_temp)

            participant = re.findall(']\s(\S.*)\s[(]', a[i].extract())[0]

            # a1.append(speech_temp)
            # b1.append(participant)
            # print(a1,b1)

            final[participant] = speech_temp

            yield {
                'speech': speech_temp,
                'participant': participant,
            }

        print(final.items())
        print("======================/n")
        df = pd.DataFrame(final.items(), columns=['Participant', 'Speech'])
        df.to_csv('test.csv',sep = '\t', encoding= 'utf-8')

        # for i in range(0, my_len):
        #     yield {
        #         'participant': re.findall(']\s(\S.*)\s[(]', a[i].extract())[0],
        #         'speech': x[i].extract(),
        #     }

        # for y in x:
        #     yield {
        #         'speech': y.extract()
        #     }

# ''
# ""

# >>> x = response.xpath('//span[@class = "tL8wMe EMoHub"]') # speech
# lWfe2d
# response.xpath('//span[@class = "lWfe2d"]/text()') # participant
# re.findall(']\s(\S*\s\S)',a.extract_first())
#  re.findall(']\s(\S.*)\s[(]',a[1].extract())

# do not go for //text in the xPath selector
# x[46].re('left;">(.*)</span>')[0]

# if not x46.find("<br>") == -1:
# re.sub("<br>",". ",x46)
