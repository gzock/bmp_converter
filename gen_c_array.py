#!/usr/bin/env python3
import sys
from PIL import Image

def bmp_to_rgb565_rle(bmp_file_path, array_name="bmp_image_array"):
    """
    指定したBMPファイルを読み込み、各ピクセルをRGB565形式に変換し、
    同じ値が連続する場合には(値, 個数)のランレングス形式にまとめて
    C言語配列として出力するソースコード文字列を返す関数。

    :param bmp_file_path: BMPファイルのパス
    :param array_name: 出力するC言語配列の名前
    :return: 生成したCソースコード文字列
    """

    # 画像を開いてRGBモードに変換
    img = Image.open(bmp_file_path).convert("RGB")
    width, height = img.size

    # ピクセルデータを取得(左上→右下へラスタスキャン順)
    pixels = list(img.getdata())

    # ---- RGB888 → RGB565 の数値へ変換 ----
    rgb565_list = []
    for (r, g, b) in pixels:
        r5 = (r >> 3) & 0x1F
        g6 = (g >> 2) & 0x3F
        b5 = (b >> 3) & 0x1F
        rgb565 = (r5 << 11) | (g6 << 5) | b5
        rgb565_list.append(rgb565)

    # ---- 同じ値の連続をまとめる(RLE) ----
    rle_pairs = []
    if not rgb565_list:
        # 画像が空の場合
        pass
    else:
        current_val = rgb565_list[0]
        count = 1
        for val in rgb565_list[1:]:
            if val == current_val:
                count += 1
            else:
                # 連続終了
                rle_pairs.append((current_val, count))
                current_val = val
                count = 1
        # 最後に残った要素を追加
        rle_pairs.append((current_val, count))

    # ---- C言語ソースの文字列を組み立て ----
    c_code_lines = []
    c_code_lines.append('#include <stdint.h>')
    c_code_lines.append('')
    c_code_lines.append(f'// Original BMP size: {width} x {height}')
    c_code_lines.append(f'// Compressed RLE array for: {bmp_file_path}')
    c_code_lines.append('')

    # 配列定義開始
    c_code_lines.append(f'// pairs: color, repeat_count')
    c_code_lines.append(f'uint16_t {array_name}[] = {{')

    # ペアを追加
    row_data = []
    for (color, count) in rle_pairs:
        # 16進数表記 + 10進数表記の繰り返し数
        row_data.append(f'0x{color:04X}, {count}')

        # ある程度で折り返す(好みに応じて調整)
        if len(row_data) >= 4:
            c_code_lines.append('    ' + ', '.join(row_data) + ',')
            row_data = []

    # 端数を出力
    if row_data:
        c_code_lines.append('    ' + ', '.join(row_data) + ',')

    # 配列定義終了
    c_code_lines.append('};')
    c_code_lines.append('')

    # 要素数 (ペアなので実際に画素展開するときは2ステップで読む)
    c_code_lines.append(f'#define {array_name.upper()}_LENGTH (sizeof({array_name})/sizeof({array_name}[0]))')
    c_code_lines.append('')

    return "\n".join(c_code_lines)

def main():
    """
    コマンドライン引数:
        1: BMPファイル
        2: 出力C配列名 (任意)
    例:
        python bmp2rgb565_rle.py sample.bmp bmp_image_array
    """
    if len(sys.argv) < 2:
        print("Usage: bmp2rgb565_rle.py <bmp_file> [c_array_name]")
        sys.exit(1)

    bmp_file = sys.argv[1]
    array_name = sys.argv[2] if len(sys.argv) > 2 else "bmp_image_array"

    # RLE Cコード生成
    c_code = bmp_to_rgb565_rle(bmp_file, array_name)

    # 標準出力に表示 (必要に応じてファイル書き出しでもOK)
    print(c_code)

if __name__ == "__main__":
    main()
