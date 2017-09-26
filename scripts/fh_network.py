# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import hashlib   
import log4j
import os
import encrypt
import common

def login():
    url = "http://202.103.24.68:90/login"
    reqData = {
        "uri":"",
        "terminal":"pc",
        "login_type":"login",
        "check_passwd":"0",
        "show_tip":"block",
        "show_change_password":"none",
        "short_message":"none",
        "show_captcha":"none",
        "show_read":"block",
        "show_assure":"none",
        "username":common.mail_addr[0:common.mail_addr.index('@')],
        "assure_phone":"",
        "password1":"do not need,password is in md6 format",
        "password":encrypt.md6(common.mail_pw),
        "new_password":"",
        "retype_newpassword":"",
        "captcha_value":"",
        "save_user":"1",
        "save_pass":"1",
        "read":"1"
    }
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Content-Type":"application/x-www-form-urlencoded"
    }
    rv_code = -1
    try:

        req = urllib2.Request(url = url,data = urllib.urlencode(reqData),headers = headers)
        res_data = urllib2.urlopen(req)
        content =  res_data.read()
        if r"submitbutton('logout')" in content:
            log4j.info("login success")
            rv_code  = 0
        else:
            log4j.error("login faild:" + content)
    except Exception as ex:
       log4j.error("login faild:" + ex)
    return rv_code

login()
