import random
import pandas as pd

# === 資料載入區 ===
def load_item_data(csv_path):
    """Load item data and return (valid_map, interference_pool, all_sets).

    ``correct_set`` values can be either numbers or text. ``0`` is reserved for
    interference items.
    """
    df = pd.read_csv(csv_path, dtype={"correct_set": str})
    df["correct_set"] = df["correct_set"].str.strip()

    # Group by correct_set excluding '0' to build valid_map
    valid_map = {
        cs: group["item_id"].tolist()
        for cs, group in df[df["correct_set"] != "0"].groupby("correct_set")
    }

    # Items marked with correct_set '0' are used as interference
    interference_pool = (
        df[df["correct_set"] == "0"]["item_id"].drop_duplicates().tolist()
    )

    all_sets = df["correct_set"].drop_duplicates().tolist()

    return valid_map, interference_pool, all_sets

# === 抽取邏輯區 ===
def draw_batch(valid_map, interference_pool, total_count, correct_set=None):
    """Draw a single batch using one correct combination.

    Parameters
    ----------
    valid_map : dict
        Mapping from correct_set value to list of item IDs.
    interference_pool : list
        List of item IDs available for interference.
    total_count : int
        Total number of IDs to draw.
    correct_set : str or None
        If provided, use this ``correct_set`` instead of picking randomly.
    """
    if correct_set is None:
        # Randomly choose a valid set when not specified
        selected_set = random.choice(list(valid_map.values())) if valid_map else []
    else:
        selected_set = valid_map.get(str(correct_set), [])

    if total_count < len(selected_set):
        raise ValueError("總抽取數量不能小於正確組合長度")

    interference_count = total_count - len(selected_set)

    if interference_count > len(interference_pool):
        raise ValueError("干擾項目不足以進行不重複抽取")

    # 使用 sample 以避免抽到重複編號
    interference_part = random.sample(interference_pool, k=interference_count)

    batch = selected_set + interference_part
    random.shuffle(batch)
    return batch

# === 主程式 ===
if __name__ == "__main__":
    try:
        # 讀取資料
        valid_map, interference_pool, all_sets = load_item_data("item_data.csv")

        print(f"可選擇的 correct_set 有: {all_sets}")
        selected = input("請輸入要使用的 correct_set (留空則隨機)：").strip()
        selected = selected if selected else None

        total_count = int(input("請輸入每次總共要抽幾個編號（例如 10）："))

        batch = draw_batch(valid_map, interference_pool, total_count, selected)

        print("\n✅ 抽取結果如下：")
        print(batch)

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
