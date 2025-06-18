import PyInstaller.__main__
import os


def create_exe_with_better_optimization():
    """
    優化版本：加入更多優化選項
    """
    icon_path = os.path.abspath("q3.ico")

    args = [
        "edid_format.py",
        "--onefile",
        "--noconsole",
        "--clean",
        "--name=EDID格式化工具 v1.1",
        "--icon=" + icon_path,
        # # 加入所有相關的 Python 檔案
        # "--add-data=XXX.py;.",
        # # 管理員權限
        # "--uac-admin",
        # 視窗設定
        "--windowed",
        # 優化選項
        "--optimize=2",  # Python 字節碼優化
        "--noupx",  # 不使用 UPX 壓縮（可能導致防毒軟體誤報）
    ]

    # PyQt5 相關依賴
    args.extend(
        [
            "--hidden-import=PyQt5.QtGui",
            "--hidden-import=PyQt5.QtWidgets",
            "--hidden-import=PyQt5.QtCore",
        ]
    )

    PyInstaller.__main__.run(args)


if __name__ == "__main__":

    create_exe_with_better_optimization()
