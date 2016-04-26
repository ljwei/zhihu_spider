# -*- coding:utf-8 -*-
import re
import sys
import json
import functools
import os
import sys
from bs4 import BeautifulSoup
from connection import Connection

reload(sys)
sys.setdefaultencoding('utf8')

addr = 'http://www.zhihu.com'

class Zhihu(object):
    def __init__(self, account='jw-li-15-23'):
        self.account = account

    def ask(self):
        html = Connection.connect(addr + '/people/' + self.account + '/asks')
        soup = BeautifulSoup(html, "html.parser")
        questions = dict()
        for ask in soup.find_all('a', 'question_link'):
            q_str = str(ask.get_text().encode('utf8'))
            q_href = str(addr + str(ask.get('href')))
            questions[q_str] = q_href
        return questions

    def topic(self):
        html = Connection.connect(addr + '/people/' + self.account + '/topics')
        soup = BeautifulSoup(html, "html.parser")
        topics = []
        for topic in soup.find_all('a', 'zm-list-avatar-link'):
            # topic_str = str(topic.strong.get_text())
            topic_href = addr + str(topic.get('href'))
            topics.append(Topic(topic_href))
        return topics

class Topic:
    def __init__(self, url=None):
        self.url = url

    def question(self):
        html = Connection.connect(self.url + '/top-answers')
        soup = BeautifulSoup(html, 'html.parser')
        questions = []
        for ask in soup.find_all('a', 'question_link'):
            # q_str = str(ask.get_text().encode('utf8'))
            q_href = str(addr + str(ask.get('href')))
            yield Question(q_href)

class Question(object):
    def __init__(self, url=None):
        self.url = url
        html = Connection.connect(url)
        self.soup = BeautifulSoup(html, 'html.parser')

    def title(self):
        title = self.soup.find('h2', 'zm-item-title zm-editable-content')
        return title.get_text().strip()

    def question_detail(self):
        question_detail = self.soup.find('div', 'zm-editable-content')
        s = question_detail.get_text()
        d = re.sub('<>', '', s)
        return d.strip()

    def answer_number(self):
        answer_number = self.soup.h3['data-num'].strip()
        return answer_number

    def follower(self):
        follower = self.soup.find('div', 'zg-gray-normal')
        return '-'.join(follower.get_text().split())

    def all_answer(self):
        answer_number = self.answer_number()
        if answer_number == 0:
            print "This question is no answers"
        else:
            re_br = re.compile(r'<br/?>')
            re_allmark = re.compile(r'<[^>]+>',re.S)
            all_answer_list = self.soup.find_all('div', "zm-item-answer  zm-item-expanded") #所有回答列表
            for each in all_answer_list:
                # yield each.h3.get_text()  #答主
                content = str(each.find('div', 'zm-editable-content clearfix'))
                br2n = re.sub(re_br, '\n', content)
                # answer = ''
                # for s in br2n.split('\n'):
                #     answer += re.sub(re_allmark, '', s)
                yield br2n
                
    def save(self, path, filename, pattern):
        title = self.title()
        question_detail = self.question_detail()
        answer_number = self.answer_number()
        followers = self.follower()
        all_answers = self.all_answer()

        full_path = path + filename + '.txt'
        # if sys.platform == 'linux2':
        #     if os.path.exists(os.path.split(path)[0]):
        #         if not os.path.split(path)[1]:
        #             destpath = os.path.split(path)[0] + filename
        #         else:
        #             destpath = path
        #     else:
        #         raise 'You path is not exists'
        # else:
        #     raise 'Other systems such as Windows are not currently supported'
        with open(full_path, pattern) as f:
            f.write('标题：%s \n' % title + '问题详情：%s \n' % question_detail + '回答数：%s \t' % answer_number \
                + ' 关注数：%s \n' % followers)
            index = 1
            for each in all_answers:
                f.write('answer :%d' % index + '\n' + '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n')
                f.write(each + '\n')
                index += 1

