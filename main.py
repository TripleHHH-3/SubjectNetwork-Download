import copy
import os

from lxml import etree
from selenium import webdriver
# 实现无可视化界面
from selenium.webdriver.chrome.options import Options
# 实现规避检测
from selenium.webdriver import ChromeOptions
from selenium.webdriver import ActionChains
from time import sleep
# 导入By类
from selenium.webdriver.common.by import By
# 导入显示等待类
from selenium.webdriver.support.ui import WebDriverWait
# 导入期望场景类
from selenium.webdriver.support import expected_conditions

from common.ReadYaml import ReadYaml

config = ReadYaml("./resources/application.yml", "utf-8")

# 实现规避检测
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])

# 下载设置
prefs = {'profile.default_content_settings.popups': 0,  # 防止保存弹窗
         # 'download.default_directory':tmp_path,#设置默认下载路径
         "profile.default_content_setting_values.automatic_downloads": 1  # 允许多文件下载
         }
option.add_experimental_option('prefs', prefs)

# 是否显示浏览器
if config.get("browser-conf.is-show"):
    bro = webdriver.Chrome(executable_path='./resources/chromedriver', options=option)
else:
    # 实现无可视化界面的操作
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    bro = webdriver.Chrome(executable_path='./resources/chromedriver', chrome_options=chrome_options, options=option)

# 进入网址
bro.get(config.get("base-url"))
tree = etree.HTML(bro.page_source)
# 添加cookie
for cookie in config.get("cookies"):
    bro.add_cookie(cookie)

# 点击登录
login_btn = bro.find_element_by_class_name('login-btn')
login_btn.click()

# 切换到账号密码登录
lcon_weixin = bro.find_element_by_class_name('lcon-weixin')
lcon_weixin.click()

# 输入账号密码
username = bro.find_element_by_xpath('//*[@id="username"]')
username.send_keys(config.get("account.username"))
psd = bro.find_element_by_xpath('//*[@id="ordinaryLoginTab"]/li[2]/div/input')
psd.send_keys(config.get("account.password"))

# 点击登录按钮
CommonLogin = bro.find_element_by_id("CommonLogin")
CommonLogin.click()

# 下载
downUrlList = config.get("down-url")
downSize = config.get("browser-conf.down-count")
downList = []
for index in range(len(downUrlList)):
    if index % downSize == 0:
        downList.append({downUrlList[index]: None})
    else:
        downList[-1].update({downUrlList[index]: None})

downMax = config.get("browser-conf.down-max")
fp = open("./resources/finishDown.txt", "a", encoding="utf-8")
for downMap in downList:
    for url in downMap:
        # 打开新标签页
        bro.execute_script("window.open()")
        bro.switch_to.window(bro.window_handles[-1])
        bro.get(url)

        # 存储文件相关信息
        tree = etree.HTML(bro.page_source)
        filename = tree.xpath('//div[@class="hd-des"]//h1/@title')[0]
        filesize = tree.xpath("//div[@class='dropdown']/p[1]/span[3]/text()")[0]
        filesize = int(filesize.split("：")[1].replace("KB", ""))
        downMap[url] = [filename, filesize, downMax * 1000 > filesize]

        if downMap[url][2]:
            # 点击下载
            download = WebDriverWait(bro, 10).until(
                expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="btnSoftDownload"]/div')))
            action = ActionChains(bro)
            action.move_to_element(download).click().perform()

            confirmBtns = bro.find_elements_by_xpath("//div[@class='modal-body']//*[contains(@class,'pw-confirm')]")
            if len(confirmBtns) != 0:
                for confirmBtn in confirmBtns:
                    try:
                        confirmBtn.click()
                        break
                    except:
                        continue

    needToDownMap = copy.deepcopy(downMap)
    while True:
        fileList = os.listdir(config.get("browser-conf.down-location"))
        downFinishList = []
        for file in fileList:
            downFinishList.append(os.path.splitext(file)[0])

        for key in list(needToDownMap):
            if needToDownMap[key][2]:
                if needToDownMap[key][0] in downFinishList:
                    fp.write(key + ":" + needToDownMap[key][0] + ":" + str(needToDownMap[key][1]) + "\n")
                    needToDownMap.pop(key)
            else:
                fp.write(
                    key + ":" + needToDownMap[key][0] + ":" + str(needToDownMap[key][1]) + ":" + "这个文件太大了死猪" + "\n")
                needToDownMap.pop(key)

        if len(needToDownMap) == 0:
            break

        sleep(0.2)

    for index in range(len(downMap)):
        bro.switch_to.window(bro.window_handles[-1])
        bro.close()
    bro.switch_to.window(bro.window_handles[0])

fp.write("下载完啦，又能挣到钱啦，棒猪！\n")
fp.close()

# 鼠标悬停
bro.switch_to.window(bro.window_handles[0])
action = ActionChains(bro)
LoginInfo = bro.find_element_by_id("LoginInfo")
action.move_to_element(LoginInfo).perform()
sleep(0.25)

# 退出
logout = bro.find_element_by_xpath('//*[@id="LoginInfo"]/div[1]/div/div[1]/a[2]')
logout.click()
sleep(1)
bro.quit()

# download = bro.find_element_by_xpath('//*[@id="btnSoftDownload"]/div')
# download.click()
# action = ActionChains(bro)
# action.move_to_element(download).click().perform()

# web_element = bro.find_element_by_xpath('//*[@id="btnSoftDownload"]/div')
# result = WebDriverWait(bro, 10).until(
#     expected_conditions.element_to_be_clickable(web_element))
# result.click()
