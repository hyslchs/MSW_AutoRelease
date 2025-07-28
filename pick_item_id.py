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
def draw_batches(valid_combinations, interference_pool, total_count, correct_per_batch):
    selected_set = random.choice(valid_combinations)
    correct_pool = selected_set.copy()
    random.shuffle(correct_pool)

    max_batches = len(correct_pool) // correct_per_batch
    results = []

    for i in range(max_batches):
        correct_part = correct_pool[i * correct_per_batch : (i + 1) * correct_per_batch]
        interference_count = total_count - correct_per_batch
        interference_part = random.choices(interference_pool, k=interference_count)

        batch = correct_part + interference_part
        random.shuffle(batch)
        results.append(batch)

    return results

# === 主程式 ===
if __name__ == "__main__":
    try:
        # 讀取資料
        valid_combinations, interference_pool = load_item_data("item_data.csv")

        total_count = int(input("請輸入每次總共要抽幾個編號（例如 10）："))
        correct_per_batch = int(input("請輸入每次要包含的正確編號數（例如 2）："))

        if correct_per_batch >= total_count:
            raise ValueError("正確編號數不能大於或等於總抽取數量")

        batches = draw_batches(valid_combinations, interference_pool, total_count, correct_per_batch)

        if not batches:
            print("⚠️ 無法抽出任何一組，可能是正確編號不足。")
        else:
            print("\n✅ 抽取結果如下：")
            for idx, batch in enumerate(batches, start=1):
                print(f"第 {idx} 組：{batch}")

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
