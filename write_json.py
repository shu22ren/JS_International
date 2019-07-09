#!/usr/bin/python
# -*- coding:utf-8 -*-

import re
import json
import requests
import sys


# 定义正则表达式
re_str = re.compile(r"'js_version': '1.0.(.*?)'")

def write_json(language,container,role,path):
    print('role==='+role)
    if language == 'international':
        url = 'https://exeutest.blob.core.chinacloudapi.cn/%s/sfdc-verson_international.json' %container
    elif language == 'india':
        url = 'https://exeutest.blob.core.chinacloudapi.cn/%s/ontap_in_versions.json' % container
    elif language == 'VN':
        url = 'https://exeutest.blob.core.chinacloudapi.cn/%s/sfdc-verson-vn.json' % container
    else:
        url = 'https://exeutest.blob.core.chinacloudapi.cn/%s/sfdc-verson.json' % container

    if role == 'spr' or role == 'k0':
        roles = ['CN %s' %(role.upper())]
    elif role == 'bds':
        roles = ['CN BDR Supervisor','CN BDR Manager']
    elif role == 'bdr':
        roles = ['IN BDR']
    elif role == 'Inspection':
        roles = ['Inspection']
    elif role == 'VNSPR':
        roles = ['VN SPR']
    elif role.index("|")!=-1:
        roles = role.split("|")
    else:
        roles = [role]
    #print(roles)
    # 读取URL中的json文件
    text = json.loads(requests.get(url).text)
    for role in roles:
        info = text.get('app_info')
        js = str(info[role])
        #print(role+'=='+js)
        s = int(re_str.findall(js)[0])
        # 针对补丁版本号的位数进行处理
        if s//10 == 0:
            s += 1
            re_s = '00%d' %s
        elif s//10 < 10:
            s += 1
            re_s = '0%d' %s
        else :
            s += 1
            re_s = str(s)
        # 版本号自增1
        re_s = "'js_version': '1.0.%s'" %re_s
        # 版本号自增后替换掉原来的版本号
        new_json = eval(re_str.sub(re_s,js,1))
        # 修改json文件中对应角色的版本号
        text['app_info'][role] = new_json

    # 读取到的内容写入json中
    with open(path,'w',encoding='utf-8') as fw:
        fw.write(json.dumps(text,ensure_ascii=False, indent=4) )

write_json(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
#write_json('VN','sfdc-test','VN BDR|VN M1',r'D:\python_work\sfdc-verson-vn.json')
