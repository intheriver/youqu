# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import hashlib   
import log4j
import os


class Youqu(object):
    def __init__(self,userName,userPass):
        self.__userName__ = userName
        self.__userPass__ = userPass
        self.__yqVer__ = "V2.1.4"
        self.__yqPlatform__ = "andriod"
        self.__userAgent__ = "okhttp/3.3.1"
        self.__loginUrl__ = "http://common.iyouqu.com.cn:8080/app/user/service.do"
        self.__signUrl__ = "http://iyouqu.com.cn:8080/app/group/service.do"
        self.__headers__ = {
            "User-Agent":self.__userAgent__,
            "YQ-Version":self.__yqVer__,
            'YQ-Platform':self.__yqPlatform__
        }
        self.__loginResponse__ = None
        self.__groupInfo__ = None
        self.__articleMap__ = {}
        #self.__userCacheFile__ = ".cache"
    def login(self):
        textData = {
            "device":"FRD-AL00",
            "mobile":self.__userName__,
            "msgId":"APP129",
            "password":self.md5(self.__userPass__),
            "pushType":1,
            "registrationId":"180bfe837d914d67a61ab3b89015cb13",
            "system":"7.0",
            "systemType":"1",
            "version":self.__yqVer__
        }
        reqData = {"text":json.dumps(textData)}
        headers = self.__headers__
        req = urllib2.Request(url = self.__loginUrl__,data = urllib.urlencode(reqData),headers = headers)
        res_data = urllib2.urlopen(req)
        content = res_data.read()
        # fp = open(self.__userCacheFile__, 'w')
        # fp.write(content)
        # fp.close()
        self.__loginResponse__ = json.loads(content)
        if '0' == self.__loginResponse__["code"]:
            self.__headers__["YQ-Token"] = self.__loginResponse__["resultMap"]["userInfo"]["usertoken"]
            log4j.info("login success,token:" + self.__headers__["YQ-Token"])
            return 0
        else:
            log4j.error("login failed,reason:" +  self.__loginResponse__["message"])
            return -1
    def signIn(self,groupName,city = u"武汉市", country = u"中国",province = u"湖北省",latitude = 30.452684,longitude = 114.431715,position = u"在烽火通信高新四路研发中心签到啦!"):
        textData = {
            "city":city,
            "country":country,
            "groupId":self.getGroupId(groupName),
            "imei":"qrre/poND6REBvagI60UNA\u003d\u003d",
            "latitude":latitude,
            "longitude":longitude,
            "msgId":"APP086",
            "position":position,
            "province":province,
            "token":"",
            "userId":self.__loginResponse__["resultMap"]["userInfo"]["id"],
            "userName":self.__loginResponse__["resultMap"]["userInfo"]["name"]
        }
        #textData["userId"] = 100
        reqData = {"text":json.dumps(textData)}
        req = urllib2.Request(url = self.__signUrl__,data = urllib.urlencode(reqData),headers = self.__headers__)
        res_data = urllib2.urlopen(req)
        response = json.loads(res_data.read())
        if '0' == response["code"]:
            log4j.info("success")
            return 0
        else:
            log4j.error("faild to signIn " + str(groupName) + ",reason:" + response["message"])
            return -1
    def md5(self,str):
        m2 = hashlib.md5()
        m2.update(str)
        return m2.hexdigest()
    def updateGroupList(self):
        textData = {
            "msgId":"APP078",
            "userId":self.__loginResponse__["resultMap"]["userInfo"]["id"]
        }
        reqData = {"text":json.dumps(textData)}
        req = urllib2.Request(url = "http://common.iyouqu.com.cn:8080/app/group/service.do",data = urllib.urlencode(reqData),headers = self.__headers__)
        res_data = urllib2.urlopen(req)
        response = json.loads(res_data.read())
        self.__groupInfo__ = response["resultMap"]["objList"]
        return None
    def getGroupId(self,name=""):
        if self.__groupInfo__ is None:
            self.updateGroupList()
        groupList = self.__groupInfo__
        # print groupList
        for group in groupList:
            if name == group["name"]:
                return int(group["id"])
        log4j.error("specified group:" + str(name) + " is not found")
        return None
    def delCommoent(self,commentId):
        textData = {
            "msgId":"APP054",
            "commentId":commentId,
            "userId":self.__loginResponse__["resultMap"]["userInfo"]["id"]
        }
    def articleComment(self,keyWord,comment = u"赞"):
        articleInfo = self.getArticleInfo(keyWord)
        if None == articleInfo:
            return
        if 1 == articleInfo["objectType"] or 3 == articleInfo["objectType"]:
            targetId = 2
        else:
            targetId = articleInfo["objectType"]
        textData = {
            "content":comment,
            "msgId":"APP039",
            "targetId":articleInfo["id"],
            "targetType":targetId,
            "userId":self.__loginResponse__["resultMap"]["userInfo"]["id"]
        }
        reqData = {"text":json.dumps(textData)}
        req = urllib2.Request(url = "http://iyouqu.com.cn:8080/app/service.do",data = urllib.urlencode(reqData),headers = self.__headers__)
        res_data = urllib2.urlopen(req)
        response = json.loads(res_data.read())
        print response
        if '0' == response["code"]:
            log4j.info("success")
        else:
            log4j.error("faild to vote commemt:<" + articleInfo["title"] + ">,reason:" + response["message"])
    def articleVote(self,keyWord):
        articleInfo = self.getArticleInfo(keyWord)
        if None == articleInfo:
            return
        if 4 == articleInfo["objectType"]:
            textData = {
                "articleId":articleInfo["id"],
                "msgId":"ARTICLE_VOTE",
                "userId":self.__loginResponse__["resultMap"]["userInfo"]["id"]
            }
            requestUrl = "http://iyouqu.com.cn:8080/app/magazine/service.do"
        elif 1 == articleInfo["objectType"] or 3 == articleInfo["objectType"]:
            textData = {
                "msgId":"APP010",
                "objectId":articleInfo["id"],
                "opinion":0,
                "userId":self.__loginResponse__["resultMap"]["userInfo"]["id"]
            }
            requestUrl = "http://iyouqu.com.cn:8080/app/newsActivity/service.do"
        else:
            log4j.error("error:unkown objectType:" + str(articleInfo["objectType"]))
            return
        reqData = {"text":json.dumps(textData)}
        req = urllib2.Request(url = requestUrl,data = urllib.urlencode(reqData),headers = self.__headers__)
        res_data = urllib2.urlopen(req)
        response = json.loads(res_data.read())
        if '0' == response["code"]:
            log4j.info("success")
        else:
            log4j.error("faild to vote article:<" + str(articleInfo["title"]) + ">,reason:" + response["message"])
    def articlePreview(self,keyWord):
        articleInfo = self.getArticleInfo(keyWord)
        if None == articleInfo:
            return
        if 4 == articleInfo["objectType"]:
            textData = {
                "articleId":articleInfo["id"],
                "isShow":"true",
                "msgId":"ARTICLE_DETAIL",
                "userId":self.__loginResponse__["resultMap"]["userInfo"]["id"]
            }
            requestUrl = "http://iyouqu.com.cn:8080/app/magazine/service.do"
        elif 1 == articleInfo["objectType"] or 3 == articleInfo["objectType"]:
            textData = {
                "msgId":"APP009",
                "objectId":articleInfo["id"],
                "opinion":0,
                "userId":self.__loginResponse__["resultMap"]["userInfo"]["id"]
            }
            requestUrl = "http://iyouqu.com.cn:8080/app/newsActivity/service.do"
        else:
            log4j.error("error:unkown objectType:" + str(articleInfo["objectType"]))
            return
        reqData = {"text":json.dumps(textData)}
        try:
            req = urllib2.Request(url = requestUrl,data = urllib.urlencode(reqData),headers = self.__headers__)
            res_data = urllib2.urlopen(req)
            response = json.loads(res_data.read())
            if '0' != response["code"]:
                log4j.error("faild to preview <" + str(articleInfo["title"]) + ">,reason:" + response["message"])
            else:
                log4j.info("success")
        except Exception as ex:
            print ex
    def getAriticlList_t(self,title = None , source = None ):
        kw = u"光配线"
        article_list = []
        index = 0
        while 1:
            print("index:" + str(index))
            textData = {
                "department":"02A20000",
                "index":str(index),
                "keyword":kw[0:5],
                "msgId":"APP011",
                "userId":self.__loginResponse__["resultMap"]["userInfo"]["id"]
            }
            reqData = {"text":json.dumps(textData)}
            req = urllib2.Request(url = "http://iyouqu.com.cn:8080/app/newsActivity/service.do",data = urllib.urlencode(reqData),headers = self.__headers__)
            res_data = urllib2.urlopen(req)
            response = json.loads(res_data.read())
            if 0 == int(response["code"]):
                round_list = response["resultMap"]["newsList"]
                if 0 == len(round_list):
                    break
                index = index + len(round_list)
                for articleInfo in round_list:
                    print articleInfo
                    try:
                        print articleInfo["title"]
                        if articleInfo.has_key("source"):
                            print articleInfo["source"]
                    except Exception as ex:
                        print ex
                    if ((title is None) or (title in articleInfo["title"])) \
                        and ((source is None) or (articleInfo.has_key("source") and source in articleInfo["source"])):
                        print "yes+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                        article_list.append(articleInfo) 
                    else:
                        print "no"
            else:
                print response["message"]
                break
        return article_list
    def getArticleInfo(self,keyWord):
        if self.__articleMap__.has_key(keyWord):
            return self.__articleMap__[keyWord]
        textData = {
            "department":"02A20000",
            "index":"0",
            "keyword":keyWord[0:5],
            "msgId":"APP011",
            "userId":self.__loginResponse__["resultMap"]["userInfo"]["id"]
        }
        reqData = {"text":json.dumps(textData)}
        req = urllib2.Request(url = "http://iyouqu.com.cn:8080/app/newsActivity/service.do",data = urllib.urlencode(reqData),headers = self.__headers__)
        res_data = urllib2.urlopen(req)
        response = json.loads(res_data.read())
        if '0' == response["code"]:
            articleList = response["resultMap"]["newsList"]
            if 0 == len(articleList):
                log4j.error("no search result")
                return None
            for i in range(0,len(articleList)):
                articleInfo = articleList[i]
                if keyWord in articleInfo["title"]:
                    self.__articleMap__[keyWord] = articleInfo
                    log4j.info("matched article:" + articleInfo["title"] + ",objectType:" + str(articleInfo["objectType"]))
                    return articleInfo
            log4j.error("error:cannot match " + keyWord + " in search result")
            return None
        else:
            log4j.error(response["message"])
            return None
