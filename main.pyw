from gui import Ui_MainWindow
from sys import argv
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLineEdit
from steganography import Steganography

def pickButton(element:QLineEdit):
    options = QFileDialog.Options()
    options |= QFileDialog.Option.ReadOnly
    file_path, _ = QFileDialog.getOpenFileName(main_window, "Select Image",
                                               "",
                                               "Images (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.jfif)",
                                               options= options)
    if file_path:
        element.setText(file_path)
    else:
        element.setText("You should select an image!")

def setOutputPath():
    options = QFileDialog.Options()
    options |= QFileDialog.FileMode.DirectoryOnly
    folder_path = QFileDialog.getExistingDirectory(main_window, "Select Folder", options= options)
    if folder_path:
        ui.lineEdit_embed_opath.setText(folder_path)
    else:
        ui.lineEdit_embed_opath.setText("You should select an output path!")

def embedButton():
    try:
        img_name_ext = ui.lineEdit_embed_ipath.text().split("/")[-1].split(".")
        img_name_ext[0] += "_embeded"
        opath = ui.lineEdit_embed_opath.text() + "/" + img_name_ext[0] + "." + img_name_ext[1]
        success = Steganography.LSB.embed(
            ui.lineEdit_embed_ipath.text(),
            opath,
            ui.plainTextEdit_message.toPlainText(),
            ui.lineEdit_delimiter.text()
            )
        if success:
            ui.plainTextEdit_message.setPlainText("Successfuly embedded.")
        else:
            ui.plainTextEdit_message.setPlainText("Failed to embed.")
    except Exception as e:
        ui.plainTextEdit_message.setPlainText('EXCEPTION: ' + str(e))

def dislodgeButton():
    try:
        ui.plainTextEdit_message.setPlainText(Steganography.LSB.dislodge(
            ipath= ui.lineEdit_dislodge_ipath.text(),
            delimiter= ui.lineEdit_delimiter.text(),
            read_all= ui.radioButton_read_all.isChecked()
            )
        )
    except Exception as e:
        ui.plainTextEdit_message.setPlainText('EXCEPTION: ' + str(e))

if __name__ == "__main__":
    app = QApplication(argv)
    main_window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    main_window.setWindowTitle("Steganography - UI")

    ui.tabWidget.currentChanged.connect(lambda: ui.plainTextEdit_message.clear())
    ui.lineEdit_delimiter.setText('\\end_of_message\\')
    ui.pushButton_embed_pick.clicked.connect(lambda: pickButton(ui.lineEdit_embed_ipath))
    ui.pushButton_embed_set_output.clicked.connect(setOutputPath)
    ui.pushButton_embed.clicked.connect(embedButton)
    ui.pushButton_dislodge_pick.clicked.connect(lambda: pickButton(ui.lineEdit_dislodge_ipath))
    ui.pushButton_dislodge.clicked.connect(dislodgeButton)

    main_window.show()
    app.exec_()