# XuanKe_new / 上海大学选课小助手 for 新选课系统
By shy

从2024年冬季学期的选课开始，学校关闭了旧的选课系统并使用了新的选课系统，因此之前的选课小助手已经失效。于是连夜对之前的程序进行了重写，赶出了新的选课小助手。

本脚本提供了三种不同的选课方式，分别对应三个函数：
- xk(clazzId, secretVal): 推荐，使用requests库直接发送请求，需要查询clazzId以及secretVal。其中secretVal错误可能会导致选课失败。
- xk2(cid, tid): 不推荐，基于selenium直接模仿人工操作浏览器，但尚无法判断是否选课成功。
- xk3(cid, tid): 基于快捷录入发送的请求，只需要教师号和课程号。

## 功能
- 自动蹲课，在课程有空余时立即选课；
- 支持对多节课的蹲课；
- cookie过期或在其他地方登录时自动更新cookie。
## 环境配置
python 3.12（推荐）环境下，控制台输入
`
pip install requirements.txt
`
安装软件包
## 使用步骤：
1. 确保电脑中有Chrome浏览器；
2. 确保chromedriver.exe在当前目录下。若不在或报错，请前往[该网址](https://googlechromelabs.github.io/chrome-for-testing/#stable)下载对应您版本的chromedriver并将解压后的chromedriver.exe移动到目录下；
3. 更改info.json中的信息:
```
  "term_index": 列表中的第几个学期，从0开始
  "Courses": 
      "cid":课程号
      "tid": 教师号
  "sleep_time": 刷新时间间隔，单位：s,
  "id": 学号,
  "password": 密码
```
4. 运行xk6.py，一开始可能需要更新cookie；
5. 查看课程，确保正确；
6. 输入[5]开始选课！
7. 静待“嘿嘿嘿哈”的成功通知！

## 须知
### 1.	合法合规使用
本程序仅用于合法目的，使用者应确保其获取的数据不违反任何适用的法律法规、网站使用条款或隐私政策。用户在使用本程序时应遵守所有相关法律、条例以及版权、商标等知识产权的规定。

### 3.	尊重网站政策
在使用程序时，用户应提前阅读并遵守目标网站的 robots.txt 文件、使用条款以及隐私政策。禁止获取不允许抓取的数据、访问被明确禁止的内容，或对网站造成任何形式的干扰。

### 4.	数据使用责任
用户在使用本程序获取的数据时，必须确保不会侵犯第三方的知识产权或个人隐私。本程序所获取的数据仅供学习、研究、数据分析等合规用途，未经授权不得用于商业或其他违法用途。

### 5.	对网站造成的影响
使用程序时，用户应避免对目标网站的服务器造成过大负担或干扰，避免频繁请求、过度抓取等行为，防止影响网站的正常运营或性能。

### 6.	免责声明
本程序的开发者对因使用该程序所引发的任何法律问题、数据泄露、损失或其他风险不承担任何责任。用户使用本程序所产生的任何纠纷、诉讼或其他后果，开发者不承担任何责任。

### 7.	网站内容的准确性与合法性
本程序不对所获取数据的准确性、合法性或完整性作出任何保证，用户需自行判断数据的可靠性和合法性。对于因使用数据产生的任何问题，开发者不承担责任。

### 8.	数据存储与保护
用户应确保所获取的数据的存储、使用符合隐私保护的相关法律法规，避免数据泄露或不当使用。特别是涉及个人隐私信息时，用户应特别小心，确保合规使用。

### 9.	开发者的权利
开发者有权随时修改、更新或撤回本程序的使用权，不会对因修改、更新或撤回服务而造成的任何影响或损失负责。
