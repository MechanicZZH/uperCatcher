import requests
from bs4 import BeautifulSoup
import json
import csv

page = range(50)


def HTMLText(url):
    with open('C:/Users/zhang/PycharmProjects/untitled5/video.csv', 'w', newline='',encoding='UTF-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['标题', '上传日期', 'up主', 'av号', '观看', '弹幕', '评论', '收藏', '硬币', '分享', '点赞'])
        for i in page:

            payload = {'keyword': 'wota', 'page': page[i]}
            headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
                   "Accept-Encoding": "gzip",
                   "Accept-Language": "zh-CN,zh;q=0.8",
                   "Referer": "http://www.bilibili.com/",
                   "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"}
            r = requests.get(url, params=payload, headers=headers)
            r.raise_for_status
            r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, 'html.parser')

            for child in soup.select('.l-item'):
                title = child.a['title']
                tags = child.select('.tags')[0]
                num = tags.select('.watch-num')[0].text.strip()
                hide = tags.select('.hide')[0].text.strip()
                time = tags.select('.time')[0].text.strip()
                upname = tags.select('.up-name')[0].text.strip()
                suburl = child.a['href']
                aid = suburl[suburl.find('av') + 2:suburl.find('?')]
                subhtml = requests.get('https://api.bilibili.com/x/web-interface/archive/stat?aid=' + aid, headers=headers)
                subhtml.encoding = subhtml.apparent_encoding
                infojson = subhtml.text
                infojson = infojson[infojson.find('data') + 6:-1]
                videoinfo = json.loads(infojson)
                videolist = []
                videolist.append([title, time, upname, videoinfo["aid"], videoinfo["view"], videoinfo["danmaku"], videoinfo["reply"],videoinfo["favorite"], videoinfo["coin"], videoinfo["share"], videoinfo["like"]])
                for videoinfo_useful in videolist:
                    print(videoinfo_useful)
                    writer.writerow(videoinfo_useful)

if __name__ == "__main__":
    url = "https://www.bilibili.com/v/dance/otaku/#/47977/0/"
    print(HTMLText(url))