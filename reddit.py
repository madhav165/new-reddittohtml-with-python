#!/usr/bin/env python3

from reddit_posts import RedditPost, RedditComment
import requests
from bs4 import BeautifulSoup
import pickle

url = input('Reddit URL: ')
rp = RedditPost(url)

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3472.3 Safari/537.36'
}

r = requests.get(url, headers=headers)

if r.status_code != 200:
	print ('Could not make successful request. Try again later.')
	exit()

# with open('reddit_file.pickle', 'wb') as f:
# 	pickle.dump(r, f, pickle.HIGHEST_PROTOCOL)

# try:
# 	with open('reddit_file.pickle', 'rb') as f:
# 		r = pickle.load(f)
# except Exception as e:
# 	print ('Encountered an exception. Exiting.')
# 	exit()

soup = BeautifulSoup(r.content, 'lxml')

body = soup.body
main_div = body.div.div.find_all('div', recursive=False)[1]\
.div.div.div.find_all('div', recursive=False)[-1].div.div.div\
.find_all('div', recursive=False)[-1].find_all('div', recursive=False)[-1]\
.div.div

content_divs = main_div.find_all(True, recursive=False)
op_div = content_divs[0].div.div
comments_div = content_divs[-1].div

def clean_soup(soup):
	for tag in soup.recursiveChildGenerator():
		try:
			tag.attrs = []
		except AttributeError: 
			# 'NavigableString' object has no attribute 'attrs'
			pass
	return soup

op_content_divs = op_div.find_all('div', recursive=False)

op_points = op_content_divs[0].div.div.text
rp.set_op_points('{} points'.format(op_points))

op_name = op_content_divs[1].div.div.div.a.text[2:]
op_age = op_content_divs[1].div.div.find('a', recursive=False).text
rp.set_op_age(op_age)
rp.set_op_name(op_name)

post_title = op_content_divs[2].span.h2
post_title.attrs=[]
rp.set_title(post_title)

op_content_div = op_content_divs[3]
op_content_div.attrs=[]
op_content = clean_soup(op_content_div)
rp.set_op_content(op_content)

comments_divs = comments_div.find_all('div', recursive=False)

# for tag in comments_divs.find_all(True, recursive=False):
	# print (tag.name)

for comment_div in comments_divs:
	comment_divs = comment_div.div.div.find_all('div', recursive=False)[-1].find_all('div', recursive=False)[-1].find_all('div', recursive=False)
	comment_context_div = comment_divs[0]
	comment_user = comment_context_div.div.a.text
	comment_points = comment_context_div.find('span', recursive=False).text
	comment_age = comment_context_div.find('a', recursive=False).span.text
	comment_content_div = comment_divs[1].find('div', recursive=False)
	comment_content_div.attrs=[]
	comment_content = clean_soup(comment_content_div)
	rc = RedditComment(url)
	rc.set_user(comment_user)
	rc.set_age(comment_age)
	rc.set_points(comment_points)
	rc.set_content(comment_content)
	rp.add_comment(rc)

file_name = '{}.html'.format(rp.title.text.replace('/',' '))
with open(file_name, 'w') as f:
	f.write('<!DOCTYPE html>')
	f.write('<html>')
	f.write('<head>')
	f.write('{}'.format(soup.title))
	f.write('</head>')
	f.write('<body>')
	f.write('{}'.format(rp.title))
	f.write('<div><b>{}</b> (<i>{} - {}</i>)</div>'.format(rp.op_name, rp.op_points, rp.op_age))
	f.write('{}'.format(rp.op_content))
	f.write('<h3>Comments</h3>')
	for comment in rp.comments:
		f.write('<div><b>{}</b> (<i>{} - {}</i>)</div>'.format(comment.user, comment.points, comment.age))
		f.write('{}'.format(comment))
	f.write('</body>')
	f.write('</html>')
