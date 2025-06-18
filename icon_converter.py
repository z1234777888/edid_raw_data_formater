import base64
import os


def convert_image_to_base64(image_path, output_file="icon_data.py"):
    """
    將圖片檔案轉換為 Base64 編碼的 Python 程式碼

    Args:
        image_path: 圖片檔案路徑
        output_file: 輸出的 Python 檔案名稱
    """

    if not os.path.exists(image_path):
        print(f"錯誤：找不到檔案 {image_path}")
        return

    try:
        # 讀取圖片檔案
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        # 轉換為 Base64
        base64_string = base64.b64encode(image_data).decode("utf-8")

        # 取得檔案名稱（不含副檔名）
        file_name = os.path.splitext(os.path.basename(image_path))[0]

        # 生成 Python 程式碼
        python_code = f'''"""
內嵌圖示資料模組
自動生成於圖片: {image_path}
"""

import base64
from PyQt6.QtGui import QIcon, QPixmap

# Base64 編碼的圖示資料
{file_name.upper()}_ICON_DATA = """
{base64_string}
"""

def get_{file_name}_icon():
    """返回 {file_name} 圖示"""
    pixmap = QPixmap()
    pixmap.loadFromData(base64.b64decode({file_name.upper()}_ICON_DATA))
    return QIcon(pixmap)

def get_{file_name}_pixmap():
    """返回 {file_name} 像素圖"""
    pixmap = QPixmap()
    pixmap.loadFromData(base64.b64decode({file_name.upper()}_ICON_DATA))
    return pixmap

# 使用範例:
# from {output_file.replace('.py', '')} import get_{file_name}_icon
# self.setWindowIcon(get_{file_name}_icon())
'''

        # 寫入檔案
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(python_code)

        print(f"✅ 成功！已生成 {output_file}")
        print(f"📁 圖片大小: {len(image_data)} bytes")
        print(f"📝 Base64 大小: {len(base64_string)} characters")
        print(f"\n使用方法:")
        print(f"from {output_file.replace('.py', '')} import get_{file_name}_icon")
        print(f"self.setWindowIcon(get_{file_name}_icon())")
        print(f"確認你使用的是PyQt6或是PyQt5，不要混用。")
    except Exception as e:
        print(f"錯誤：{e}")


def convert_multiple_images(image_paths, output_file="icons_data.py"):
    """
    轉換多個圖片檔案到一個 Python 檔案中
    """

    if not image_paths:
        print("錯誤：沒有提供圖片路徑")
        return

    python_code = '''"""
內嵌圖示資料模組
包含多個圖示的 Base64 資料
"""

import base64
from PyQt6.QtGui import QIcon, QPixmap

'''

    functions_code = ""

    for image_path in image_paths:
        if not os.path.exists(image_path):
            print(f"警告：找不到檔案 {image_path}，跳過...")
            continue

        try:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()

            base64_string = base64.b64encode(image_data).decode("utf-8")
            file_name = os.path.splitext(os.path.basename(image_path))[0]

            # 加入 Base64 資料
            python_code += f'''
# {image_path}
{file_name.upper()}_ICON_DATA = """
{base64_string}
"""
'''

            # 加入函數
            functions_code += f'''
def get_{file_name}_icon():
    """返回 {file_name} 圖示"""
    pixmap = QPixmap()
    pixmap.loadFromData(base64.b64decode({file_name.upper()}_ICON_DATA))
    return QIcon(pixmap)

def get_{file_name}_pixmap():
    """返回 {file_name} 像素圖"""
    pixmap = QPixmap()
    pixmap.loadFromData(base64.b64decode({file_name.upper()}_ICON_DATA))
    return pixmap
'''

            print(f"✅ 已處理: {image_path}")

        except Exception as e:
            print(f"錯誤處理 {image_path}: {e}")

    python_code += functions_code

    # 寫入檔案
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(python_code)
        print(f"\n🎉 成功生成 {output_file}！")
    except Exception as e:
        print(f"寫入檔案錯誤: {e}")


if __name__ == "__main__":
    print("🖼️  圖片轉 Base64 轉換器")
    print("=" * 40)

    # 單一檔案轉換範例
    image_file = input("請輸入圖片檔案路徑 (例: branch.ico): ").strip()

    if image_file:
        output_name = (
            input("請輸入輸出檔案名稱 (預設: icon_data.py): ").strip() or "icon_data.py"
        )
        convert_image_to_base64(image_file, output_name)
    else:
        print("沒有輸入檔案路徑，程式結束。")

    # 多檔案轉換範例（取消註解以使用）
    # image_files = ["branch.ico", "settings.png", "close.png"]
    # convert_multiple_images(image_files, "all_icons.py")
