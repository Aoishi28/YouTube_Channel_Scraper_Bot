from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

path='C:\\Users\\Suprakash\\Anaconda3\\chromedriver.exe'
browser=webdriver.Chrome(executable_path=path)

browser.get('https://www.youtube.com/')
time.sleep(10)

channel='' # Mention the channel's name

search=browser.find_element_by_xpath('//*[@id="search"]')
search.click()
search.send_keys(channel)
search.send_keys(Keys.ENTER)

time.sleep(5)

ch=browser.find_element_by_xpath('//*[@id="main-link"]') #Accessing the link of the channel
url=ch.get_attribute('href')

browser.get(url+'/videos') #Accessing the videos of the channel

time.sleep(5)

#Scrolling till the end of the channel so that all videos can be accessed
while True:
    scroll_height = 2000
    h1 = browser.execute_script("return document.documentElement.scrollHeight")
    browser.execute_script(f"window.scrollTo(0, {h1 + scroll_height});")
    time.sleep(1.5)
    h2 = browser.execute_script("return document.documentElement.scrollHeight")
    if h1 == h2:
        break

#Scraping information about the videos
pg=browser.page_source
soup=BeautifulSoup(pg,'lxml')
de=soup.findAll('a',{'class':"yt-simple-endpoint style-scope ytd-grid-video-renderer"}) #Getting all the videos

urls=[]

for i in de:
	u=i.get('href')
	urls.append('https://www.youtube.com'+u) #Since the fetched urls are not complete we need to append -https://www.youtube.com in front to fetch the complete url


name=[]
likes=[]
dislikes=[]
views=[]
date=[]

#Accessing each video and fetching informations like - name,likes,dislikes,views and the release date
for i in urls:
	browser.get(i)
	time.sleep(5)
	
	name.append(browser.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text)
	likes.append(browser.find_element_by_xpath('//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[1]/a').text)
	dislikes.append(browser.find_element_by_xpath('//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[2]/a').text)
	views.append(browser.find_element_by_xpath('//*[@id="count"]/ytd-video-view-count-renderer/span[1]').text)
	date.append(browser.find_element_by_xpath('//*[@id="date"]/yt-formatted-string').text)

#Creating a dataframe to store the information
data = {'Name of the video': name, 'URL': urls,'Number of likes':likes,'Number of dislikes':dislikes,'Views':views,'Release Date':date}  
df=pd.DataFrame(data)

df.to_csv("YouTube_data.csv") #Converting it to a csv file

print("Done !!")