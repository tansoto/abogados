
from msilib.schema import CheckBox
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QFileDialog, QLabel,QCheckBox
from docx import Document
from reportlab.pdfgen import canvas

class VerCausaApp(QMainWindow):
    def __init__(self, causa):
        super().__init__()
        self.setWindowTitle('Detalle de Causa')
        self.setGeometry(200, 200, 400, 200)

        self.causa = causa  # Guardar la causa

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Mostrar detalles de la causa
        self.label_causa = QLabel(f'Detalles de la Causa:\n{causa}', self)
        self.layout.addWidget(self.label_causa)

        # Checkbox para editar el estampado
        self.checkbox_estampado = QCheckBox('Estampada', self)
        self.checkbox_estampado.setChecked(self.causa["Estampada"])
        self.layout.addWidget(self.checkbox_estampado)

        # Botón para aplicar cambios
        self.btn_guardar = QPushButton('Guardar Cambios', self)
        self.btn_guardar.clicked.connect(self.guardar_cambios)
        self.layout.addWidget(self.btn_guardar)

        self.central_widget.setLayout(self.layout)

    def guardar_cambios(self):
        # Actualizar el estampado de la causa con el valor del checkbox
        self.causa["Estampada"] = self.checkbox_estampado.isChecked()

        # Puedes agregar aquí la lógica para guardar los cambios en la base de datos o en tu estructura de datos

        # Cerrar la ventana después de guardar cambios
        self.close()

# Ejemplo de uso:
if __name__ == '__main__':
    app = QApplication([])

    app.exec()

def main():
    app = QApplication(sys.argv)
    window = VerCausaApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
