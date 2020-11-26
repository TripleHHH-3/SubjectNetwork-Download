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
downList = []
for index in range(len(downUrlList)):
    if index % 5 == 0:
        downList.append({downUrlList[index]: ""})
    else:
        downList[-1].update({downUrlList[index]: ""})

for downMap in downList:
    for url in downMap:
        # 打开新标签页
        bro.execute_script("window.open()")
        bro.switch_to.window(bro.window_handles[-1])
        bro.get(url)

        # 存储文件名
        tree = etree.HTML(bro.page_source)
        filename = tree.xpath('//div[@class="hd-des"]//i/text()')[0]
        downMap[url] = filename

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

sleep(0.5)
isDowning = True
while isDowning:
    listdir = os.listdir(config.get("browser-conf.down-location"))
    for file in listdir:
        if file.endswith(".crdownload"):
            sleep(0.5)
            break
    else:
        isDowning = False

# 鼠标悬停
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
