import random

# 可湊成一套的組合
valid_combinations = [
    ["aaaaa", "bbbbb", "ccccc", "ddddd"],
    ["eeeee", "fffff", "ggggg", "hhhhh"]
]

# 干擾用編號（可重複使用）
interference_pool = [
    "isudje", "ksjdi", "jsidw", "ksjdi", "ksjdo",
    "ksodw", "jsosw", "cjdls", "ksodq", "cjflo",
    "spdqw", "yuwie"
]

def draw_batches(total_count, correct_per_batch):
    # 選一組正確編號組合
    selected_set = random.choice(valid_combinations)
    correct_pool = selected_set.copy()
    random.shuffle(correct_pool)

    # 計算最多可抽幾次
    max_batches = len(correct_pool) // correct_per_batch
    results = []

    for i in range(max_batches):
        # 取出 M 個正確編號（不重複）
        correct_part = correct_pool[i * correct_per_batch : (i + 1) * correct_per_batch]

        # 干擾用數量 = N - M
        interference_count = total_count - correct_per_batch
        interference_part = random.choices(interference_pool, k=interference_count)

        batch = correct_part + interference_part
        random.shuffle(batch)
        results.append(batch)

    return results

# 主程式
if __name__ == "__main__":
    try:
        total_count = int(input("請輸入每次總共要抽幾個編號（例如 10）："))
        correct_per_batch = int(input("請輸入每次要包含的正確編號數（例如 2）："))

        if correct_per_batch >= total_count:
            raise ValueError("正確編號數不能大於或等於總抽取數量")

        batches = draw_batches(total_count, correct_per_batch)

        if not batches:
            print("⚠️ 無法抽出任何一組，可能是正確編號不足。")
        else:
            print("\n✅ 抽取結果如下：")
            for idx, batch in enumerate(batches, start=1):
                print(f"第 {idx} 組：{batch}")

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
