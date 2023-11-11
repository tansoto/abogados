import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QHBoxLayout
from PyQt6.QtGui import QColor
import pymssql
from verCausa import VerCausaApp
from buscado import BuscadorDatosCausaApp
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import Qt
class DashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dashboard App')
        self.setGeometry(100, 100, 1020, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout_vertical = QVBoxLayout()#crea un layout vertical
        self.layout_horizontal = QHBoxLayout()#crea un layout horizontal

   
#crea un boton para buscar
        self.btn_buscar = QPushButton('Buscar', self)
        self.btn_buscar.clicked.connect(self.buscar_clicked)
        self.layout_horizontal.addWidget(self.btn_buscar)
#crea un boton para insertar excel
        self.btn_Insertar_excel = QPushButton('Insertar Excel', self)
        self.btn_Insertar_excel.clicked.connect(self.Insertar_excel_clicked)
        self.layout_horizontal.addWidget(self.btn_Insertar_excel)
#crea un boton para insertar manual
        self.btn_Insertar_manual = QPushButton('Insertar Manual', self)
        self.btn_Insertar_manual.clicked.connect(self.Insertar_manual_clicked)
        self.layout_horizontal.addWidget(self.btn_Insertar_manual)
#anida los botones en el layout horizontal con el vertical
        self.layout_vertical.addLayout(self.layout_horizontal)
#creat una tabla
        self.table = QTableWidget()
        self.layout_vertical.addWidget(self.table)
#crea un boton para Guardar los datos de la tabla
        self.btn_Guardar = QPushButton('Guardar', self)
        self.btn_Guardar.clicked.connect(self.Guardar_clicked)
        self.layout_vertical.addWidget(self.btn_Guardar)
       # self.btn_Guardar.clicked.connect(self.Guardar_clicked)
        self.central_widget.setLayout(self.layout_vertical)

        # Llama automáticamente a acceder_base_de_datos y mostrar_clicked al iniciar la aplicación
        self.acceder_base_de_datos()
        self.mostrar_clicked()

        # Ajustar el tamaño de la ventana
        self.ajustar_tamanio()

    def Guardar_clicked(self):
   # Manejar la lógica cuando se hace clic en el botón de guardar
        for row_index, causa in enumerate(self.causas):
            # Obtener el estado del QCheckBox de "Busqueda positiva"
            checkbox_positiva = self.table.cellWidget(row_index, 9)
            causa["Busqueda positiva"] = "1" if checkbox_positiva.isChecked() else "0"

            # Obtener el estado del QCheckBox de "Busqueda negativa"
            checkbox_negativa = self.table.cellWidget(row_index, 10)
            causa["Busqueda negativa"] = "1" if checkbox_negativa.isChecked() else "0"

            # Actualizar estos cambios en la base de datos
            self.actualizar_base_de_datos(causa)
    def Insertar_excel_clicked(self):
        # Manejar la lógica cuando se hace clic en el botón de insertar excel
        import subprocess
        subprocess.Popen(['python', 'insertar.py'])
        
        pass
    def Insertar_manual_clicked(self):
        # Manejar la lógica cuando se hace clic en el botón de insertar manual
        import subprocess
        subprocess.Popen(['python', 'manualapajas.py'])
        pass
    def estampar_clicked(self):
        import subprocess
        subprocess.Popen(['python', 'estampar.py'])
        # Manejar la lógica cuando se hace clic en el botón de estampado
    
    def buscar_clicked(self):
        import subprocess
        subprocess.Popen(['python', 'buscado.py'])



    def verCausa_clicked(self):
        # Manejar la lógica cuando se hace clic en el botón de VerCausa
        button = self.sender()
        index = self.table.indexAt(button.pos())
        row, col = index.row(), index.column()
        # Obtener la causa correspondiente a la fila
        causa = self.causas[row]
        # Llama a la ventana VerCausa
        self.vercausa_app = VerCausaApp(causa)
        self.vercausa_app.show()

    def actualizar_base_de_datos(self, causa):
            # Conectar a la base de datos
            conn = pymssql.connect(
                server='vps-3697915-x.dattaweb.com',
                user='daniel',
                password='LOLxdsas--',
                database='micau5a'
            )

            # Crear un cursor
            cursor = conn.cursor()

            # Actualizar la base de datos con los nuevos valores de "Busqueda positiva" y "Busqueda negativa"
            query = f"UPDATE notificacion SET [Busqueda positiva] = '{causa['Busqueda positiva']}', " \
                    f"[Busqueda negativa] = '{causa['Busqueda negativa']}' WHERE rolCausa = '{causa['Rol Causa']}'"
            cursor.execute(query)

            # Confirmar y cerrar la conexión
            conn.commit()
            cursor.close()
            conn.close()
    def acceder_base_de_datos(self):
        # Conectar a la base de datos MySQL
        conn = pymssql.connect(
            server='vps-3697915-x.dattaweb.com',
            user='daniel',
            password='LOLxdsas--',
            database='micau5a'
        )

        # Crear un cursor
        cursor = conn.cursor()

        # Ejecutar una consulta SELECT
        


        """query = "insert into demanda (numjui,rolCausa,nombTribunal,nombmandante,domicilio,nombDemandado,arancel) values ('1','rol1','tribunal1','mandante1','domicilio1','demandado1','12000')"
        cursor.execute(query)
        query = "insert into demanda (numjui,rolCausa,nombTribunal,nombmandante,domicilio,nombDemandado,arancel) values ('2','rol2','tribunal2','mandante2','domicilio2','demandado2','14000')"
        cursor.execute(query)
        query = "insert into tribunal(numjui,nombTribunal) values ('1','tribunal1')"
        cursor.execute(query)
        query = "insert into tribunal(numjui,nombTribunal) values ('2','tribunal2')"
        cursor.execute(query)
        query ="insert into notificacion(fechaNotificacion,numjui,nombMandante,rolCausa,nombTribunal,estadoCausa) values ('2021-10-10','1','mandante1','rol1','tribunal1','1')"#1Pendiente (por ejemplo, 1): La causa ha sido notificada, pero aún no ha sido procesada o resuelta por el tribunal.
        cursor.execute(query)
        query ="insert into notificacion(fechaNotificacion,numjui,nombMandante,rolCausa,nombTribunal,estadoCausa) values ('2022-11-13','2','mandante2','rol2','tribunal2','2')"#2En Proceso (por ejemplo, 2): La causa ha sido notificada y está siendo procesada o resuelta por el tribunal.
        cursor.execute(query)"""


        query = "SELECT fechaNotificacion, numjui, nombmandante, rolCausa, nombTribunal, estadoCausa FROM notificacion"
        cursor.execute(query)
        # Obtener todos los resultados
        resultados = cursor.fetchall()

        

        # Cerrar el cursor y la conexión
        cursor.close()
        conn.commit() 
        conn.close()

        self.causas = []

        for fila in resultados:
            causa = {
                "Fecha notificacion": fila[0],
                "Numero juicio": fila[1],
                "Nombre Mandante": fila[2],
                "Rol Causa": fila[3],
                "Tribunal": fila[4],
                "Estado causa": fila[5],
                "Notificada": True,
                "Estampada": True,
                "VerCausa": "Ver Causa",
                "Busqueda positiva": "0",
                "Busqueda negativa": "0",
            }
            self.causas.append(causa)

    def mostrar_clicked(self):
        self.table.setColumnCount(11)  # Número de columnas
        self.table.setHorizontalHeaderLabels(['Fecha', 'Número juicio', 'Nombre mandante', 'Rol Causa', 'Tribunal', 'Estado causa','Notificada','Estampada', 'Ver Causa','Busqueda Positiva','Busqueda Negativa'])  # Etiquetas de las columnas

        for row_index, causa in enumerate(self.causas):
            self.table.insertRow(row_index)
            notificada = causa["Notificada"]
            estampada = causa["Estampada"]
            for col_index, (key, value) in enumerate(causa.items()):
                item = QTableWidgetItem(str(value))
                # Establecer un botón en la celda de estampado
                if key == "Estampada":
                    button = QPushButton("Estampar", self)
                    button.clicked.connect(self.estampar_clicked)
                    self.table.setCellWidget(row_index, col_index, button)
                # Establecer un botón en la celda de ver causa
                elif key == "VerCausa":
                    button = QPushButton("Ver Causa", self)
                    button.clicked.connect(self.verCausa_clicked)
                    self.table.setCellWidget(row_index, col_index, button)
                elif key == "Busqueda positiva":
                    checkbox = QCheckBox("Si", self)
                    if value == "1":
                        checkbox.setChecked(True)
                    else:
                        checkbox.setChecked(False)
                    self.table.setCellWidget(row_index, col_index, checkbox)
                elif key == "Busqueda negativa":
                    checkbox = QCheckBox("No", self)
                    if value == "1":
                        checkbox.setChecked(True)
                    else:
                        checkbox.setChecked(False)
                    self.table.setCellWidget(row_index, col_index, checkbox) 
                self.color_y_etiqueta_celda(item, estampada, notificada)
                self.table.setItem(row_index, col_index, item)

        # Mover estas líneas fuera del bucle para ajustar el tamaño después de agregar todas las filas
        

    def ajustar_tamanio(self):
        # Ajustar automáticamente el tamaño de las columnas
        self.table.resizeColumnsToContents()
        
        # Calcular el ancho total de las columnas
        total_width = sum(self.table.columnWidth(col) for col in range(self.table.columnCount()))
        
        # Establecer el ancho mínimo de la ventana para evitar achicarse demasiado
        min_width = max(self.width(), total_width)
        
        # Ajustar el tamaño de la ventana al tamaño máximo necesario
        self.setMinimumWidth(min_width)
        #self.resize(total_width, self.height())  # Opcional: Ajustar también el ancho actual de la ventana
        
        # Ajustar automáticamente el tamaño de la ventana
        #self.adjustSize()


    def color_y_etiqueta_celda(self, item, estampada, notificada):
        color = QColor()
        if estampada and notificada:
            color = QColor(0, 255, 0)  # Verde
        elif estampada and not notificada:
            color = QColor(255, 255, 0)  # Amarillo
        elif not estampada and notificada:
            color = QColor(0, 0, 255)  # Azul
        else:
            color = QColor(255, 0, 0)  # Rojo
        item.setBackground(color)

def main():
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
