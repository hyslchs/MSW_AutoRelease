# MSW_AutoRelease

## Requirements
- Download a ChromeDriver that matches your OS from
  <https://googlechromelabs.github.io/chrome-for-testing/> and place it in the
  same directory.
- Prepare an `item_data.csv` file which contains your product information.
- Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage
Run the GUI and follow the on screen steps:

```bash
python gui.py
```

### Workflow
1. **Manual login** – Click *"開啟瀏覽器並手動登入"* and sign in manually.
   Afterwards click *"儲存 Cookie 並關閉瀏覽器"* to store `cookies.pkl`.
2. **Generate item batches** – Choose `item_data.csv`, set the total amount and
   the number of correct IDs for each batch, then click *"產生結果"*. Select one
   of the generated batches in the list.
3. **Auto upload/remove** – Click *"開啟瀏覽器並自動登入"* and then choose either
   *"一鍵上架"* or *"一鍵下架"* to process the selected batch. The browser will
   remain open so you can continue running operations.
4. Click *"關閉瀏覽器"* when you are done.

The original command line scripts `take_cookie.py`, `pick_item_id.py` and
`main.py` remain available if you prefer using the terminal.
