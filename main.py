from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
import pickle


Form, Window = uic.loadUiType("tracker.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

date_param = 'dd-MM-yyyy'
data_file = 'config.txt'

def save_to_file_history():
    global start_date, calc_date, description
    data_to_save = {'start': start_date, 'end': calc_date, 'desc': description}
    history = open(data_file, 'wb')
    pickle.dump(data_to_save, history)
    history.close()
    pass

def read_from_file_history():
    global start_date, calc_date, description
    try:
        history = open(data_file, 'rb')
        data_to_load = pickle.load(history)
        history.close()
        start_date = data_to_load['start']
        calc_date = data_to_load['end']
        description = data_to_load['desc']
        start_date.toString(date_param), calc_date.toString(date_param), description
        form.calendarWidget.setSelectedDate(calc_date)
        form.dateEdit.setDate(calc_date)
        form.plainTextEdit.setPlainText(description)
        print('\n', start_date.toString(date_param), '\n', calc_date.toString(date_param), '\n', description)
    except:
        print('Файл не существует')


def on_click():
    global calc_date, description
    calc_date = form.calendarWidget.selectedDate()
    description = form.plainTextEdit.toPlainText()
    save_to_file_history()


def on_click_calendar():
    global start_date, calc_date
    form.dateEdit.setDate(form.calendarWidget.selectedDate())
    calc_date = form.calendarWidget.selectedDate()
    delta_days = start_date.daysTo(calc_date)
    form.label_2.setText("Дедлайн через : %s" % delta_days)

def on_dateedit_change():
    global start_date, calc_date
    form.calendarWidget.setSelectedDate(form.dateEdit.date())
    calc_date = form.dateEdit.date()
    delta_days = start_date.daysTo(calc_date)
    form.label_2.setText("Дедлайн через : %s" % delta_days)
    print('осталось ', delta_days, 'дней')

form.pushButton.clicked.connect(on_click)
form.calendarWidget.clicked.connect(on_click_calendar)
form.dateEdit.dateChanged.connect(on_dateedit_change)

start_date = form.calendarWidget.selectedDate()
calc_date = form.calendarWidget.selectedDate()
description = form.plainTextEdit.toPlainText()
read_from_file_history()

form.label.setText("Сегодня: %s" % start_date.toString(date_param))
on_click_calendar()

app.exec()
