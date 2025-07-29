import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ID_FILE = "product_ids.txt"
URL_PREFIX = "https://maplestoryworlds.nexon.com/zh-tw/avatar/register/"
BATCH_SIZE = 10


def login(driver, cookie_path="cookies.pkl"):
    driver.get("https://maplestoryworlds.nexon.com/zh-tw/")
    time.sleep(2)
    with open(cookie_path, "rb") as f:
        cookies = pickle.load(f)
    for cookie in cookies:
        cookie.pop("sameSite", None)
        driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(2)
    close_popup_if_exists(driver)
    print("✅ 已成功登入")


def close_popup_if_exists(driver):
    try:
        close_btns = driver.find_elements(
            By.XPATH,
             "//button[contains(@class, 'btn') and contains(@class, 'btn_none') and contains(., 'Do Not Show Again Today')]",
        )
        if close_btns:
            driver.execute_script("arguments[0].click();", close_btns[0])
            print("🔕 已關閉彈出式視窗")
    except Exception:
        pass  # 如果沒有跳窗就略過


def open_browser_and_login(cookie_path="cookies.pkl"):
    """Open browser, login with saved cookies and return driver."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)
    login(driver, cookie_path)
    return driver


def process_batch(driver, item_ids, mode):
    """Process a list of item IDs with the given mode."""
    for item_id in item_ids:
        url = URL_PREFIX + item_id
        process_product(driver, url, mode)


def load_product_urls(id_file):
    with open(id_file, "r", encoding="utf-8") as f:
        ids = [line.strip() for line in f if line.strip()]
    return [URL_PREFIX + pid for pid in ids]


def select_mode():
    print("\n🔧 請選擇要執行的操作模式：")
    print("[1] 上架商品")
    print("[2] 下架商品")
    print("[q] 離開程式")
    while True:
        mode = input("👉 請輸入選項：").strip().lower()
        if mode in ["1", "2", "q"]:
            return mode
        print("⚠️ 無效輸入，請輸入 1、2 或 q")


def process_product(driver, url, mode):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        close_popup_if_exists(driver)

        if mode == "1":
            label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='published' and contains(@class, 'check__radio')]")))
            driver.execute_script("arguments[0].click();", label)
            print(f"✅ 上架：{url}")
        elif mode == "2":
            label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='unPublished' and contains(@class, 'check__radio')]")))
            driver.execute_script("arguments[0].click();", label)
            print(f"✅ 下架：{url}")
        else:
            print("⚠️ 模式錯誤，跳過")
            return

        #time.sleep(0.5)
        modify_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn') and contains(., '修改')]")))
        driver.execute_script("arguments[0].click();", modify_btn)
        print("✅ 修改完成")
        #time.sleep(1)

    except Exception as e:
        print(f"❌ 操作失敗：{url}\n原因：{e}")


def main():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    try:
        login(driver)
        product_urls = load_product_urls(ID_FILE)
        total = len(product_urls)
        user_quit = False

        while True:
            mode = select_mode()
            if mode == "q":
                print("👋 程式結束。")
                user_quit = True
                break

            index = 0
            while index < total:
                batch = product_urls[index:index + BATCH_SIZE]
                print(f"\n🚀 處理第 {index + 1} ~ {index + len(batch)} 件商品...")
                for url in batch:
                    process_product(driver, url, mode)
                index += len(batch)

                if index >= total:
                    print("✅ 所有商品處理完畢！")
                    break

                again = input("\n是否繼續下一批？[Enter 繼續 / q 結束當前模式]：").strip().lower()
                if again == "q":
                    break

        if not user_quit:
            input("\n🕒 按 Enter 鍵關閉瀏覽器...")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
