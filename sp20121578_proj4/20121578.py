import requests
from bs4 import BeautifulSoup
from operator import eq

visited_link = dict()
visited_lst = []
text_number = 1
start_URL = 'http://cspro.sogang.ac.kr/~gr120170213/' #used for starting URL
base_URL = 'http://cspro.sogang.ac.kr/~gr120170213/'  #used for making the URL

def URL_Visited():
	global visited_link

	url_fp = open('URL.txt','w')
	for i in range(len(visited_lst)):
		if eq(visited_lst[i],start_URL):
			continue
		if visited_link[visited_lst[i]] == True:
			url_fp.write(visited_lst[i])
			if i < len(visited_lst)-1:
				url_fp.write('\n')
	url_fp.close()
	return

def writeText(new_text):
	global text_number
	for i in range(1,text_number):
		check_fname = "Output_%04d" % i
		check_fname = check_fname + '.txt'
		check_fp = open(check_fname,'r')
		check_lst = check_fp.readlines()
		check_fp.close()
		check_string = ''
		for j in check_lst:
			check_string = check_string + j
		if eq(new_text,check_string):
			return

	fname_str = "Output_%04d" % text_number
	fname_str = fname_str + '.txt'
	text_fp = open(fname_str,'w')
	text_fp.write(new_text)
	text_number += 1
	text_fp.close()

def crawlWeb(cur_link):
	global visited_link
	global visited_list
	global start_URL

	visited_link[cur_link] = True
	visited_lst.append(cur_link)
	# start of crawling
	try:
		cur_req = requests.get(cur_link);
		if cur_req.ok:
			cur_soup = BeautifulSoup(cur_req.content,'html.parser')
			writeText(cur_soup.get_text())
			new_links = cur_soup.find_all('a')
			new_URL = []
			# find the html string
			for i in new_links:
				html_str = i.get('href')
				if eq(html_str[:1],'?') or eq(html_str[:1],'#'):
					continue
				elif html_str.find('http://') == -1:
					new_URL.append(base_URL+html_str)
				else:
					new_URL.append(html_str)
			
			# check if it is visited. if not visited, recursively crawl
			for url in new_URL:
				if url in visited_link:
					continue
				else:
					crawlWeb(url)
		else:
			visited_link[cur_link] = False
			return

	except requests.exceptions.ConnectionError:
		print("Connection Error.")

crawlWeb(start_URL)
URL_Visited()
