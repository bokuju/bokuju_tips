#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate
from email import Charset

import mail_conf as conf

#Charset.add_charset('shift_jis', Charset.QP, Charset.BASE64, 'shift_jis')
#Charset.add_codec('shift_jis', 'cp932')

def send(from_addr, to_addr, msg):
    s = smtplib.SMTP(conf.server, conf.port)
    s.ehlo()
    #s.starttls()
    s.ehlo()
    s.login(conf.auth_user, conf.auth_passwd)
    s.sendmail(from_addr, to_addr, msg.as_string())
    s.close()
    pass

def create_message(from_addr, to_addr, subject, body):
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = from_addr
    if isinstance(to_addr, list) == True:
        for _a in to_addr:
            msg['To'] = _a
            print _a
    else:
        msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg

def emoji_filter(msg):
    import string
    _emoji = {
        'hare':u'\uE63E',
        'kumori':u'\uE63F',
        'ame':u'\uE640',
        'yuki':u'\uE641',
    }

    try:
        msg = string.replace(msg, u'晴', _emoji['hare'])
        msg = string.replace(msg, u'曇', _emoji['kumori'])
        msg = string.replace(msg, u'雨', _emoji['ame'])
        msg = string.replace(msg, u'雪', _emoji['yuki'])
    except e:
        return None

    return msg

if __name__ == '__main__':
    from get_otenki import Otenki

    o = Otenki()
    _td_dom = o.get_today_dom()
    _td_weather_info = o.get_weather_info(_td_dom)
    _td_temp_info = o.get_temp_info(_td_dom)
    _td_rain_info = o.get_rain_info(_td_dom)
    _td_nature_info = o.get_nature_info(_td_dom)

    from_addr = conf.mail_from
    to_addr = conf.rcpt_to
    body = ""
    body += u"""\
- 降水確率 -
"""
    for _n in range(len(_td_rain_info)):
        body += u"""\
%(time)-5s : %(probability)-3s
""" % _td_rain_info[_n]
    body += u"""\
- 気温 -
最高 : %(high)s
最低 : %(low)s
""" % _td_temp_info
    body += u"""\
- その他 -
風 : %(wind)s
波 : %(wave)s
""" % _td_nature_info
    subject = "%(date)s : %(status)s" % _td_weather_info
    subject = emoji_filter(subject)
    msg = create_message(from_addr, to_addr, subject, body)
    send(from_addr, to_addr, msg)
