""" module gui_app.py """
import logging
import sys

from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg

from src.data_processing.data_processor import DataProcessor
from src.utils.config_loader import load_config
from src.utils.setup_logging import setup_logger

from src.gui.data_table import DataTable

logger = setup_logger('qui_app', logging.DEBUG)

class MainWindow(qtw.QMainWindow):
    def __init__(self , *args, **kwargs):
        super().__init__(*args, **kwargs)

        data_processing_config = load_config('./src/config.ini', 'data_processing')
        target_url = data_processing_config['target_url']

        self.data_processor = DataProcessor(target_url = target_url)
        self.data_table = None
        self.setupUI()

        # Connect signals:
        self.btnShowData.clicked.connect(self.show_data)
        self.btnCrawlerRun.clicked.connect( self.run_crawler )

        self.show()

    def setupUI(self):
        self.setWindowTitle('Countries Scraper')

        layout = qtw.QVBoxLayout()
        lblTableCaption = qtw.QLabel('Countries Data')
        lblTableCaption.setObjectName('lblTableCaption')
        lblTableCaption.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lblTableCaption)

        btnsLayout = qtw.QHBoxLayout()
        self.btnCrawlerRun = qtw.QPushButton('Run Crawler')
        self.btnShowData = qtw.QPushButton('Show Data')
        # self.btnShowData.setEnabled(False)

        btnsLayout.addWidget(self.btnCrawlerRun)
        btnsLayout.addWidget(self.btnShowData)
        layout.addLayout(btnsLayout)

        # add spacer or just fixed spacing
        layout.addSpacing(10)
        # layout.addSpacerItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding))

        # Create Main Window Central Widjet
        mainWidget = qtw.QWidget()
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)

        self.center_window()

    def center_window(self):
        # Set window size and center it on the screen
        window_width = 400
        window_height = 400
        primary_screen = qtg.QGuiApplication.primaryScreen()
        if primary_screen:
            available_geometry = primary_screen.availableGeometry()

        self.setGeometry(
            (available_geometry.width() - window_width) // 2,
            (available_geometry.height() - window_height) // 2,
            window_width,
            window_height
        )

    @qtc.pyqtSlot()
    def show_data(self):
        self.data_table = DataTable(parent=self)
        self.data_table.show()

    @qtc.pyqtSlot()
    def run_crawler(self):
        self.setCursor(qtc.Qt.CursorShape.WaitCursor)

        self.data_processor.run()

        self.setCursor(qtc.Qt.CursorShape.ArrowCursor)


class MainApp(qtw.QApplication):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.main_window = MainWindow()
        self.main_window.show()

if __name__ == '__main__':
    app = MainApp(sys.argv)
    sys.exit(app.exec())