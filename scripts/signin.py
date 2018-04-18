# -*- coding: utf-8 -*-

from youqu import Youqu
from mail import sendmail
import time
from optparse import OptionParser
import log4j


def main():
    usage = "usage: %prog -u <username> -p <password> -g <group> -m <email> -l <location>"  
    parser = OptionParser(usage = usage)
    parser.add_option('-u','--username', dest ='username', type='string', help = 'specify the username')
    parser.add_option('-p','--passwd',dest = 'passwd', type = 'string', help = 'specify the password')
    parser.add_option('-g','--group',dest = 'group', type = 'string', help = 'specify the groupName')
    parser.add_option('-m','--mail',dest = 'mail', type = 'string', help = 'specify the email address')
    parser.add_option('-l','--location',dest = 'location', type = 'string', help = 'specify the location')
    (options, args) = parser.parse_args()
    if (options.username == None) | (options.passwd == None) | (options.group == None) | (options.mail == None):
        print parser.usage
        exit(0)
    if options.location == None:
        location = u"在烽火通信高新四路研发中心签到啦!"
    else:
        location = (options.location).decode("gbk");
    log4j.init()
    
    userName = options.username
    userPass = options.passwd
    groupName = (options.group).decode("gbk")
    to_addr = options.mail
    status = "fail"

    start_time = time.strftime('%y-%m-%d %H:%M:%S',time.localtime(time.time()))
    user = Youqu(userName,userPass)
    status_list = []

    article_preview_details = ""

    if 0 == user.login():
        for group in groupName.split(","):
            status = "fail"
            if 0 == user.signIn(groupName = group , position = location):
                status = "success"
            status_list.append({"group":group,"status":status})

        articles = user.getLatestArticles(19)
        for article in articles:
            if 0 == user.articlePreview(article):
                article_preview_details += ("%-15s : %s\n" % (article["title"], "+1"))
            else:
                article_preview_details += ("%-15s : %s\n" % (article["title"], "+0"))

    stop_time = time.strftime('%y-%m-%d %H:%M:%S',time.localtime(time.time()))
    msg_content = ""
    msg_content += ("%-07s: %s\n"%("user" , userName))
    for item in status_list:
        msg_content += ("%-07s: %s ===> %s\n"%("group" , item["group"] , item["status"]))
    msg_content += ("%-07s: %s\n"%("start" , start_time))
    msg_content += ("%-07s: %s\n"%("stop" , stop_time))

    msg_content += ( "\n" + ("*" * 80) + "\n")
    msg_content += article_preview_details
    
    sendmail(to_addr = to_addr , content = msg_content)

if __name__ == '__main__':
    main()
