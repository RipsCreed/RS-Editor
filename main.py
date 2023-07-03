from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import Qt
from lineNumber import LineNumberWidget
from PyQt5.QtWidgets import QWidget
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.text_area = QTextEdit()
        self.text_area.textChanged.connect(self.Line_Count_Changed)
        self.line_widget = LineNumberWidget(self.text_area)

        self.text_area_font = QFont()
        self.text_area_font.setPointSize(10)
        self.text_area_font.setWeight(50)

        self.text_area.setFont(self.text_area_font)

        hbox = QHBoxLayout()
        hbox.addWidget(self.line_widget)
        hbox.addWidget(self.text_area)

        self.setLayout(hbox)

    def Line_Count_Changed(self):
        if self.line_widget:
            number = int(self.text_area.document().lineCount())
            self.line_widget.changeLineCount(number)

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(1366, 768)
        self.setWindowTitle("RS Editor")

        self.main_window = MainWindow()
        self.setCentralWidget(self.main_window)

        #! StyleSheet

        self.setStyleSheet("background-color: cyan;")
        self.main_window.text_area.setStyleSheet("background-color: white; border: 1px solid")


        self.main_window.text_area.document().modificationChanged.connect(self.setWindowModified)

        self.m_bar = self.menuBar()

        self.m_bar.setStyleSheet("""
            QMenuBar {
                color: #363636;
            }
            QMenuBar::item:selected {
                background-color: cyan;
                border-top: none;
                border-left:none;
                border-bottom:none;
                border-left:2px solid #363636;;
            }""")

        self.menu_file = self.m_bar.addMenu("File")
        self.menu_view = self.m_bar.addMenu("View")
        
        action_open = QAction("Open File...", self)
        action_open.setShortcut("CTRL+O")

        action_save = QAction("Save File...", self)
        action_save.setShortcut("CTRL+S")

        action_save_as = QAction("Save As File...", self)
        action_save_as.setShortcut("CTRL+SHIFT+S")

        action_close = QAction("Close", self)
        action_close.setShortcut("CTRL+Q")

        self.action_change_theme = QAction("Dark Mode", self)


        self.menu_file.addAction(action_open)
        self.menu_file.addSeparator()
        self.menu_file.addAction(action_save)
        self.menu_file.addAction(action_save_as)
        self.menu_file.addSeparator()
        self.menu_file.addAction(action_close)

        self.menu_file.setStyleSheet("""
QMenu {
    background-color: cyan;
    border-top: none;
    border-left:none;
    border-right:none;
    border-bottom:4px solid  #363636;;
    color: #363636;;
}

QMenu::item {
    spacing: 3px; /* spacing between menu bar items */
    padding: 10px 85px 10px 20px;
    background: transparent;
}
QMenu::item:selected {
    background-color: cyan;
    border-top: none;
    border-left:none;
    border-bottom:none;
    border-left:3px solid  #363636;;
}""")

        self.menu_view.addAction(self.action_change_theme)
        self.menu_view.setStyleSheet("""
            QMenu {
    background-color: cyan;
    border-top: none;
    border-left:none;
    border-right:none;
    border-bottom:4px solid  #363636;;
    color: #363636;;
}

QMenu::item {
    spacing: 3px; /* spacing between menu bar items */
    padding: 10px 85px 10px 20px;
    background: transparent;
}
QMenu::item:selected {
    background-color: cyan;
    border-top: none;
    border-left:none;
    border-bottom:none;
    border-left:3px solid  #363636;;
}""")

        action_open.triggered.connect(self.Open_File)
        action_save.triggered.connect(self.Save_File)
        action_save_as.triggered.connect(self.Save_As_File)
        self.action_change_theme.triggered.connect(self.Change_Theme)

    def Open_File(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File", os.getenv("HOME"), "Python Files (*.py)")

        if file_name[0] != "" and file_name[1] != "":
            with open(file_name[0], "r") as file:
                self.main_window.text_area.setPlainText(file.read())

    def Save_File(self):
        if not self.isWindowModified():
            return
        if not self.file_name:
            self.saveAs()
        else:
            with open(self.file_name, 'w') as f:
                f.write(self.main_window.text_area.toPlainText())

    def Save_As_File(self):
        if not self.isWindowModified():
            return
        file_name, _ = QFileDialog.getSaveFileName(self, 
            "Save File", os.getenv("HOME"), "Python Files (*.py)")
        if file_name:
            with open(file_name, 'w') as f:
                f.write(self.main_window.text_area.toPlainText())
            self.file_name = file_name

    def Change_Theme(self):
        if self.action_change_theme.text() == "Dark Mode":
            self.setStyleSheet("background-color: #363636;")
            self.main_window.text_area.setStyleSheet("background-color: #4f4f4f; color: #dddddd;")
            self.m_bar.setStyleSheet("""
            QMenuBar {
                color: #dddddd;
            }
            QMenuBar::item:selected {
                background-color: #363636;
                border-top: none;
                border-left:none;
                border-bottom:none;
                border-left:2px solid  #dddddd;;
            }""")
            self.menu_file.setStyleSheet("""
            QMenu {
    background-color:#363636;
    border-top: none;
    border-left:none;
    border-right:none;
    border-bottom:4px solid  #dddddd;;
    color: #fff;;
}

QMenu::item {
    spacing: 3px; /* spacing between menu bar items */
    padding: 10px 85px 10px 20px;
    background: transparent;
}
QMenu::item:selected {
    background-color: #363636;
    border-top: none;
    border-left:none;
    border-bottom:none;
    border-left:3px solid  #dddddd;;
}""")
            self.menu_view.setStyleSheet("""
            QMenu {
    background-color:#363636;
    border-top: none;
    border-left:none;
    border-right:none;
    border-bottom:4px solid  #dddddd;;
    color:#dddddd;;
}

QMenu::item {
    spacing: 3px; /* spacing between menu bar items */
    padding: 10px 85px 10px 20px;
    background: transparent;
}
QMenu::item:selected {
    background-color: #363636;
    border-top: none;
    border-left:none;
    border-bottom:none;
    border-left:3px solid  #dddddd;;
}""")
            self.action_change_theme.setText("Light Mode")




        elif self.action_change_theme.text() == "Light Mode":
            self.setStyleSheet("background-color: cyan;")
            self.main_window.text_area.setStyleSheet("background-color: white; color: black;")
            self.m_bar.setStyleSheet("""
            QMenuBar {
                color: #363636;
            }
            QMenuBar::item:selected {
                background-color: cyan;
                border-top: none;
                border-left:none;
                border-bottom:none;
                border-left:2px solid #363636;;
            }""")

            self.menu_file.setStyleSheet("""
QMenu {
    background-color: cyan;
    border-top: none;
    border-left:none;
    border-right:none;
    border-bottom:4px solid  #363636;;
    color: #363636;;
}

QMenu::item {
    spacing: 3px; /* spacing between menu bar items */
    padding: 10px 85px 10px 20px;
    background: transparent;
}
QMenu::item:selected {
    background-color: cyan;
    border-top: none;
    border-left:none;
    border-bottom:none;
    border-left:3px solid  #363636;;
}""")
            
            self.menu_view.setStyleSheet("""
            QMenu {
    background-color: cyan;
    border-top: none;
    border-left:none;
    border-right:none;
    border-bottom:4px solid  #363636;;
    color:#363636;;
    border-radius: 1.5px;
}

QMenu::item {
    spacing: 3px; /* spacing between menu bar items */
    padding: 10px 85px 10px 20px;
    background: transparent;
}
QMenu::item:selected {
    background-color: cyan;
    border-top: none;
    border-left:none;
    border-bottom:none;
    border-left:3px solid  #363636;;
}""")
            self.action_change_theme.setText("Dark Mode")

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = Menu()
    w.show()
    app.exec()