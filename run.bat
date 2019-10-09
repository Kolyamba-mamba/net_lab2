pyuic5 ./mainwindow.ui -o ./mainwindow_ui.py
pyrcc5 -o mainwindow_rc.py mainwindow.qrc
python main.py