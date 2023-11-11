"""
 _______       _            _     _          ______        _                 _ 
(_______)     (_)       _  (_)   | |        (____  \      (_)               | |
 _______  ____ _  ___ _| |_ _  __| |_____    ____)  ) ____ _ _____ ____   __| |
|  ___  |/ ___) |/___|_   _) |/ _  | ___ |  |  __  ( / ___) (____ |  _ \ / _  |
| |   | | |   | |___ | | |_| ( (_| | ____|  | |__)  ) |   | / ___ | | | ( (_| |
|_|   |_|_|   |_(___/   \__)_|\____|_____)  |______/|_|   |_\_____|_| |_|\____|
    
Auteur: daniel(mitchel.dmch@gmail.com) 
insertar.py(Ɔ) 2023
Description : Saisissez la description puis « Tab »
Créé le :  samedi 4 novembre 2023 à 16:15:10 
Dernière modification : samedi 4 novembre 2023 à 22:30:52
"""

import sys
import pymssql
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QLineEdit, QVBoxLayout, QWidget
import openpyxl

class ExcelToDatabaseApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Excel to Database App")
        self.setGeometry(100, 100, 800, 400)

        self.upload_button = QPushButton("Cargar Excel", self)
        self.upload_button.clicked.connect(self.uploadExcel)

        self.save_button = QPushButton("Guardar", self)
        self.save_button.clicked.connect(self.saveData)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.data_table = QTableWidget(self)
        self.data_table.setColumnCount(7)  # 5 para los datos Excel, 1 para "arancel", 1 para "tribunal"
        self.data_table.setHorizontalHeaderLabels(["numjui", "nombmandante", "nombdemandado", "domicilio", "rolcausa", "Arancel", "Tribunal"])
        layout.addWidget(self.data_table)

        layout.addWidget(self.upload_button)
        layout.addWidget(self.save_button)

        self.excel_data = None

    def uploadExcel(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Selecciona un archivo Excel", "", "Excel Files (*.xlsx);;All Files (*)")

        if file_name:
            # Leer datos del archivo Excel usando openpyxl
            workbook = openpyxl.load_workbook(file_name)
            sheet = workbook.active
            self.excel_data = [row for row in sheet.iter_rows(values_only=True)]

            self.data_table.setRowCount(len(self.excel_data))
            for row_idx, row in enumerate(self.excel_data):
                for col_idx, cell_value in enumerate(row):
                    item = QTableWidgetItem(str(cell_value))
                    self.data_table.setItem(row_idx, col_idx, item)
                    if col_idx == 5:  # Columna "Arancel"
                        arancel_input = QLineEdit()
                        self.data_table.setCellWidget(row_idx, 5, arancel_input)
                    if col_idx == 6:  # Columna "Tribunal"
                        tribunal_input = QLineEdit()
                        self.data_table.setCellWidget(row_idx, 6, tribunal_input)

    def saveData(self):
        if self.excel_data is None:
            return  # No hay datos de Excel cargados

        # Conectar a la base de datos SQL Server
        db_connection = pymssql.connect(
                server='vps-3697915-x.dattaweb.com',
                user='daniel',
                password='LOLxdsas--',
                database='micau5a'
        )
        cursor = db_connection.cursor()

        for row_idx in range(self.data_table.rowCount()):
            numjui = self.data_table.item(row_idx, 0).text()
            nombmandante = self.data_table.item(row_idx, 1).text()
            nombdemandado = self.data_table.item(row_idx, 2).text()
            domicilio = self.data_table.item(row_idx, 3).text()
            rolcausa = self.data_table.item(row_idx, 4).text()
            arancel_item = self.data_table.item(row_idx, 5)
        if arancel_item and isinstance(arancel_item, QLineEdit):
            arancel_text = arancel_item.text()
            try:
                arancel = float(arancel_text)
            except ValueError:
                arancel = 0  # Valor predeterminado si la conversión falla
        tribunal_item = self.data_table.item(row_idx, 6)
        tribunal = ""
        if tribunal_item:
            tribunal = tribunal_item.text()

        # Verificar si tribunal es nulo o vacío
        if not tribunal:
            tribunal = "Tribunal Desconocido"  # O utiliza otro valor predeterminado si es apropiado

        # Insertar datos de la demanda en la tabla "demanda"
        insert_query = "INSERT INTO demanda (numjui, nombmandante, nombdemandado, domicilio, rolcausa, nombTribunal,arancel) VALUES (%s, %s, %s, %s, %s, %s,%s)"
        cursor.execute(insert_query, (numjui, nombmandante, nombdemandado, domicilio, rolcausa, tribunal,arancel))


        

       
        db_connection.commit()
        db_connection.close()

        # Proporciona retroalimentación al usuario

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExcelToDatabaseApp()
    window.show()
    sys.exit(app.exec())
