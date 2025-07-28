import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def open_browser():
    """Open a browser window for manual login and return the driver."""
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.get("https://maplestoryworlds.nexon.com")
    return driver


def save_cookies(driver, cookie_path="cookies.pkl"):
    """Save cookies from the given driver to ``cookie_path``."""
    with open(cookie_path, "wb") as f:
        pickle.dump(driver.get_cookies(), f)
    print("✅ Cookies 已儲存完成！")


if __name__ == "__main__":
    driver = open_browser()
    print("✅ 請手動完成登入，完成後在終端機輸入 'y' 並按下 Enter")
    while True:
        confirm = input("登入完成後輸入 'y'：")
        if confirm.lower() == "y":
            break
        else:
            print("請輸入小寫 'y' 繼續。")

    save_cookies(driver)
    driver.quit()
