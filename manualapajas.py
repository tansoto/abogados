"""
 _______       _            _     _          ______        _                 _ 
(_______)     (_)       _  (_)   | |        (____  \      (_)               | |
 _______  ____ _  ___ _| |_ _  __| |_____    ____)  ) ____ _ _____ ____   __| |
|  ___  |/ ___) |/___|_   _) |/ _  | ___ |  |  __  ( / ___) (____ |  _ \ / _  |
| |   | | |   | |___ | | |_| ( (_| | ____|  | |__)  ) |   | / ___ | | | ( (_| |
|_|   |_|_|   |_(___/   \__)_|\____|_____)  |______/|_|   |_\_____|_| |_|\____|
    
Auteur: daniel(mitchel.dmch@gmail.com) 
manualapajas.py(Ɔ) 2023
Description : Saisissez la description puis « Tab »
Créé le :  samedi 4 novembre 2023 à 17:40:55 
Dernière modification : samedi 4 novembre 2023 à 22:27:30
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QWidget, QMessageBox,QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit  # Agregado para importar QLineEdit

import pymssql

class MiApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ingreso de Datos")
        self.setGeometry(100, 100, 800, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QHBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["numjui", "nombmandante", "nombdemandado", "domicilio", "rolcausa", "nombTribunal", "arancel"])
        layout.addWidget(self.table)

        self.add_row_button = QPushButton("Agregar Fila")
        self.add_row_button.clicked.connect(self.add_row)
        layout.addWidget(self.add_row_button)

        self.delete_row_button = QPushButton("Eliminar Fila")
        self.delete_row_button.clicked.connect(self.delete_row)
        layout.addWidget(self.delete_row_button)

        self.save_button = QPushButton("Guardar Datos")
        self.save_button.clicked.connect(self.save_data)
        layout.addWidget(self.save_button)

        self.central_widget.setLayout(layout)
    def add_row(self):
        self.table.insertRow(self.table.rowCount())
        
    def delete_row(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.table.removeRow(selected_row)
        else:
            QMessageBox.information(self, "Información", "Selecciona una fila para eliminar.")


    def save_data(self):
        db_connection = pymssql.connect(
            server='vps-3697915-x.dattaweb.com',
            user='daniel',
            password='LOLxdsas--',
            database='micau5a')
        cursor = db_connection.cursor()

        for row_idx in range(self.table.rowCount()):
            numjui = self.table.item(row_idx, 0).text()
            nombmandante = self.table.item(row_idx, 1).text()
            nombdemandado = self.table.item(row_idx, 2).text()
            domicilio = self.table.item(row_idx, 3).text()
            rolcausa = self.table.item(row_idx, 4).text()

            arancel_item = self.table.cellWidget(row_idx, 5)  # Usar cellWidget para obtener el QLineEdit
            arancel_text = arancel_item.text() if isinstance(arancel_item, QLineEdit) else "0"
            try:
                arancel = float(arancel_text)
            except ValueError:
                arancel = 0  # Valor predeterminado si la conversión falla

            tribunal_item = self.table.cellWidget(row_idx, 6)  # Usar cellWidget para obtener el QLineEdit
            tribunal = tribunal_item.text() if isinstance(tribunal_item, QLineEdit) else "Tribunal Desconocido"

            if all([numjui, nombmandante, nombdemandado, domicilio, rolcausa]):
                insert_query = "INSERT INTO demanda (numjui, nombmandante, nombdemandado, domicilio, rolcausa, nombTribunal, arancel) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, (numjui, nombmandante, nombdemandado, domicilio, rolcausa, tribunal, arancel))
            else:
                QMessageBox.critical(self, "Error", "No se permiten celdas vacías en la fila {}".format(row_idx + 1))
                db_connection.rollback()
                break

        db_connection.commit()
        db_connection.close()

        self.clear_table()
        QMessageBox.information(self, "Éxito", "Datos guardados correctamente")

    def clear_table(self):
        self.table.setRowCount(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MiApp()
    window.show()
    sys.exit(app.exec())
