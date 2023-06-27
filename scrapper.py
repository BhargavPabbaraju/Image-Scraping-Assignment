from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
class Scrapper:
    def __init__(self,url,size=5):
        self.url = url
        self.size = size

        self.driver = webdriver.Edge()
        self.driver.get(url)
        self.driver.find_elements("id","video-title-link")[1].send_keys(Keys.PAGE_DOWN)
        time.sleep(5)
        self.html = self.driver.page_source
        self.html = bs(self.html,'html.parser')
        

    def scrape(self,start=0):
        
        
        self.videos = []
        vids = self.html.find_all("ytd-rich-item-renderer") [start:self.size]
        for vid in vids:
            record={}
            #video url
            record['vid_url'] = vid.find('ytd-thumbnail').find('a')['href']
            try:
                #image thumbnail
                record['thumbnail'] = vid.find('yt-image').find('img')['src']
            except:
                print(vid.find('yt-image').find('img'))
                record['thumbnail'] = ''
            #title
            record['title'] = vid.find('a',{'id':'video-title-link'}).find('yt-formatted-string').text
            #views
            record['views'] = vid.find_all('span',{'class':'inline-metadata-item style-scope ytd-video-meta-block'})[0].text
            record['views'] = record['views'][:record['views'].find(' ')]
            #posted time
            record['posted_time'] = vid.find_all('span',{'class':'inline-metadata-item style-scope ytd-video-meta-block'})[1].text
            self.videos.append(record)
        
        self.driver.close()
    
    
    def to_csv(self,filename='data.csv'):
        self.headings = ['Title','Video url','Thumbnail','Views','Posted time']
        with open(filename,'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.headings)
            for vid in self.videos:
                row = [vid['title'],vid['vid_url'],vid['thumbnail'],vid['views'],vid['posted_time']]
                writer.writerow([x.encode('utf-8') for x in row])
                
    