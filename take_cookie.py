import time
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 初始化瀏覽器
options = Options()
driver = webdriver.Chrome(options=options)

# 開啟目標網站
driver.get("https://maplestoryworlds.nexon.com")
print("✅ 請手動完成登入，完成後在終端機輸入 'y' 並按下 Enter")

# 等待使用者輸入
while True:
    confirm = input("登入完成後輸入 'y'：")
    if confirm.lower() == "y":
        break
    else:
        print("請輸入小寫 'y' 繼續。")

# 儲存 cookies
with open("cookies.pkl", "wb") as f:
    pickle.dump(driver.get_cookies(), f)

print("✅ Cookies 已儲存完成！")
driver.quit()
