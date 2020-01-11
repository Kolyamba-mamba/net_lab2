@echo python -m PyQt5.uic.pyuic -x mainwindow.ui -o mainwindow_ui.py > log.txt
python -m PyQt5.uic.pyuic -x mainwindow.ui -o mainwindow_ui.py >> log.txt 2>>&1
@echo python main.py >> log.txt
python main.py >> log.txt 2>>&1