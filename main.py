import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === 設定 ===
ID_FILE = "product_ids.txt"
URL_PREFIX = "https://maplestoryworlds.nexon.com/zh-tw/avatar/register/"
BATCH_SIZE = 10

# === 載入商品 ID 清單 ===
def load_product_urls(id_file):
    with open(id_file, "r", encoding="utf-8") as f:
        ids = [line.strip() for line in f if line.strip()]
    return [URL_PREFIX + pid for pid in ids]

# === 載入 cookie 登入 ===
def load_cookies(driver, cookie_path="cookies.pkl"):
    driver.get("https://maplestoryworlds.nexon.com/zh-tw/")
    time.sleep(2)
    with open(cookie_path, "rb") as f:
        cookies = pickle.load(f)
    for cookie in cookies:
        cookie.pop("sameSite", None)
        driver.add_cookie(cookie)
    print("✅ Cookies 載入完成")

# === 單一商品操作 ===
def process_product(driver, url, mode):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        if mode == "1":
            label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='published' and contains(@class, 'check__radio')]")))
            driver.execute_script("arguments[0].click();", label)
            print(f"✅ 上架：{url}")
        elif mode == "2":
            label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='unPublished' and contains(@class, 'check__radio')]")))
            driver.execute_script("arguments[0].click();", label)
            print(f"✅ 下架：{url}")
        else:
            print("⚠️ 模式無效，跳過")
            return

        time.sleep(0.5)
        modify_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn') and contains(., '修改')]")))
        driver.execute_script("arguments[0].click();", modify_btn)
        print(f"✅ 修改完成：{url}")
        time.sleep(1)

    except Exception as e:
        print(f"❌ 操作失敗：{url}\n原因：{e}")

# === 主流程 ===
def main():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    try:
        load_cookies(driver)
        product_urls = load_product_urls(ID_FILE)

        total = len(product_urls)
        index = 0

        while index < total:
            print("\n🔸 請選擇操作模式：")
            print("[1] 上架 10 件")
            print("[2] 下架 10 件")
            print("[q] 離開程式")
            choice = input("👉 請輸入選項：").strip().lower()

            if choice == "q":
                print("👋 已結束程式")
                break
            elif choice not in ["1", "2"]:
                print("⚠️ 無效輸入，請重新輸入 1 / 2 / q")
                continue

            batch = product_urls[index:index + BATCH_SIZE]
            print(f"\n🚀 處理第 {index + 1} ~ {index + len(batch)} 件商品...")
            for url in batch:
                process_product(driver, url, choice)

            index += len(batch)

            if index >= total:
                print("✅ 所有商品已處理完畢！")
                break

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
