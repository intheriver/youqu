# 配置脚本运行环境
1.重命名scripts/common_example.py -> common.py  
更改scripts/common.py  

mail_addr = "xxx@fiberhome.com"  
mail_pw = "xxx"  

这个配置的发送邮件方的邮箱地址和密码  

2.重命名signjob_example.bat -> signjob.bat  
以下是修改签到信息的，修改文件为  
    start /b cmd /c %py% scripts/signin.py -u xx -p xx -m xx@fiberhome.com -g xx -l 在烽火通信高新四路研发中心签到啦!  
    %py% scripts/sleep.py 2  
    start /b cmd /c %py% scripts/signin.py -u xx -p xx -m xx@fiberhome.com -g xx -l 在烽火通信高新四路研发中心签到啦!

-u 悠趣用户名，一般是手机号  
-p 悠趣的密码  
-m 接收签到信息的邮箱  
-g 要签到的圈子，多个圈子用 **','** 隔开 ，比如 **二部,三部**  
-l 指定签到的位置信息  

sleep.py 后面跟的数字是上一条命令执行之后隔多长时间执行下一条，单位是**秒**

**此工具需要安装python**  
set py="D:/OTNM/ext/win32_vc9_x86/Python27/python"  
这个指定的是网管的python,如果没有安装网管，那需要自己安装python，并且将这个路径改为安装路径  
python版本为2.7  


# 建立定时任务
开始->管理工具->任务计划程序

右边栏**创建任务**  
- 操作栏：  
    新建->操作里面选择“启动程序”->程序或脚本里面点击“浏览”，找到signjob.bat这个路径
    ”起始于“框里面填入signbat.bat程序的路径
    比如signjob.bat的全路径为d:\youqu\signjob.bat,那么这里应该填**d:\youqu**
* 触发器：  
    新建->选择每周->勾选要签到的时间
    起始于的意思是每天在什么时间点执行
    选中启用
    
* 常规：  
    选中 不管用户是否登录都执行
* 名称：  
    这里可以随便写