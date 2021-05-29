from logging import error
from django.shortcuts import redirect, render
import requests
import pyperclip
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import chromedriver_autoinstaller
from collections import Counter
import json

# Create your views here.


def home(request):
    return render(request, 'home.html')


def report(request):
    id = request.GET['id']
    pw = request.GET['pw']

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    path = chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(path, options=options)
    driver.implicitly_wait(5)
    driver.get('https://nid.naver.com/nidlogin.login')
    driver.implicitly_wait(5)

    # 아이디 입력, 패스워드 입력
    naver_id = driver.find_element_by_name('id')
    naver_id.clear()
    naver_id.click()
    user_id = id
    user_pw = pw
    pyperclip.copy(user_id)
    naver_id.send_keys(Keys.COMMAND, 'v')
    driver.implicitly_wait(5)

    naver_pw = driver.find_element_by_name('pw')
    naver_pw.clear()
    naver_pw.click()
    pyperclip.copy(user_pw)
    naver_pw.send_keys(Keys.COMMAND, 'v')
    driver.implicitly_wait(5)

    # 로그인 버튼 누르기
    login_btn = driver.find_element_by_id('log.login')
    login_btn.click()
    time.sleep(1)

    # 메일 함 들어갔을 때 사용자의 쿠키 받아오기(cookie)
    cookies = driver.get_cookies()
    cookie = ''
    for i in range(len(cookies)):
        cookie = cookie+(cookies[i])['name']+'='+(cookies[i])['value']+';'

    headers = {
        'cookie': cookie
    }
    params_mail = (
        ('page', '1'),
        ('u', id),
    )

    params_data = {
        'u': id
    }
    mail_list_name = []
    # 메일에 관련된 요청
    response_mail = requests.post(
        'https://mail.naver.com/json/list/', headers=headers, params=params_mail)
    arr = response_mail.json()
    totalCount = arr['totalCount']  # 총 메일갯수
    one_page_number = arr['listCount']  # 첫페이지 메일 갯수
    page_number = int(int(totalCount)/int(one_page_number) + 1)  # 총 페이지 갯수
    unreadCount = arr['unreadCount']

    # 용량에 관련된 요청
    response_capacity = requests.post(
        'https://mail.naver.com/json/option/trash/get/', headers=headers, data=params_data)
    diskUsage = (response_capacity.json())['diskUsage']  # 총 사용 용량

    for i in range(1, page_number+1):
        headers = {
            'cookie': cookie

        }
        params_mail = (
            ('page', i),
            ('u', id),
        )

    # 메일에 관련된 요청
        response_mail = requests.post(
            'https://mail.naver.com/json/list/', headers=headers, params=params_mail)
        arr = response_mail.json()

        mail_data_list = arr['mailData']
        # 제목, 보낸이, 크기, 시리얼넘버, 보낸 시간, read(default:read), mark(default:mark) 딕션너리 생성
        for i in mail_data_list:
            mail_list_name.append((i['from'])['name'])

    # result의 값은 보낸이를 내림차순으로 나타낸 리스트이다.
    result = Counter(mail_list_name)
    result = sorted(result.items(), key=lambda x: x[1], reverse=True)

    result_list = []
    if len(result) < 3:
        for i in range(len(result)):
            result_list.append(result[i][0])
    else:
        for i in range(3):
            result_list.append(result[i][0])
    return render(request, 'report.html', {'id': id, 'unreadCount': unreadCount, 'diskUsage': diskUsage, 'cookie': cookie, 'totalCount': totalCount, 'result_list': result_list})


def delete(request):
    mail_list = []
    id = request.GET['id']
    # read = request.GET['isRead']
    # mark = request.GET['isMark']
    cookie = request.GET['cookie']
    # to_date = request.GET['to_date']
    # from_date = request.GET['from_date']

##################[첫 페이지] #########################################

    headers = {
        'cookie': cookie
    }
    params = (
        ('page', '1'),
        ('u', id),
    )

    response_mail = requests.post(
        'https://mail.naver.com/json/list/', headers=headers, params=params, timeout=250)
    arr = response_mail.json()
    totalCount = arr['totalCount']  # 총 메일갯수
    one_page_number = arr['listCount']  # 첫페이지 메일 갯수
    page_number = arr['lastPage']  # 총 페이지 갯수
    unreadCount = arr['unreadCount']

    mail_data_list = arr['mailData']
    for i in mail_data_list:
        mail_list.append(
            {'name': (i['from'])['name'],
             'size': i['size'],
             'subject': i['subject'],
             'mailSN': i['mailSN'],
             'sentTime': i['sentTime'],
             'read': 'read',
             'mark': 'unmark',
             }
        )
        if len(mail_data_list) == 0:
            break
##############################################################################

#####################[두번쨰부터 끝까지]##########################################
    for i in range(2, 33):
        headers = {
            'cookie': cookie

        }
        params_mail = (
            ('page', i),
            ('u', id),
        )

    # 메일에 관련된 요청
        response_mail = requests.post(
            'https://mail.naver.com/json/list/', headers=headers, params=params_mail, timeout=250)
        arr = response_mail.json()
        mail_data_list = arr['mailData']
        # 제목, 보낸이, 크기, 시리얼넘버, 보낸 시간, read(default:read), mark(default:mark) 딕션너리 생성
        for i in mail_data_list:
            mail_list.append(
                {'name': (i['from'])['name'],
                 'size': i['size'],
                 'subject': i['subject'],
                 'mailSN': i['mailSN'],
                 'sentTime': i['sentTime'],
                 'read': 'read',
                 'mark': 'none'
                 }
            )
            if len(mail_data_list) == 0:
                break
#########################################################################################

############################안읽은메일 요청해서 read:read 값을 read:unread로 치환###############
    for i in range(1, 33):
        headers = {
            'cookie': cookie
        }
        params = (
            ('page', i),
            ('isUnread', 'true'),
            ('u', id),
        )

        response_mail = requests.post(
            'https://mail.naver.com/json/list/', headers=headers, params=params, timeout=250)
        arr = response_mail.json()

        mail_data_list = arr['mailData']  # 보낸 사람

        a = []
        for i in mail_data_list:
            a.append(i['mailSN'])
        for m in mail_list:
            if m['mailSN'] in a:
                m['read'] = 'unread'
        if len(mail_data_list) == 0:
            break

######################################################################################

#########################중요메일 표시된메일만 요청해서 mark:unmark 값을 mark:mark 로 치환#######
    for i in range(1, 33):
        headers = {
            'cookie': cookie
        }
        params = (
            ('page', i),
            ('type', 'mark'),
            ('u', id),
        )

        response_mail = requests.post(
            'https://mail.naver.com/json/list/', headers=headers, params=params, timeout=250)
        arr = response_mail.json()
        mail_data_list = arr['mailData']  # 보낸 사람
        a = []
        for i in mail_data_list:
            a.append(i['mailSN'])
        for m in mail_list:
            if m['mailSN'] in a:
                m['mark'] = 'mark'
        if len(mail_data_list) == 0:
            break

###############################################################################

    # if read == "both" and mark == "both":
    #     mail_list = mail_list
    # elif read == "both" and mark != "both":
    #     mail_list = [x for x in mail_list
    #                  if x["mark"] == mark]
    # elif read != "both" and mark == "both":
    #     mail_list = [x for x in mail_list
    #                  if x["read"] == read]
    # else:
    #     mail_list = [x for x in mail_list
    #                  if x["mark"] == mark and x["read"] == read]

    # from_date = time.mktime(datetime.strptime(
    #     from_date, '%Y-%m-%d').timetuple())
    # to_date = time.mktime(datetime.strptime(to_date, '%Y-%m-%d').timetuple())

    # mail_list = [x for x in mail_list
    #              if from_date < x["sentTime"] < to_date]

    return render(request, 'delete.html', {'mail_list': json.dumps(mail_list), 'id': id, 'cookie': cookie})


# def checked(request):
#     mailSN = request.GET.getlist('mailSN')
#     cookie = request.GET['cookie']
#     id = request.GET['id']

#     # 휴지통으로 보내기 위해
#     delete = ''
#     for i in mailSN:
#         delete = delete+i+';'

#     # 휴지통으로 보내기
#     headers = {
#         'authority': 'mail.naver.com',
#         'referer': 'https://mail.naver.com/',
#         'cookie': cookie,
#     }

#     data = {
#         'mailSNList': delete,
#         'currentFolderType': 'etc',
#         'u': id
#     }

#     requests.post(
#         'https://mail.naver.com/json/select/delete/', headers=headers, data=data)
#     return render(request, 'delete.html',  {'mailSN': mailSN, 'id': id, 'cookie': cookie})
