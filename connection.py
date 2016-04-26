# -*- coding:utf-8 -*-
__author__ = 'jwli'

import requests
from ConfigParser import ConfigParser

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

class Connection(Singleton):
    conf = ConfigParser()
    conf.read('config.ini')
    cookies = dict(conf._sections['cookies'])
    session = requests.Session()

    @classmethod
    def connect(self, url):
        html = Connection.session.get(url, cookies=Connection.cookies, verify=False).text
        return html
        # r = session.post('http://www.zhihu.com/login/email', data=post_data, headers=header)

    # if r.json()['r'] == 1:
    #     print 'Login Failed, reason is:',
    # for m in r.json()['data']:
    #     print r.json()['data'][m]
    # print 'So we use cookies to login in...'
    # has_cookies = False
    # for key in cookies:
    #     if key != '__name__' and cookies[key] != '':
    #         has_cookies = True
    #         break
    # if has_cookies is False:
    #     raise ValueError('请填写config.ini文件中的cookies项.')
    # else:
        # r = requests.get('http://www.zhihu.com/login/email', cookies=cookies) # 实现验证码登陆
        # session.get('http://www.zhihu.com/login/email', cookies=cookies) # 实现验证码登陆

if '__main__' == __name__:
    c1 = Connection()
    c2 = Connection()
    assert c1 == c2
    assert c1.session == c2.session
    assert Connection.session == c1.session
    print Connection.connect('http://www.zhihu.com/people/jw-li-15-23')