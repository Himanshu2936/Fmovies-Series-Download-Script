import sys
import time
import requests
import os
from clint.textui import progress
from selenium import webdriver
from bs4 import BeautifulSoup as BS
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

name=''

def main():
	print('\nWelcome To Fmovies Download Script!\n')
	name_of_series=input('Enter the name of the series you want to download : ')
	season_no=input('Enter the Season Number : ')
	global name
	name=name_of_series+" "+season_no
	os.makedirs(name,exist_ok=True)
	os.chdir(name)
	primary_page_url=input('Enter the URL of the page for that season : ')
	start_of_episodes=int(input('Enter the Episode Number you want to start download from : '))
	end_of_episodes=int(input('Enter the Episode Number you want to download upto : '))
	print("NOTE : Subtitles will be downloaded only if there is option for downloading subtitle on "+ 
	"the page itself in which Case Enter the 5 digit subtitle no\nFor more details please refer to readme file")
	sub_choice=input('Do you want to download subtitle(y/n) : ')
	if(sub_choice=='y'):
		subtitle_no=int(input('Enter the subtitle Number : '))
	else :
		subtitle_no=-1

	start_of_episodes=start_of_episodes-1
#get ids

	ids=getidsfromurl(primary_page_url,end_of_episodes)
	
#get dwn_link from ids and download episodes
	getdownloadlinks(primary_page_url,ids[start_of_episodes:],start_of_episodes+1,subtitle_no)
	
	
	
def downloadepisode(link,no,ep_no):
	subpre="https://fmovies.is/subtitle/"
	subsuf=".dl?v1"
	local_name=name+" - "+str(ep_no)
	if link!='p':
		if no != -1:
			url=subpre+str(no)+subsuf
			print("downloading subtitle for episode ",ep_no)
			dwnfile(url,local_name+".srt")
		print("downloading episode ",ep_no)
		dwnfile(link,local_name+".mp4")
	
	
	
def dwnfile(url,name):
	rsp = requests.get(url, stream=True)
	length=rsp.headers.get('content-length')
	if length==None:
		with open(name, 'wb') as f:
			for chunk in rsp.iter_content(chunk_size=1024):
				if chunk:
					f.write(chunk)
	else :
		length=int(length)
		with open(name, 'wb') as f:
			for chunk in progress.bar(rsp.iter_content(chunk_size=1024), expected_size=(length/1024) + 1):
				if chunk:
					f.write(chunk)

	
def getidsfromurl(url,no):
	print("Getting ids for episodes")
	rsp=requests.get(url)
	soup=BS(rsp.text,'html.parser')
	ategs=soup.select('a')
	idslist=[]
	count=0;
	for id in ategs:
		if(id.get('data-id')!=None):
			idslist.append(id.get('data-id'))
			count=count+1
		if count==no:
			break
	print("Got all ids for episodes")
	print("It takes time to get download links for Episodes so please Have Patience")
	return idslist

def getdownloadlinks(purl,ids,count,subtitle_no):
	for each_id in ids:
		print("Getting download link for Episode",count)
		url=purl+'/'+each_id
		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		browser=webdriver.Chrome(chrome_options=options)
		browser.get(url)
		try:
			element = browser.find_element_by_class_name('cover')
			element.click()
			if browser.window_handles[1]!=None:
				current=browser.window_handles[0]
				add=browser.window_handles[1]
				browser.switch_to_window(add)
				browser.close()
				browser.switch_to_window(current)
			WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".jw-media.jw-reset")))
			time.sleep(2)
			element2=browser.find_element_by_css_selector(".jw-media.jw-reset")
			html=element2.get_attribute('innerHTML')
			soup=BS(html,'html.parser')
			video = soup.find("video").get("src")
			browser.close()
			if video!=None:
				downloadepisode(video,subtitle_no,count)
		except:
			print("Problem in getting link of Episode ",count)
			browser.close()
		if subtitle_no != -1:
			subtitle_no=subtitle_no+1
		count=count+1

if __name__ == "__main__":
    main()	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	