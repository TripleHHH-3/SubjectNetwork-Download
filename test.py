from selenium import webdriver
# 实现无可视化界面
from selenium.webdriver.chrome.options import Options
# 实现规避检测
from selenium.webdriver import ChromeOptions
from selenium.webdriver import ActionChains

from common.ReadYaml import ReadYaml

config = ReadYaml("./resources/application.yml", "utf-8")

# 实现规避检测
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])

bro = webdriver.Chrome(executable_path='./resources/chromedriver', options=option)

bro.get("https://www.baidu.com/")

bro.execute_script("window.open()")
print(type(bro.window_handles))
bro.switch_to.window(bro.window_handles[1])
bro.get("https://www.baidu.com/")


bro.execute_script("window.open()")

bro.switch_to.window(bro.window_handles[2])
bro.get("https://www.baidu.com/")

print(len(bro.window_handles))

bro.close()
bro.switch_to.window(bro.window_handles[1])
bro.close()


# 进入网址
# bro.get(config.get("base-url"))

# bro.get("http://www.zxxk.com/soft/25810958.html")

# # 点击登录
# login_btn = bro.find_element_by_class_name('login-btn')
# login_btn.click()
#
# # 切换到账号密码登录
# lcon_weixin = bro.find_element_by_class_name('lcon-weixin')
# lcon_weixin.click()
#
# # 输入账号密码
# username = bro.find_element_by_xpath('//*[@id="username"]')
# username.send_keys(config.get("account.username"))
# psd = bro.find_element_by_xpath('//*[@id="ordinaryLoginTab"]/li[2]/div/input')
# psd.send_keys(config.get("account.password"))
#
# # 点击登录按钮
# CommonLogin = bro.find_element_by_id("CommonLogin")
# CommonLogin.click()
#
# # 鼠标悬停
# action = ActionChains(bro)
# LoginInfo = bro.find_element_by_id("LoginInfo")
# action.move_to_element(LoginInfo).perform()
#
# # 退出
# logout = bro.find_element_by_xpath('//*[@id="LoginInfo"]/div[1]/div/div[1]/a[2]')
# logout.click()
