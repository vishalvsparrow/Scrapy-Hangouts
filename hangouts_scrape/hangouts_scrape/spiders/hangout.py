import scrapy
import re

# import urllib
import pandas as pd

# files = os.listdir(os.getcwd())
# print(files[0])

# url_1 = 'file:///C:/cool/hello.txt'
# url_2 = 'file:///C:/Users/vishal/PycharmProjects/scrape_hangouts/hangouts_scrape/hangouts_scrape/spiders/frame2.htm'

file_name = '04-05-8p-C'
file_to_read = 'file:///C:/Users/vishal/PycharmProjects/scrape_hangouts/hangouts_scrape/hangouts_scrape/spiders' \
                '/TEAM_C_4_5_8p.htm'

# team_a_5_7_730p = 'file:///C:/Users/vishal/PycharmProjects/scrape_hangouts/hangouts_scrape/hangouts_scrape/spiders' \
#                   '/TEAM_A_5_10_730p.htm '
# team_b_5_7_730p = 'file:///C:/Users/vishal/PycharmProjects/scrape_hangouts/hangouts_scrape/hangouts_scrape/spiders' \
#                   '/TEAM_B_5_10_730p.htm '
#
# team_a_3_17_12p = 'file:///C:/Users/vishal/PycharmProjects/scrape_hangouts/hangouts_scrape/hangouts_scrape/spiders' \
#                   '/TEAM_A_3_17_12p.htm '
#
# team_b_3_17_12p = 'file:///C:/Users/vishal/PycharmProjects/scrape_hangouts/hangouts_scrape/hangouts_scrape/spiders' \
#                   '/TEAM_B_3_17_12p.htm '

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

    start_urls = [file_to_read]

    def parse(self, response):

        # a = response.xpath('//span[@class = "lWfe2d"]/text()')
        # x = response.xpath('//span[@class = "tL8wMe EMoHub"]/text()')

        a = response.xpath('//span[@class = "lWfe2d"]')
        x = response.xpath('//span[@class = "tL8wMe EMoHub"]')

        find_stickers = response.xpath('//div[@class = "iiWVtd e7Iaw"]').extract()

        sticker_list = list()

        if not find_stickers == []:
            print("##################################################")
            for i in range(0, len(find_stickers)):
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                sticker_pname = re.findall('title="(.*)"\sstyle', find_stickers[i])[0]
                stick_temp = re.findall('Team\s(.*)\sParticipant\s(\S)', sticker_pname)[0]
                sticker_pname = ''.join(str(i) for i in stick_temp)
                sticker_name = response.xpath('//div[@class = "ZDX4qc"]')[i].extract()
                sticker_name = re.findall('<img\s.*(Callouts_.*).png"', sticker_name)[0]
                sticker_list.append({sticker_pname: sticker_name})

        my_len = len(x)

        final = list()

        for i in range(0, my_len):

            extract_speech = x[i].re('left;">(.*)</span>')

            if not extract_speech == []:
                speech_temp = extract_speech[0]
            else:
                speech_temp = x[i].re('left;">(.*)')[0]

            if not speech_temp.find('<br>') == -1:
                speech_temp = re.sub('<br>', ". ", speech_temp)

            if not speech_temp.find('<span data-emo=') == -1:
                emoji = re.findall('<span data-emo=\"(\S*)\"', speech_temp)[0]
                speech_temp = re.sub('<span data-emo=.*</div></span>', emoji, speech_temp)  # find_emo

            # speech_temp = re.sub('\u00a0', " ", speech_temp)

            participant = re.findall(']\s(\S.*)\s[(]', a[i].extract())[0]

            if participant.find('Study-Facilitator A') == -1:
                participant_temp = re.findall('Team\s(.*)\sParticipant\s(\S)', participant)[0]
                participant_temp = ''.join(str(i) for i in participant_temp)
            else:
                participant_temp = participant

            # a1.append(speech_temp)
            # b1.append(participant)
            # print(a1,b1)

            yield {
                "Speech": speech_temp,
                "Participant": participant_temp,
            }

            # if not speech_temp.find('\xa0') == -1:

            final.append({participant_temp: speech_temp})

            # print(final.items())
            # print("======================/n")
            # df = pd.DataFrame(final.items(), columns=['Participant', 'Speech'])
            # df.to_csv('test.csv', sep='\t', encoding='utf-8')

            # for i in range(0, my_len):
            #     yield {
            #         'participant': re.findall(']\s(\S.*)\s[(]', a[i].extract())[0],
            #         'speech': x[i].extract(),
            #     }

            # for y in x:
            #     yield {
            #         'speech': y.extract()
            #     }

        for s in sticker_list:
            final.append(s)
        # print(final)
        # print("DAB==================================DAB")
        list_again = list()
        for f in final:
            for k, v in f.items():
                # print (k, v)
                list_again.append((k, v))

        # print(list_again)
        # list_again.encode("utf-8")

        df = pd.DataFrame(list_again)
        # df.encode("utf-8")
        # df.columns("Participant", "Speech")
        df.columns = ['Speech', 'Participant']
        df.to_csv(file_name+'.csv', encoding='utf-8', index=False)

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

# "iiWVtd e7Iaw" is the div class for those nasty stickers
# find_stickers = response.xpath('//div[@class = "iiWVtd e7Iaw"]').extract()
