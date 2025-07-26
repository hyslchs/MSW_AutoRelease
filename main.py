import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === 設定 Selenium 瀏覽器選項 ===
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # 最大化視窗
# chrome_options.add_argument("--headless")       # 無頭模式（若不需要顯示視窗）

# === 初始化 Driver ===
service = Service()  # 可指定 chromedriver 路徑，例如 Service("chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# === 1. 先進入網域以便設置 Cookie ===
url = "https://maplestoryworlds.nexon.com/zh-tw/"
driver.get(url)
time.sleep(3)  # 確保網頁載入完成

# === 2. 載入並添加 cookie ===
try:
    with open("cookies.pkl", "rb") as f:
        cookies = pickle.load(f)
    for cookie in cookies:
        # 有些 cookie 可能缺少 'sameSite'，會導致 add_cookie 出錯
        cookie.pop('sameSite', None)
        driver.add_cookie(cookie)
    print("✅ 已成功導入 cookies")
except Exception as e:
    print("❌ Cookie 載入失敗：", e)
    driver.quit()
    exit()

# === 3. 登入完成後重新載入目標頁面 ===
target_url = "https://maplestoryworlds.nexon.com/zh-tw/avatar/register/76O1F77UL"
driver.get(target_url)
time.sleep(3)

# === 4. 點擊「上架」按鈕 ===
try:
    publish_label = driver.find_element(By.XPATH, "//label[@for='published' and contains(@class, 'check__radio')]")
    driver.execute_script("arguments[0].click();", publish_label)
    print("✅ 已點擊『上架』按鈕")
except Exception as e:
    print("❌ 無法點擊『上架』按鈕：", e)

# === 5. 點擊「修改」按鈕 ===
try:
    wait = WebDriverWait(driver, 10)
    # 改用包含文字「修改」的按鈕
    modify_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(@class, 'btn') and contains(., '修改')]"
    )))
    driver.execute_script("arguments[0].click();", modify_button)
    print("✅ 已點擊『修改』按鈕")
except Exception as e:
    print("❌ 點擊『修改』按鈕失敗：", e)

# === 6. 停留等待後續指令 ===
input("🕒 操作完成，請按 Enter 鍵結束程式...")
driver.quit()
