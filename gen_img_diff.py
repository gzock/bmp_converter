#!/usr/bin/env python3

import sys
from PIL import Image

def bmp_to_rgb565_list(bmp_file_path):
    """
    指定したBMPファイルを読み込み、各ピクセルをRGB565形式の16ビット値に変換し、
    その配列（リスト）を返す。
    """
    img = Image.open(bmp_file_path).convert("RGB")
    width, height = img.size
    pixels = list(img.getdata())

    rgb565_list = []
    for (r, g, b) in pixels:
        r5 = (r >> 3) & 0x1F
        g6 = (g >> 2) & 0x3F
        b5 = (b >> 3) & 0x1F
        rgb565 = (r5 << 11) | (g6 << 5) | b5
        rgb565_list.append(rgb565)

    return (width, height, rgb565_list)

def compare_rgb565_lists(list1, list2):
    """
    2つのRGB565リストを比較し、差分がある要素のみ抽出して返す。
    戻り値: [(index, value1, value2, diff), ...] のリスト
    """
    differences = []
    length = len(list1)
    for i in range(length):
        val1 = list1[i]
        val2 = list2[i]
        if val1 != val2:
            # 差分(ここでは val2 - val1 を出力する例)
            diff = val2 - val1
            differences.append((i, val1, val2, diff))
    return differences

def main():
    """
    python diff_bmp_rgb565.py <bmp_file1> <bmp_file2>

    1) 2つのBMPを読み込み
    2) サイズ・ピクセル数を比較
    3) RGB565変換リストを比較して差分を抽出
    4) 結果を出力
    """
    if len(sys.argv) < 3:
        print("Usage: diff_bmp_rgb565.py <bmp_file1> <bmp_file2>")
        sys.exit(1)

    bmp_file1 = sys.argv[1]
    bmp_file2 = sys.argv[2]

    # 画像1読み込み
    width1, height1, rgb565_list1 = bmp_to_rgb565_list(bmp_file1)
    # 画像2読み込み
    width2, height2, rgb565_list2 = bmp_to_rgb565_list(bmp_file2)

    # サイズ比較
    if (width1 != width2) or (height1 != height2):
        print("Error: 画像サイズが異なるため、差分比較はできません。")
        sys.exit(1)

    # 差分比較
    differences = compare_rgb565_lists(rgb565_list1, rgb565_list2)

    # 結果出力
    print(f"画像サイズ: {width1} x {height1}")
    print(f"総ピクセル数: {width1 * height1}")

    if not differences:
        print("差分はありません。両画像は同一です。")
    else:
        print(f"差分数: {len(differences)}")
        print("差分詳細: (index: old -> new, diff)")
        for idx, old_val, new_val, diff in differences:
            print(f"  Index {idx}: 0x{old_val:04X} -> 0x{new_val:04X} (diff={diff:+d})")

if __name__ == "__main__":
    main()
