# MSW_AutoRelease

### 需求
- 自行下載一個符合你系統環境的 chromedrive:
https://googlechromelabs.github.io/chrome-for-testing/
並且放置在同一路徑下

- 同一路徑下建立一個 `product_ids.txt`，裡面放你欲上架的商品 ID


---
### 操作流程
1. 先執行 `take_cookie.py` 手動登入後，在終端機輸入 `y` 儲存 cookies.pkl
(注意請手動輸入帳號密碼，第三方登入會被擋)

2. 接著執行 `main.py`，依照終端機的提示進行 一鍵上架/下架 的操作，會根據在 `product_ids.txt` 的順序執行，直到最後一行操作完畢為止

