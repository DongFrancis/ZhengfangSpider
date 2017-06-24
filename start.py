#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2016.12.02
@author: 15999222
"""

import func
import parserInfo
from spider import Student
import command


def main():
    ob = Student(num = '15999222',password = 'dhn78834') # change your own num and password and name.
    ob.login() # login function,in order to log in the system.
    ob.get_ess()
    # cmd = command.results

    # print(cmd.year)
    # print(cmd.term)
    # print(cmd.output)

    while 1:
        switch = input("\n\n输入 1：获取课表并转为ical\t 2：查询学期成绩\t 3：查询平均学分绩点\t 0：结束\n")
        # print(switch)
        if switch == '0':
            break
        if switch == '1':
            responser = ob.sp_class()  # get web content.
            info = parserInfo.get_sch(responser)  # get the information you want.
            func.get_cal(info)  # show those information.

        if switch == '2':
            responser = ob.sp_GP()
            info = parserInfo.get_GP(responser)
            func.show_GP(info)

        if switch == '3':
            responser = ob.sp_GPA()
            GPA = parserInfo.get_GPA(responser)
            func.show_GPA(GPA)

        if switch == '4':
            responser = ob.test()
            print("HHHHHHHHH")
            GPA = parserInfo.test( responser )
            # func.show_GPA( GPA )
            print(GPA)

    return 0

if __name__ == "__main__":
    main()


