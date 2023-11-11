"""
 _______       _            _     _          ______        _                 _ 
(_______)     (_)       _  (_)   | |        (____  \      (_)               | |
 _______  ____ _  ___ _| |_ _  __| |_____    ____)  ) ____ _ _____ ____   __| |
|  ___  |/ ___) |/___|_   _) |/ _  | ___ |  |  __  ( / ___) (____ |  _ \ / _  |
| |   | | |   | |___ | | |_| ( (_| | ____|  | |__)  ) |   | / ___ | | | ( (_| |
|_|   |_|_|   |_(___/   \__)_|\____|_____)  |______/|_|   |_\_____|_| |_|\____|
    
Auteur: danie(danie.pro@gmail.com) 
coneccion2.py(Ɔ) 2023
Description : Saisissez la description puis « Tab »
Créé le :  samedi 28 octobre 2023 à 18:13:56 
Dernière modification : samedi 28 octobre 2023 à 18:14:40
"""

import sys
import pymssql
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

class DatabaseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initDatabaseConnection()

    def initUI(self):
        self.setWindowTitle('Aplicación de Base de Datos SQL Server')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.status_label = QLabel('', self)
        layout.addWidget(self.status_label)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def initDatabaseConnection(self):
        try:
            # Configura la cadena de conexión a tu base de datos SQL Server en la nube
            connection = pymssql.connect(
                server='vps-3697915-x.dattaweb.com',
                user='daniel',
                password='LOLxdsas--',
                database='micau5a'
            )

            cursor = connection.cursor()
            cursor.execute('SELECT @@version')
            row = cursor.fetchone()
            self.status_label.setText(f'Conexión exitosa a la base de datos en la nube (SQL Server): {row[0]}')

            # Aquí puedes realizar operaciones en la base de datos según tus necesidades

            connection.close()
        except pymssql.DatabaseError as e:
            self.status_label.setText(f'Error de conexión a la base de datos en la nube: {str(e)}')

def main():
    app = QApplication(sys.argv)
    window = DatabaseApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
