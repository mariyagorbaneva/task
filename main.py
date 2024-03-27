from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
import pickle


Form, Window = uic.loadUiType("tracker.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

# добавим клик по кнопке
def save_to_fale():
    global start_date, calc_date, description
    data_to_save = {'start': start_date, 'end': calc_date, 'desc': description}
    file1 = open('config.txt', 'wb')
    pickle.dump(data_to_save, file1)
    file1.close()
    pass

def read_from_file():
    global start_date, calc_date, description
    try:
        file1 = open('config.txt', 'rb')
        data_to_load = pickle.load(file1)
        file1.close()
        start_date = data_to_load['start']
        calc_date = data_to_load['end']
        description = data_to_load['desc']
        print(start_date.toString('dd-MM-yyyy'), calc_date.toString('dd-MM-yyyy'), description)
        form.calendarWidget.setSelectedDate(calc_date)
        form.dateEdit.setDate(calc_date)
        form.plainTextEdit.setPlainText(description)
    except:
        print('Файл не существует')


def on_click():
    global calc_date, description
    #print(form.plainTextEdit.toPlainText())
    #print(form.dateEdit.dateTime().toString('dd-MM-yyyy'))
    #print(form.calendarWidget.selectedDate().toString('dd-MM-yyyy'))
    calc_date = form.calendarWidget.selectedDate()
    description = form.plainTextEdit.toPlainText()
    print('Вывести')
    save_to_fale()
    # date = QDate(2024, 3, 3)
    # form.calendarWidget.setSelectedDate()

def on_click_calendar():
    global start_date, calc_date
    #form.calendarWidget.selectedDate().toString('dd-MM-yyyy')
    form.dateEdit.setDate(form.calendarWidget.selectedDate())
    calc_date = form.calendarWidget.selectedDate()
    delta_days = start_date.daysTo(calc_date)
    print(delta_days)
    form.label_2.setText("Дедлайн через : %s" % delta_days)

def on_dateedit_change():
    global start_date, calc_date
    #print(form.dateEdit.dateTime().toString('dd-MM-yyyy'))
    form.calendarWidget.setSelectedDate(form.dateEdit.date())
    calc_date = form.dateEdit.date()
    delta_days = start_date.daysTo(calc_date)
    print(delta_days)
    form.label_2.setText("Дедлайн через : %s" % delta_days)

form.pushButton.clicked.connect(on_click)
form.calendarWidget.clicked.connect(on_click_calendar)
form.dateEdit.dateChanged.connect(on_dateedit_change)

start_date = form.calendarWidget.selectedDate()
calc_date = form.calendarWidget.selectedDate()
description = form.plainTextEdit.toPlainText()
read_from_file()

form.label.setText("Сегодня: %s" % start_date.toString('dd-MM-yyyy'))
on_click_calendar()

app.exec()
