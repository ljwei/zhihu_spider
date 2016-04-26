# -*- coding:utf-8 -*-

__author__ = 'jwli'

from zhihu import Zhihu
from connection import Connection

conn = Connection()

my = Zhihu()
topic_count = 1
for topic in my.topic():
    print topic.url
    question_count = 1
    for question in topic.question():
        try:
            print question.url
            question.save('./result/', str(topic_count) + '-' + str(question_count), 'w')
            question_count += 1
        except Exception as e:
            continue
    topic_count += 1

#有些问题在question/23905111之后还有类似#12817817的后缀，请删除之
# question = Question('https://www.zhihu.com/explore/recommendations', session)
# print question.title()  #问题的标题
# print question.question_detail()  #问题的详情
# print question.answer_number()   #问题的回答数
# print question.follower()    #问题的关注数


#会打印出问题的每个答案，返回的是一个generator
# answers = question.all_answer()
# for each in answers:
#     print each

#如果你需要保存，第二个参数是保存文件的路径，第三个参数是文件打开的读写模式。
#如果你要指定文件   /home/path/a.txt
#如果你要指定路径  /home/path/dir/   会在此路径下生成以问题标题为名的txt文件
# question.save(answers, '.', 'w')