#!/usr/bin/env python3

class RedditPost(object):

	comments = []
	def __init__(self, url):
		self.url = url

	def __repr__(self):
		return 'RedditPost({})'.format(self.url)

	def __str__(self):
		return '{}'.format(self.title)

	def set_title(self, title):
		self.title = title

	def set_op_name(self, op_name):
		self.op_name = op_name

	def set_op_age(self, op_age):
		self.op_age = op_age

	def set_op_points(self, op_points):
		self.op_points = op_points

	def set_op_content(self, op_content):
		self.op_content = op_content

	def add_comment(self, comment):
		self.comments.append(comment)

class RedditComment(RedditPost):

	def __repr__(self):
		return 'RedditComment({})'.format(self.url)

	def __str__(self):
		return '{}'.format(self.content)

	def set_age(self, age):
		self.age = age

	def set_user(self, user):
		self.user = user

	def set_points(self, points):
		self.points = points

	def set_content(self, content):
		self.content = content