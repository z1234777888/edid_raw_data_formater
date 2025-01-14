import sys
import re
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QTextEdit,
    QPushButton,
)
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from PyQt5.QtCore import Qt


class EDIDReaderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EDID Formater V1.0")
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #C4E1E1;
            }
            QTextEdit {
                background-color: white;
            }
            QCheckBox {
                background-color: transparent;
            }
            QLabel {
                background-color: transparent;
            }
        """
        )

        # 設定字體
        self.setup_fonts()

        # Set window icon
        if getattr(sys, "frozen", False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))

        icon_path = os.path.join(application_path, "q3.ico")

        try:
            self.setWindowIcon(QIcon(icon_path))
        except:
            print(f"Warning: Icon file not found at {icon_path}")

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title_label = QLabel("EDID:")
        title_label.setFont(self.title_font)
        main_layout.addWidget(title_label)

        # Checkboxes layout
        checkbox_layout = QHBoxLayout()

        self.add_line_breaks = QCheckBox("Add Line Breaks")
        self.add_commas = QCheckBox("Add Commas")
        self.add_hex_prefix = QCheckBox("Add Hex Prefix (0x)")

        # 設定 checkbox 字體
        for checkbox in [self.add_line_breaks, self.add_commas, self.add_hex_prefix]:
            checkbox.setFont(self.monospace_font)

        checkbox_layout.addWidget(self.add_line_breaks)
        checkbox_layout.addWidget(self.add_commas)
        checkbox_layout.addWidget(self.add_hex_prefix)
        checkbox_layout.addStretch()
        main_layout.addLayout(checkbox_layout)

        # Text area
        self.edid_text = QTextEdit()
        self.edid_text.setFont(self.monospace_font)
        self.edid_text.setAcceptRichText(False)
        main_layout.addWidget(self.edid_text)

        # Parse button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        parse_button = QPushButton("Format!")
        parse_button.clicked.connect(self.format_edid)
        parse_button.setFont(self.monospace_font)
        button_layout.addWidget(parse_button)

        main_layout.addLayout(button_layout)

        # Footer
        footer_layout = QVBoxLayout()

        reference_label = QLabel("reference http://www.edidreader.com/")
        reference_label.setAlignment(Qt.AlignRight)
        reference_label.setFont(self.small_font)
        reference_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard
        )
        reference_label.setCursor(Qt.IBeamCursor)
        footer_layout.addWidget(reference_label)

        creator_label = QLabel("tool created by ken冠魁")
        creator_label.setAlignment(Qt.AlignRight)
        creator_label.setFont(self.small_font)
        footer_layout.addWidget(creator_label)

        main_layout.addLayout(footer_layout)

        # Set window size
        self.resize(750, 720)

    def setup_fonts(self):
        """設定字體，包含備用字體"""
        # 獲取系統中可用的字體
        available_fonts = QFontDatabase().families()

        # 定義首選字體列表
        monospace_fonts = [
            "JetBrains Mono NL",
            "Monospace",
            "Consolas",
        ]

        # 選擇第一個可用的等寬字體
        selected_font = None
        for font_name in monospace_fonts:
            if font_name in available_fonts:
                selected_font = font_name
                break

        # 如果沒有找到任何首選字體，使用系統預設等寬字體
        if not selected_font:
            font = QFont()
            font.setStyleHint(QFont.Monospace)
            selected_font = font.defaultFamily()

        # 建立各種字體實例
        self.title_font = QFont(selected_font, 16)
        self.monospace_font = QFont(selected_font, 10)
        self.monospace_font.setFixedPitch(True)
        self.small_font = QFont(selected_font, 8)

    def format_edid(self):
        # Get checkbox states
        line_breaks = self.add_line_breaks.isChecked()
        commas = self.add_commas.isChecked()
        hex_prefix = self.add_hex_prefix.isChecked()

        # Get the raw EDID text
        raw_edid_text = self.edid_text.toPlainText().strip()

        try:
            # Function to extract hex values from different input formats
            def extract_hex(text):
                # Remove existing formatting
                text = re.sub(r"0x|\s|-|,", "", text)
                return [text[i : i + 2] for i in range(0, len(text), 2)]

            # Extract hex bytes
            hex_bytes = extract_hex(raw_edid_text)

            # Validate EDID length
            if len(hex_bytes) % 128 != 0:
                raise ValueError("EDID length must be a multiple of 128 bytes")

            # Validate EDID header
            expected_header = ["00", "FF", "FF", "FF", "FF", "FF", "FF", "00"]
            if len(hex_bytes) >= 8:  # Make sure we have enough bytes to check
                actual_header = [byte.upper() for byte in hex_bytes[:8]]
                if actual_header != expected_header:
                    raise ValueError(
                        "Invalid EDID header: expecting 00 FF FF FF FF FF FF 00"
                    )

            # Format the hex bytes according to user preferences
            formatted_edid = ""
            for i, byte in enumerate(hex_bytes):
                if hex_prefix:
                    formatted_edid += "0x"
                formatted_edid += byte.upper()

                if i < len(hex_bytes) - 1:  # Don't add separator after last byte
                    if commas:
                        formatted_edid += ", "
                    else:
                        formatted_edid += " "

                if line_breaks:
                    if (i + 1) % 16 == 0:  # Every 16 bytes
                        formatted_edid += "\n"
                        if (i + 1) % 128 == 0:  # Every 8 groups of 16 bytes
                            formatted_edid += "\n"  # Extra line break

            # Update the text widget with the formatted text
            self.edid_text.setText(formatted_edid)

            print("Parsed EDID:")
            print(formatted_edid)

        except Exception as e:
            error_message = f"Error parsing EDID: {str(e)}"
            self.edid_text.setText(error_message)
            print(error_message)


def main():
    app = QApplication(sys.argv)
    window = EDIDReaderGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
