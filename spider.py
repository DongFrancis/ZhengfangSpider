# -*- coding: utf-8 -*-
"""
Created on 2016.12.02
@author: 15999222
"""

import platform
import os
import re
import requests
from bs4 import BeautifulSoup

XN = ["2015-2016","2016-2017"]
XQ = ["1","2"]
IFLOGIN = "请登录"

class Student:
    def __init__(self):
        self.st_num = '15999222'  # 学号
        self.password = 'dhn78834'  #
        self.grade = ''
        self.name = '董华楠'  # 姓名
        self.urlName = '%B6%AD%BB%AA%E9%AA'  # url编码后的姓名
        self.idCardNumber = ''  # 身份证号
        self.sex = '' # 性别
        self.enterSchoolTime = ''  # 入学时间
        self.birthsday = ''  # 出生日期
        self.highschool = ''  # 毕业中学
        self.nationality = ''  # 名族
        self.hometown = ''  # 籍贯
        self.politicsStatus = ''  # 政治面貌
        self.college = ''  # 学院
        self.major = ''  # 专业
        self.classname = ''  # 所在班级
        self.gradeClass = ''  # 年级
        self.session = requests.session()
        self.baseUrl = "http://210.30.208.200/"

    def login(self):
        # 访问教务系统
        status = True
        print("正在尝试登录......")
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        response = self.session.get(self.baseUrl)
        self.baseUrl = response.url
        self.baseUrl = re.subn(r'.default2.aspx', '', self.baseUrl)[0]
        loginUrl = self.baseUrl + '/default2.aspx'

        while (status):
            response = self.session.get(loginUrl)
            __VIEWSTATE = re.findall("name=\"__VIEWSTATE\" value=\"(.*?)\"", response.content.decode('GBK'))[0]
            # print(__VIEWSTATE)
            print("Got viewatate")
            print( "正在获取验证码......" )
            imgUrl = self.baseUrl + "/CheckCode.aspx?"
            imgresponse = self.session.get(imgUrl, stream=True)
            image = imgresponse.content

            # 保存code
            if 'Linux' in platform.system():
                DstDir = os.getcwd() + "/"
                # print(DstDir)
                with open(DstDir + "code.jpg", "wb") as jpg:
                    jpg.write(image)
                    print("保存验证码到：" + DstDir + "code.jpg" + "\n")

                os.popen("display " + DstDir + "code.jpg")
            else:
                DstDir = os.getcwd() + "\\"
                print(DstDir)
                with open(DstDir + "code.jpg", "wb") as jpg:
                    jpg.write(image)
                    print("保存验证码到：" + DstDir + "code.jpg" + "\n")

                command = "start" + " \"\" " + DstDir +"code.jpg"
                x = os.popen( command ).read()

            code = input("验证码是：")
            RadioButtonList1 = u"学生".encode('gb2312', 'replace')
            data = {
                "RadioButtonList1": RadioButtonList1,
                "__VIEWSTATE": __VIEWSTATE,
                "txtUserName": self.st_num,
                "TextBox2": self.password,
                "Button1": "",
                "txtSecretCode": code,
            }

            Loginresponse = self.session.post(loginUrl, data=data)
            print("尝试登录中......")

            url2 = self.baseUrl + "/xs_main.aspx?xh=" + self.st_num
            self.session.headers['Referer'] = self.baseUrl + "default2.aspx"
            response2 = self.session.get(url2)
            html = response2.content.decode("gb2312")
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.get_text()
            print(title)
            if title.find(IFLOGIN) != -1:
                print("登录失败，正在重新登录......")
            else:
                status = False

        print("成功登录教务系统")
        # succeed
        return 1



    # print(Loginresponse.content.decode('GBK'))

    '''
        个人课表
    '''
    def sp_class(self):
        # 选择学期
        choice = int(input("清选择学期：\n\t\t1、2015-2016 第一学期\t2、2015-2016 第二学期\n\t\t3、2016-2017 第一学期\t4、2016-2017 第二学期\n"))
        xn = XN[int((choice -1)/2)]
        xq = XQ[int(choice % 2)]

        # 从课程便初始页面获取__VIEWSTATE
        url2 = self.baseUrl + "/xskbcx.aspx?xh=" + self.st_num + "&xm=" + self.urlName + "&gnmkdm=N121603"
        self.session.headers['Referer'] = self.baseUrl + '/xs_main.aspx?xh=' + self.st_num
        response2 = self.session.get( url2 )
        html = response2.content.decode( "gb2312" )
        soup = BeautifulSoup( html, 'html.parser' )
        __VIEWSTATE2 = soup.findAll( 'input' )[2]['value']
        print(__VIEWSTATE2)

        self.session.headers['Referer'] = self.baseUrl + "/xscjcx.aspx?xh=" + self.st_num + "&xm=" + self.urlName + "&gnmkdm=N121603"
        data2 = {
            '__EVENTTARGET':'xqd',
            '__EVENTARGUMENT':'',
            '__VIEWSTATE':__VIEWSTATE2,
            'xnd':xn,
            'xqd':xq,
        }
        response2 = self.session.post(url2,data = data2)
        ans = response2.text
        return ans


    '''
    GPA 学期
    '''
    def sp_GPA(self):
        # 选择学期
        choice = int(input("清选择学期：\n\t\t1、2015-2016 第一学期\t2、2015-2016 第二学期\n\t\t3、2016-2017 第一学期\t4、2016-2017 第二学期\n"))
        xn = XN[int((choice - 1)/2)]
        xq = XQ[int((choice - 1) % 2 )]

        url3_1 = self.baseUrl + "/xscjcx.aspx?xh=" + self.st_num + "&xm=" + self.urlName + "&gnmkdm=N121605"
        self.session.headers['Referer'] = self.baseUrl + '/xs_main.aspx?xh=' + self.st_num
        response3_1 = self.session.get(url3_1)
        html = response3_1.content.decode("gb2312")
        soup = BeautifulSoup(html,'html.parser')
        __VIEWSTATE3 = soup.findAll('input')[2]['value']

        self.session.headers['Referer'] = self.baseUrl + "/xscjcx.aspx?xh=" + self.st_num + "&xm=" + self.urlName + "&gnmkdm=N121605"
        data3 = {
            "__EVENTTARGET":"",
            "__EVENTARGUMENT":"",
            "__VIEWSTATE":__VIEWSTATE3,
            'hidLanguage':"",
            "ddlXN":xn,
            "ddlXQ":xq,
            "ddl_kcxz":"",
            "btn_xq" : u"学期成绩".encode('gb2312', 'replace')
        }
        response3 = self.session.post(url3_1,data=data3)

        ans = response3.content
        return ans
