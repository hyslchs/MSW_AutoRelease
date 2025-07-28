import random
import pandas as pd

# === 資料載入區 ===
def load_item_data(csv_path):
    df = pd.read_csv(csv_path)

    # 將正確組合依據 correct_set 分組（排除 correct_set=0）
    valid_combinations = []
    for _, group in df[df["correct_set"] > 0].groupby("correct_set"):
        valid_combinations.append(group["item_id"].tolist())

    # 取出 correct_set=0 的干擾項目
    interference_pool = df[df["correct_set"] == 0]["item_id"].tolist()

    return valid_combinations, interference_pool

# === 抽取邏輯區 ===
def draw_batch(valid_combinations, interference_pool, total_count):
    """Draw a single batch using one correct combination."""
    selected_set = random.choice(valid_combinations)
    if total_count < len(selected_set):
        raise ValueError("總抽取數量不能小於正確組合長度")

    interference_count = total_count - len(selected_set)
    interference_part = random.choices(interference_pool, k=interference_count)

    batch = selected_set + interference_part
    random.shuffle(batch)
    return batch

# === 主程式 ===
if __name__ == "__main__":
    try:
        # 讀取資料
        valid_combinations, interference_pool = load_item_data("item_data.csv")

        total_count = int(input("請輸入每次總共要抽幾個編號（例如 10）："))

        batch = draw_batch(valid_combinations, interference_pool, total_count)

        print("\n✅ 抽取結果如下：")
        print(batch)

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
