import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog
import PyPDF2

class PdfSigner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Signer')
        self.setGeometry(100, 100, 400, 200)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()

        self.selectMainPdfButton = QPushButton('Seleccionar firma')
        self.selectMainPdfButton.clicked.connect(self.selectMainPdf)
        self.layout.addWidget(self.selectMainPdfButton)

        self.selectSignatureButton = QPushButton('Seleccionar documento a firmar')
        self.selectSignatureButton.clicked.connect(self.selectSignaturePdf)
        self.layout.addWidget(self.selectSignatureButton)

        self.signPdfButton = QPushButton('Firmar PDF')
        self.signPdfButton.clicked.connect(self.signPdf)
        self.layout.addWidget(self.signPdfButton)

        self.centralWidget.setLayout(self.layout)

        self.mainPdfPath = None
        self.signaturePdfPath = None

    def selectMainPdf(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Selecciona un archivo PDF", "", "PDF Files (*.pdf);;All Files (*)")
        if filePath:
            self.mainPdfPath = filePath

    def selectSignaturePdf(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Selecciona un archivo PDF para la firma", "", "PDF Files (*.pdf);;All Files (*)")
        if filePath:
            self.signaturePdfPath = filePath

    def signPdf(self):
        if self.mainPdfPath and self.signaturePdfPath:
            # Abrir el archivo PDF principal
            with open(self.mainPdfPath, 'rb') as mainPdfFile:
                mainPdfReader = PyPDF2.PdfFileReader(mainPdfFile)
                mainPdfWriter = PyPDF2.PdfFileWriter()

                # Agregar páginas del PDF principal al nuevo PDF
                for pageNum in range(mainPdfReader.numPages):
                    pageObj = mainPdfReader.getPage(pageNum)
                    mainPdfWriter.addPage(pageObj)

                # Abrir el archivo PDF de la firma
                with open(self.signaturePdfPath, 'rb') as signaturePdfFile:
                    signaturePdfReader = PyPDF2.PdfFileReader(signaturePdfFile)
                    signaturePage = signaturePdfReader.getPage(0)

                    # Agregar la firma al primer documento PDF
                    firstPage = mainPdfWriter.getPage(0)
                    firstPage.mergePage(signaturePage)

                # Guardar el PDF con la firma en un nuevo archivo
                outputFilePath, _ = QFileDialog.getSaveFileName(self, "Guardar PDF Firmado", "", "PDF Files (*.pdf);;All Files (*)")
                if outputFilePath:
                    with open(outputFilePath, 'wb') as outputPdfFile:
                        mainPdfWriter.write(outputPdfFile)

                    print(f'PDF firmado correctamente y guardado como {outputFilePath}')
        else:
            print('Por favor, selecciona un archivo PDF principal y un archivo PDF para la firma.')

def main():
    app = QApplication(sys.argv)
    window = PdfSigner()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
