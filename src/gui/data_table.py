import datetime
import logging
from typing import Optional, Union

from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg

from src.db.db import DB

from src.utils.setup_logging import setup_logger


logger = setup_logger('data_table', logging.DEBUG)


class TableView(qtw.QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.db = self.initialize_database()

        self.initialize_model()

        self.setupUI()


    def initialize_database(self):
        try:
            db = DB('src/config.ini', section='mysql')
        except Exception as e:
            self.handle_database_error(str(e))
            raise Exception("Database connection failed")

        return db

    def handle_database_error(self, error_message="Unknown database error"):
        qtw.QMessageBox.critical(
            self,
            "Database Error!",
            f"Database Error: {error_message}",
        )

    def initialize_model(self):
        self.data = self.db.select_all_data()
        logger.debug('model data loaded: %s', self.data[:10])
        self.column_names = self.db.get_column_names()

        model = self.setup_model()

        self.filter_proxy_model = qtc.QSortFilterProxyModel(self)
        self.filter_proxy_model.setSourceModel(model)
        self.filter_proxy_model.setFilterCaseSensitivity(qtc.Qt.CaseSensitivity.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(1)  # filter on the second column initially

        self.setModel(self.filter_proxy_model)

    def setup_model(self):
        model = qtg.QStandardItemModel()
        model.setHorizontalHeaderLabels(self.column_names)

        for i, row in enumerate(self.data):
            ### if we do not care of item types, but just want to stringify them:
            items = [qtg.QStandardItem(str(item)) for item in row]
            logger.debug('ROW: %s', row)

            ### handle diffrent item types
            # items = []
            # for field in row:
            #     item = qtg.QStandardItem()
            #     if isinstance(field, datetime.date):
            #         field = field.strftime('%d.%m.%Y')
            #     elif isinstance(field, str) and len(field)>100:
            #         # set full string with UserRole for later use:
            #         item.setData(field, qtc.Qt.ItemDataRole.UserRole)
            #         # trim string for display
            #         field = field[0:50]+'...'


            #     item.setData(field, qtc.Qt.ItemDataRole.DisplayRole)
            #     items.append(item)

            model.insertRow(i, items)

        return model


    def setupUI(self):
        ### set table dimensions:

        # self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        # self.setColumnWidth(3, 300)

        self.verticalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeMode.ResizeToContents);

        # enable columns sort
        self.setSortingEnabled(True)
        self.sortByColumn(0,qtc.Qt.SortOrder.AscendingOrder)

    @qtc.pyqtSlot(int)
    def set_filter_column(self,index):
        self.filter_proxy_model.setFilterKeyColumn(index)

    def get_last_updated_date(self) -> str:
        """Retrieve the last updated date from the database or the current date and time.

            Returns:
                str: A string representing the last updated date or the current date and time.
        """
        try:
            last_updated_date: Optional[str] = self.db.get_last_updated_date()
        except Exception:
            last_updated_date = None

        if last_updated_date is not None:
            return last_updated_date.strftime('%d.%m.%y, %H:%M:%S')
        else:
            return datetime.datetime.now().strftime('%d.%m.%y, %H:%M:%S')

class DataTable(qtw.QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent

        self.setup_gui()
        self.center_window()

    def setup_gui(self):
        # table view:
        self.tableView = TableView()
        tableViewWidth = self.tableView.frameGeometry().width()

        # label
        lblTitle = qtw.QLabel()
        label_msg = f'Countries crawled on {self.tableView.get_last_updated_date()}'
        lblTitle.setText(label_msg)
        lblTitle.setStyleSheet('''
            font-size: 30px;
        ''')
        lblTitle.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)

        # filter box layout:
        filterLabel = qtw.QLabel('Filter by column: ')

        filterLineEdit = qtw.QLineEdit()
        filterLineEdit.textChanged.connect(
            self.tableView.filter_proxy_model.setFilterRegularExpression
        )

        comboBox = qtw.QComboBox()
        comboBox.addItems(["{0}".format(col) for col in self.tableView.column_names])
        comboBox.setCurrentText('title')
        comboBox.currentIndexChanged.connect(
            lambda idx:self.tableView.set_filter_column(idx)
        )

        filterBoxLayout = qtw.QHBoxLayout()
        filterBoxLayout.addWidget(filterLabel)
        filterBoxLayout.addWidget(comboBox)
        filterBoxLayout.addWidget(filterLineEdit)

        # close button
        btnClose = qtw.QPushButton('Close')
        btnClose.clicked.connect(self.close_all)

        # main layout
        layout = qtw.QVBoxLayout()
        layout.addWidget(lblTitle)
        layout.addLayout(filterBoxLayout)
        layout.addWidget(self.tableView)
        layout.addWidget(btnClose)

        self.setLayout(layout)

        self.setFixedWidth(tableViewWidth)
        # self.setFixedHeight(tableViewHeight)

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
    def close_all(self):
        self.parent.close()
        self.close()

    @qtc.pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self,index):
        self.tableView.filter_proxy_model.setFilterKeyColumn(index)




