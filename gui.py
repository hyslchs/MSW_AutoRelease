import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import take_cookie
from pick_item_id import load_item_data, draw_batch
from main import open_browser_and_login, process_batch

# Status message handling
status_var = None


def update_status(msg):
    """Display a status message in the GUI and print it."""
    if status_var is not None:
        status_var.set(msg)
    print(msg)

# Global state
manual_driver = None
main_driver = None
batches = []
selected_index = 0

# Data loaded from CSV
valid_map = {}
interference_pool = []


def open_manual_browser():
    global manual_driver
    if manual_driver:
        update_status("瀏覽器已開啟")
        return
    manual_driver = take_cookie.open_browser()
    update_status("請在瀏覽器中登入，完成後點擊『儲存 Cookie 並關閉瀏覽器』")


def save_cookie_and_close():
    global manual_driver
    if not manual_driver:
        update_status("尚未開啟瀏覽器")
        return
    take_cookie.save_cookies(manual_driver)
    manual_driver.quit()
    manual_driver = None
    update_status("Cookie 已儲存")


def browse_csv():
    path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if path:
        csv_path_var.set(path)
        try:
            global valid_map, interference_pool
            valid_map, interference_pool, sets = load_item_data(path)
            correct_combo['values'] = [str(s) for s in sets]
            if sets:
                correct_set_var.set(str(sets[0]))
        except Exception as e:
            update_status(str(e))


def generate_batch():
    """Generate a single batch and display it in the listbox."""
    global batches
    try:
        if not valid_map and not interference_pool:
            update_status("請先選擇 CSV 檔")
            return

        interference = int(interference_var.get())
        selected = correct_set_var.get().strip()
        selected = selected if selected else None

        batch = draw_batch(valid_map, interference_pool, interference, selected)
        batches = [batch]
        listbox.delete(0, tk.END)
        listbox.insert(tk.END, f"第 1 組：{batch}")
        listbox.selection_set(0)
    except Exception as e:
        update_status(str(e))


def on_select(event):
    global selected_index
    sel = listbox.curselection()
    if sel:
        selected_index = sel[0]


def open_auto_browser():
    global main_driver
    if main_driver:
        update_status("瀏覽器已開啟")
        return
    main_driver = open_browser_and_login()
    update_status("已自動登入完成")


def start_publish(mode):
    if not main_driver:
        update_status("請先開啟瀏覽器並登入")
        return
    if not batches:
        update_status("請先產生抽取結果")
        return
    ids = batches[selected_index]
    process_batch(main_driver, ids, mode)
    update_status("操作完成")


def close_main_browser():
    global main_driver
    if main_driver:
        main_driver.quit()
        main_driver = None


root = tk.Tk()
root.title("MSW Auto Release")
status_var = tk.StringVar()

# ----- Step 1 -----
frame1 = tk.LabelFrame(root, text="1. 手動登入並儲存 Cookie")
frame1.pack(fill="x", padx=10, pady=5)

btn_open = tk.Button(frame1, text="開啟瀏覽器並手動登入", command=open_manual_browser)
btn_open.pack(side="left", padx=5, pady=5)

btn_save = tk.Button(frame1, text="儲存 Cookie 並關閉瀏覽器", command=save_cookie_and_close)
btn_save.pack(side="left", padx=5, pady=5)

# ----- Step 2 -----
frame2 = tk.LabelFrame(root, text="2. 抽取商品ID")
frame2.pack(fill="x", padx=10, pady=5)

csv_path_var = tk.StringVar()
entry_csv = tk.Entry(frame2, textvariable=csv_path_var, width=40)
entry_csv.pack(side="left", padx=5)
btn_browse = tk.Button(frame2, text="選擇 CSV", command=browse_csv)
btn_browse.pack(side="left", padx=5)

subframe = tk.Frame(frame2)
subframe.pack(fill="x", pady=5)

tk.Label(subframe, text="要加入干擾 ID 數量").grid(row=0, column=0)

interference_var = tk.StringVar(value="5")

tk.Entry(subframe, textvariable=interference_var, width=5).grid(row=0, column=1)

tk.Label(subframe, text="correct_set").grid(row=0, column=2, padx=(10,0))
correct_set_var = tk.StringVar()
correct_combo = ttk.Combobox(subframe, textvariable=correct_set_var, values=[])
correct_combo.grid(row=0, column=3)

btn_generate = tk.Button(subframe, text="產生結果", command=generate_batch)
btn_generate.grid(row=0, column=4, padx=5)

listbox = tk.Listbox(frame2, height=5)
listbox.pack(fill="x", padx=5, pady=5)
listbox.bind("<<ListboxSelect>>", on_select)

# ----- Step 3 -----
frame3 = tk.LabelFrame(root, text="3. 自動上架/下架")
frame3.pack(fill="x", padx=10, pady=5)

btn_login = tk.Button(frame3, text="開啟瀏覽器並自動登入", command=open_auto_browser)
btn_login.pack(side="left", padx=5, pady=5)

btn_publish = tk.Button(frame3, text="一鍵上架", command=lambda: start_publish("1"))
btn_publish.pack(side="left", padx=5, pady=5)

btn_unpublish = tk.Button(frame3, text="一鍵下架", command=lambda: start_publish("2"))
btn_unpublish.pack(side="left", padx=5, pady=5)

btn_close = tk.Button(frame3, text="關閉瀏覽器", command=close_main_browser)
btn_close.pack(side="left", padx=5, pady=5)

# ----- Status Bar -----
status_label = tk.Label(root, textvariable=status_var, anchor="w")
status_label.pack(fill="x", padx=5, pady=5)

root.mainloop()
