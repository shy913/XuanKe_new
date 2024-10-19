# XuanKe_new / 上海大学选课小助手 for 新选课系统
By shy

从2024年冬季学期的选课开始，学校关闭了旧的选课系统并使用了新的选课系统，因此之前的选课小助手已经失效。于是连夜对之前的程序进行了重写，赶出了新的选课小助手。

本脚本提供了三种不同的选课方式，分别对应三个函数：
- xk(clazzId, secretVal): 推荐，使用requests库直接发送请求，需要查询clazzId以及secretVal。其中secretVal错误可能会导致选课失败。
- xk2(cid, tid): 不推荐，基于selenium直接模仿人工操作浏览器，但尚无法判断是否选课成功。
- xk3(cid, tid): 开发中，基于快捷录入发送的请求，只需要教师号和课程号。


## 须知
由于本项目造成的任何后果由您负责。

请确保不会对学校系统造成负担。

## 功能
- 自动蹲课，在课程有空余时立即选课；
- 支持对多节课的蹲课；
- cookie过期或在其他地方登录时自动更新cookie。

## 使用步骤：
1. 确保电脑中有Chrome浏览器；
2. 确保chromedriver.exe在当前目录下。若不在或报错，请前往[该网址](https://googlechromelabs.github.io/chrome-for-testing/#stable)下载对应您版本的chromedriver并将解压后的chromedriver.exe移动到目录下；
3. 更改info.json中的账号密码以及蹲的课；
4. 运行xk6.py，一开始可能需要更新cookie；
5. 查看课程，确保正确；
6. 输入[5]开始选课！
7. 静待“嘿嘿嘿哈”的成功通知！
