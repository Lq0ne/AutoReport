# -*- coding: UTF-8 -*-
import requests
import os
import json
import sys
import datetime

# # 定义全局变量
pwd = "123ab!@#"
user = "20190000000"
path="./user_data"



#token请求
token_req_url = "https://zhxg.qau.edu.cn/xuegong/api/UserAuth/GetManUserLogin"
token_req_header = {
    "Host": "zhxg.qau.edu.cn",
    "Connection": "keep-alive",
    "Content-Length": "86",
    "AppType": "4#1.1.11",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
    "content-type": "application/json",
    "Referer": "https://servicewechat.com/wx9af32b509e88340c/44/page-frame.html",
    "Accept-Encoding": "gzip, deflate, br"
}
token_req_json = {
    "ApplyType":3,
    "LoginName":"20190200779",
    "Pwd":"Ran20010219",
    "Code":"",
    "Key":"123123"
}





#上报请求
report_url = "https://zhxg.qau.edu.cn/xuegong/api/DayVirus/AddVirus"
report_header = {
    "Host": "zhxg.qau.edu.cn",
    "Connection": "keep-alive",
    "Content-Length": "701",
    "Accept": "application/json, text/plain, */*",
    "X-Token": "",
    "AppType": "2#3.0.0#1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 11; M2007J17C Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3179 MMWEBSDK/20210601 Mobile Safari/537.36 MMWEBID/2392 MicroMessenger/8.0.11.1980(0x28000B5B) Process/appbrand0 WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 miniProgram",
    "Content-Type": "application/json",
    "Origin": "https://zhxg.qau.edu.cn",
    "X-Requested-With": "com.tencent.mm",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://zhxg.qau.edu.cn/xgwui/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    # "Cookie": "insert_cookie=29594869"
}
report_json = {
    # "NowDate":"2022-01-13",
    # "UserType":1,
    # "Country":"中国",
    # "Province":"山东省",
    # "City":"青岛市",
    # "County":"城阳区",
    # "street_number":"长城路",
    # "CurrentPosition":"山东省青岛市城阳区长城路",
    # "FirstStitchDate":"2021-07-07",
    # "TwoStitchDate":"2021-08-07",
    # "FollowingCon":0,
    # "ContactPerson":0,
    # "Community":0,
    # "Health":0,
    # "GoToEpidemic":0,
    # "NowProvince":"山东省",
    # "NowCity":"青岛市",
    # "NowCountry":"城阳区",
    # "IsHeat":0,
    # "IsColdChain":0,
    # "IsLowRiskPerson":0,
    # "DayTemperature":1,
    # "Vaccination":2,
    # "Practice":0
}


class report_Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')

def get_token():
    global token_req_header
    global token_req_json
    global token_req_url
    token_req_json["Loginname"] = user
    token_req_json["pwd"] = pwd
    io = requests.post(token_req_url, json = token_req_json, headers = token_req_header, verify = False).json()
    # token = io[io.find("Token\":\"")+8:io.find("\",\"Exp")]
    return io['ResultValue']['Token']
    
    
    
def report():
    global report_json
    global report_header
    report_header["X-Token"] = get_token()
    report_json["NowDate"] = str(datetime.date.today())
    io = requests.post(report_url, json = report_json, headers = report_header, verify = False).text
    print(io)
    
    
def get_usr_data(file):
    global report_json
    global pwd
    fo = open(path + "/" + "passwd/" + file + ".txt", "r")
    pwd = fo.readline()
        
    #获取失败，终止脚本
    if pwd == "0":
        log.success("get user pwd fail !!!" + "\n" + "error code:0x0002")
        sys.exit()
        
    # 获取用户json    
    with open(path + "/" + "json/" + file + ".json", "rb") as load_json:
        report_json = json.load(load_json)
    # report_json = open(path + "/" + "json/" + file + ".json", "rb").read()
        
    # 获取失败，终止脚本
    if report_json == {}:
        log.success("get user json fail !!!" + "\n" + "error code:0x0003")
        sys.exit()

def main():
    global user
    user = sys.argv[1]
    
    # 传参失败，终止脚本
    if user == "0":
        log.success("get user fail !!!" + "error code:0x0001")
        sys.exit()
        
    get_usr_data(user)
    report()
main()