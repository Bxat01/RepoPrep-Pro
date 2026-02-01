STYLESHEET = """
QMainWindow {
    background-color: #2d2d2d;
    color: #ffffff;
}

QGroupBox {
    border: 2px solid #444444;
    border-radius: 8px;
    margin-top: 15px;
    padding-top: 15px;
    color: #ffffff;
    font-weight: bold;
    font-size: 14px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 10px 0 10px;
    color: #64b5f6;
}

QPushButton {
    background-color: #3c3c3c;
    border: 1px solid #555555;
    border-radius: 5px;
    padding: 10px 20px;
    color: #ffffff;
    font-weight: bold;
    font-size: 13px;
    min-width: 100px;
}

QPushButton:hover {
    background-color: #4a4a4a;
    border-color: #64b5f6;
}

QPushButton:pressed {
    background-color: #2c3e50;
    border-color: #3498db;
}

QPushButton:disabled {
    background-color: #2b2b2b;
    color: #777777;
    border-color: #3c3c3c;
}

QLineEdit {
    background-color: #3c3c3c;
    border: 1px solid #555555;
    border-radius: 5px;
    padding: 10px;
    color: #ffffff;
    font-size: 13px;
    selection-background-color: #3498db;
}

QLineEdit:disabled {
    background-color: #2b2b2b;
    color: #777777;
}

QTextEdit {
    background-color: #252525;
    border: 1px solid #444444;
    border-radius: 5px;
    color: #dddddd;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 12px;
    padding: 10px;
}

QLabel {
    color: #ffffff;
    padding: 3px;
}

QStatusBar {
    background-color: #3c3c3c;
    color: #ffffff;
    font-size: 12px;
}

QProgressBar {
    border: 1px solid #555555;
    border-radius: 5px;
    text-align: center;
    color: #ffffff;
    background-color: #3c3c3c;
}

QProgressBar::chunk {
    background-color: #4CAF50;
    border-radius: 5px;
}

QMenuBar {
    background-color: #3c3c3c;
    color: #ffffff;
}

QMenuBar::item:selected {
    background-color: #505050;
}

QMenu {
    background-color: #3c3c3c;
    color: #ffffff;
    border: 1px solid #555555;
}

QMenu::item:selected {
    background-color: #505050;
}
"""