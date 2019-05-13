from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog
from pprint import pprint
import ndb_layout as ui
import dbhandler
from postcode_processor import get_postcodes
#from logger import debug_log, level
import signal
import sys

class nasc_main(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)

        # TODO(jamie): Locate this radius search stuff in its own setup function
        self.ui.checkBox_radius.clicked.connect(self.handle_check_radius_click)
        self.ui.radioButton_5m.setChecked(True)
        self.ui.spinBox_radius.setMaximum(100)
        self.ui.spinBox_radius.setMinimum(10)
        self.is_radius_search = False
        self.ui.checkBox_radius.setChecked(True)

        self.dbhandler = dbhandler.DBHandler("database/fake.db")
        self.setup()

    def handle_check_radius_click(self):
        if self.ui.checkBox_radius.isChecked():
            self.ui.lineEdit_search.setPlaceholderText("Enter postcode")
            self.is_radius_search = True
        else:
            self.ui.lineEdit_search.setPlaceholderText(self.default_placeholder)
            self.is_radius_search = False

    def setup(self):
        self.display_headers = ["Member ID", "Primary Contact", "Company", "Primary Tel", "Secondary Tel", "Address", "Postcode", "Email", "Region", "County"]
        self.model = self.create_model()
        self.ui.tableView_search.setModel(self.model)

        # Handle buttons
        self.ui.pushButton_search.clicked.connect(self.process_query)
        self.ui.pushButton_import.clicked.connect(self.load_new_db_file)
        self.ui.lineEdit_search.returnPressed.connect(self.process_query)

        # Set default state
        if self.ui.checkBox_radius.isChecked():
            self.default_placeholder = "Enter your postcode"
        else:
            self.default_placeholder = "Enter your search string..."

        self.ui.lineEdit_search.setPlaceholderText(self.default_placeholder)

        # Set combo box to 'name' by default
        self.ui.comboBox_search.setCurrentIndex(1)
        #self.ui.check_dev.stateChanged.connect(self.check_toggle_state)
        #self.ui.tabWidget.setCurrentIndex(1)
        #self.ui.table_db.doubleClicked.connect(self.rowselector)
        #self.ui.table_db.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

    def create_model(self):
        #debug_log("CALLED CREATE MODEL", level.debug)
        model = QtGui.QStandardItemModel()
        headers = self.display_headers
        model.setColumnCount(len(headers))
        model.setHorizontalHeaderLabels(headers)
        return(model)

    def display_results(self, data):
        self.model.setRowCount(0)
        # This may contain: a List of a list of tuples
        # [ [ (rowdata) ]]
        # NOTE(jamie): data consists of a list of tuples, with tuples
        # containing column data
        for entries in data:
            row = []
            for element in entries:
                item = QtGui.QStandardItem(element)
                row.append(item)
            self.model.appendRow(row)
        self.ui.tableView_search.resizeColumnsToContents()

    def format_data(self, container):
        result = []
        for element in container:
            for each_row in element:
                name      = " ".join(each_row[1:3])
                remaining = each_row[3:]
                interim_row = [each_row[0],name]
                interim_row += remaining
                result.append(interim_row)
        return(result)

    def process_query(self):
        query_string = self.ui.lineEdit_search.text().upper()

        if self.ui.checkBox_radius.isChecked():
            if len(query_string) < 2:
                QtWidgets.QMessageBox.warning(self, 'Oops...', 'A partial postcode must contain at least three alphanumeric characters: e.g. "AB1"', \
                                           QMessageBox.Ok)
                return

            if self.ui.radioButton_5m.isChecked():
                radius_in_miles = 5
            elif self.ui.radioButton_10m.isChecked():
                radius_in_miles = 10
            elif self.ui.radioButton_25m.isChecked():
                radius_in_miles = 25
            elif self.ui.radioButton_custom.isChecked():
                radius_in_miles = self.ui.spinBox_radius.value()

            pc = get_postcodes(query_string, radius_in_miles)

            # TODO(jamie): check what is going on with postcodes!!!
            # TODO(jamie): check what is going on with postcodes!!!
            # TODO(jamie): check what is going on with postcodes!!!
            # TODO(jamie): check what is going on with postcodes!!!
            if pc == -1:
                QtWidgets.QMessageBox.warning(self, 'Oops...', 'Not a valid UK postcode', \
                                           QMessageBox.Ok)
                return

            pc_results = []

            for each_postcode in pc:
                 db_result = self.dbhandler.querydb([each_postcode], True)
                 if db_result:
                     pc_results.append(db_result)
                 else:
                     continue
            formatted = self.format_data(pc_results)
            self.display_results(formatted)
        else:
            # This can contain many strings
            split_query_string = query_string.split(" ")
            db_result = [self.dbhandler.querydb(split_query_string)]
            data = self.format_data(db_result)
            self.display_results(data)

    def load_new_db_file(self):
        sure = QtWidgets.QMessageBox.critical(self, 'Here be dragons!!!', "You're about to change the active database. Continue?", \
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if sure == QtWidgets.QMessageBox.Yes:

            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            new_db_filename, _ = QFileDialog.getOpenFileName(self, "Open Database", "database/","Database Files (*.db)", options=options);
            success = self.dbhandler.change_active_database(new_db_filename)

        else:
            print ("No")
            return

def main():
    app  = QtWidgets.QApplication(sys.argv)
    form = nasc_main()
    form.show()
    # NOTE(jamie): So we can ctrl-c out of the application from shell
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app.exec_()

if __name__ == '__main__':
    main()
