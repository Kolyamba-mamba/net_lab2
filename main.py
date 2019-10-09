import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainWindow()
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
