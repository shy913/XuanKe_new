import json
import tabulate
import winsound
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
import requests
import time
from datetime import datetime, timedelta
import urllib.parse

VERSION = "6.1"

def get_cookie():
    global Info
    print("正在更新cookie...")
    service = Service(executable_path=r'chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.set_window_size(1920, 1080)
    driver.minimize_window()
    driver.get("http://jwxk.shu.edu.cn/")
    driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div/form/div[1]/input').send_keys(Info['id'])
    driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div/form/div[2]/input[2]').send_keys(Info['password'])
    driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div/form/button').click()

    # 刷新以跳过等待时间
    time.sleep(1)
    driver.refresh()
    time.sleep(2) # 一秒会报错

    # 如果index != 0，切换学期
    if Info['term_index'] != '0':
        # "切换"
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/a[2]/span/a').click()

        # 选择学期， 按下位置 = 第一个按钮位置 + 偏移量，下为原始位置
        # driver.find_element(By.XPATH, '/html/body/div[2]/div/div[8]/div/div[2]/div[1]/table/tbody/tr[2]/td[1]/label/span[1]/span')
        shift = int(Info['term_index'])
        driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[8]/div/div[2]/div[1]/table/tbody/tr[{2 + shift}]/td[1]/label/span[1]/span').click()

        # 确认
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div[8]/div/div[2]/div[2]/span/button[1]').click()

        # 更新batchid
        batch_id = driver.current_url.split('=')[-1]
        Info['batch_id'] = batch_id


    driver.refresh()
    time.sleep(1)
    coo = ''
    flag = False
    for req in driver.requests:
        if req.method == 'POST' and req.url == 'https://jwxk.shu.edu.cn/xsxk/elective/shu/clazz/list':
            coo = req.headers['Cookie']
            flag = True

    if flag is False:
        print("未查询到POST")
        return False
    else:
        with open('info.json', 'r', encoding='utf-8') as f:
            t = json.load(f)
        t['batch_id'] = Info['batch_id']
        t["cookie"]["value"] = coo
        t["cookie"]["auth"] = coo[54:]
        t["cookie"]["datetime"] = datetime.now().isoformat()
        with open('info.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(t, indent=4))
        print("cookie写入成功")
        time.sleep(float(Info["wait_time"]))
        with open('info.json', 'r', encoding='utf-8') as f:
            Info = json.load(f)
        print(Info["cookie"]["datetime"])
        return True


def list_clazz():
    global Info
    with open('info.json', 'r', encoding='utf-8') as f:
        Info = json.load(f)
    # print(Info)
    for course in Info['Courses']:
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "authorization": Info["cookie"]["auth"],
            "batchid": batch_id,
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            'Cookie': Info["cookie"]["value"]
        }
        body = f'teachingClassType=ALLKC&pageNumber=1&pageSize=10&orderBy=&KCH={course['cid']}&JSH={course['tid']}'
        try:
            response = requests.post('https://jwxk.shu.edu.cn/xsxk/elective/shu/clazz/list', headers=headers, data=body,
                                     timeout=5).text
            response = json.loads(response)
            text = [['name', response['data']['list']['rows'][0]['SKSJ'][0]['KCM']],
                    ['cid', response['data']['list']['rows'][0]['SKSJ'][0]['KCH']],
                    ['tid', response['data']['list']['rows'][0]['SKSJ'][0]['KXH']],
                    ['selecting num', response['data']['list']['rows'][0]['YXRS']],
                    ['capacity', response['data']['list']['rows'][0]['KRL']],
                    ['remain', int(response['data']['list']['rows'][0]['KRL']) - int(
                        response['data']['list']['rows'][0]['YXRS'])], ]
            print(tabulate.tabulate(text, tablefmt="fancy_grid"))
        except:
            print(f'{course}请求失败！')
            # print(f'返回信息：{response.__repr__()[:20]}......')


def get_remain(cid, tid):
    global Info
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "authorization": Info["cookie"]["auth"],
        "batchid": batch_id,
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        'Cookie': Info["cookie"]["value"]
    }
    body = f'teachingClassType=ALLKC&pageNumber=1&pageSize=10&orderBy=&KCH={cid}&JSH={tid}'
    try:
        response = requests.post('https://jwxk.shu.edu.cn/xsxk/elective/shu/clazz/list',
                                 headers=headers,
                                 data=body,
                                 timeout=5).text
        response = json.loads(response)
        text = [['name', response['data']['list']['rows'][0]['SKSJ'][0]['KCM']],
                ['tid', response['data']['list']['rows'][0]['SKSJ'][0]['KXH']],
                ['remain',
                 int(response['data']['list']['rows'][0]['KRL']) - int(response['data']['list']['rows'][0]['YXRS'])], ]
        print(tabulate.tabulate(text))
        ret = [int(response['data']['list']['rows'][0]['KRL']) - int(response['data']['list']['rows'][0]['YXRS'])]
        ret.append(response['data']['list']['rows'][0]['JXBID'])
        ret.append(response['data']['list']['rows'][0]['secretVal'])
        return ret
    except Exception as e:
        print(f'{cid},{tid}请求失败！')
        print(f"请求错误！{e}")
        return [-100, None, None]


def xk2(cid, tid):
    global Info
    # driver.find_element(By.XPATH,
    #                     "/html/body/div[2]/div/div[5]/div/div/div[2]/div[1]/div/div[1]/div[1]/div/div[2]/div/input").clear()
    # driver.find_element(By.XPATH,
    #                     "/html/body/div[2]/div/div[5]/div/div/div[2]/div[1]/div/div[1]/div[1]/div/div[2]/div/input").send_keys(
    #     cid)
    # driver.find_element(By.XPATH,
    #                     "/html/body/div[2]/div/div[5]/div/div/div[2]/div[1]/div/div[1]/div[3]/div/div[2]/div/input").clear()
    #
    # driver.find_element(By.XPATH,
    #                     "/html/body/div[2]/div/div[5]/div/div/div[2]/div[1]/div/div[1]/div[3]/div/div[2]/div/input").send_keys(
    #     tid)
    # driver.find_element(By.XPATH,
    #                     "/html/body/div[2]/div/div[5]/div/div/div[2]/div[1]/div/div[1]/div[14]/button[1]").click()
    # time.sleep(10)
    # driver.find_element(By.XPATH,
    #                     "/html/body/div[2]/div/div[5]/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div[3]/table/tbody/tr/td[1]/div/button").click()
    # driver.find_element(By.XPATH,
    #                     "/html/body/div[3]/div/div[3]/button[2]").click()


def xk3(cid, tid):
    global Info
    url = "https://jwxk.shu.edu.cn/xsxk/elective/shu/clazz/quick-add"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": Info["cookie"]["auth"],
        "batchId": batch_id,
        "Origin": "https://jwxk.shu.edu.cn",
        "Connection": "keep-alive",
        "Referer": f"https://jwxk.shu.edu.cn/xsxk/elective/grablessons?batchId={batch_id}",
        "Cookie": Info["cookie"]["value"],
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin", }
    body = f"1=%{cid}%2C{tid}"
    try:
        response = requests.post(url, headers=headers, data=body, timeout=5).text
    except Exception as e:
        print("呃吼吼呜")
        print(e)
        return False
    if "成功" in response:
        print("嘿嘿嘿哈!!!")
        return True
    else:
        print("呃吼吼呜")
        print(response)
        return False

def xk(clazzId, secretVal):
    global Info
    secretVal = urllib.parse.quote(secretVal)
    print("开始选课！")
    url = "https://jwxk.shu.edu.cn/xsxk/elective/shu/clazz/add"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": Info["cookie"]["auth"],
        "batchId": batch_id,
        "Origin": "https://jwxk.shu.edu.cn",
        "Connection": "keep-alive",
        "Referer": f"https://jwxk.shu.edu.cn/xsxk/elective/grablessons?batchId={batch_id}",
        "Cookie": Info["cookie"]["value"],
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin", }
    body = f"clazzType=XGKC&clazzId={clazzId}&secretVal={secretVal}"
    try:
        response = requests.post(url, headers=headers, data=body, timeout=5).text
    except Exception as e:
        print("呃吼吼呜")
        print(e)
        return False
    if "成功" in response:
        print("嘿嘿嘿哈!!!")
        return True
    else:
        print("呃吼吼呜")
        print(response)
        return False

def jiao():
    type = '1'
    if type == '1':
        winsound.MessageBeep(winsound.MB_ICONHAND)
    if type == '2':
        winsound.MessageBeep(winsound.MB_OK)
    if type == '3':
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    if type == "0":
        """额"""
def main():
    global Info

    with open('info.json', 'r', encoding='utf-8') as f:
        Info = json.load(f)
    items = ["查看选课列表", "查看设置", "手动更新cookie", "退出", "开始选课"]
    text = []
    for i in range(len(items)):
        text.append([f"[{i + 1}]", items[i]])
    while True:
        print(f"选课小助手 {VERSION}")

        # cookie 时间查询
        current_time = datetime.now()
        # print(current_time.isoformat())
        try:
            last_time = datetime.fromisoformat(Info["cookie"]["datetime"])
        except:
            last_time = datetime(2000, 1, 1, 0, 0, 0)
        time_diff = current_time - last_time
        if time_diff > timedelta(hours=1):
            i = input("cookie 超过一小时，是否更新？\ny/n")
            if i == "y":
                get_cookie()
            elif i == "n":
                print("Warning: errors may occur")
        else:
            print(f"cookie上次获取时间：{time_diff.seconds}s前")

        print(tabulate.tabulate(text))
        choice = input("")
        if choice == "1":
            list_clazz()
        if choice == "2":
            print(Info)
        if choice == "3":
            get_cookie()
        if choice == "4":
            exit()
        if choice == "5" or choice == "":
            print("开始选课！")
            err_count = 0
            time_count = 1
            while True:
                if err_count >= 5:
                    err_count = 0
                    get_cookie()
                for i in range(len(Info["Courses"])):
                    course = Info["Courses"][i]
                    if course["selected"] is False:
                        if True: # False: 忽略剩余人数限制
                            result = get_remain(course['cid'], course['tid'])
                            if result[0] == -100:
                                err_count += 1
                            elif result[0] > 0:
                                if xk(result[1], result[2]):
                                # if xk3(course['cid'],course['tid']):
                                    print("选课成功！")
                                    Info["Courses"][i]["selected"] = True
                                    with open('info.json', 'w', encoding='utf-8') as f:
                                        f.write(json.dumps(Info, indent=4))
                                jiao()
                            time.sleep(float(Info["wait_time"]))
                        else:
                            if xk3(course['cid'], course['tid']):
                                print("选课成功！")
                                Info["Courses"][i]["selected"] = True
                                with open('info.json', 'w', encoding='utf-8') as f:
                                    f.write(json.dumps(Info, indent=4))
                            time.sleep(float(Info["wait_time"]))
                    else:
                        print(f"已跳过 {course['cid']}, {course['tid']}")
                print(
                    f"第{time_count}次循环已结束！\n"
                    f"time:{datetime.strftime(datetime.now(), "%m月%d日%H:%M:%S")}\n"
                    f"err_count:{err_count}\n")
                time_count += 1
                time.sleep(float(Info["sleep_time"]))



if __name__ == '__main__':
    jiao()
    # initialize
    print("Made by shy")
    # 判断新用户
    with open('info.json', 'r', encoding='utf-8') as f:
        Info = json.load(f)
    batch_id = Info["batch_id"]
    if Info["new"] is True:
        agree = 'tongyi'
        if input(f'Note:\n由于本项目造成的任何后果由您负责。\n请确保不会对计算机系统造成负担。\n你是否同意？\n输入{agree}以继续：') == agree:
            Info["new"] = False
            Info["sleep_time"] = int(input("请输入刷新间隔(s)："))
            Info["id"] = input("请输入学号：")
            Info["password"] = input("请输入密码：")
            with open('info.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(Info, indent=4))
            print('ok!')
        else:
            exit()

    # print("welcome!")
    try:
        main()
    except Exception as e:
        print(e)
        main()
    time.sleep(2200)
