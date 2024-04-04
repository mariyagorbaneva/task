import pickle

from PyQt6 import uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication

Form, Window = uic.loadUiType("tracker.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

date_param = 'dd-MM-yyyy'
data_file = 'config.txt'


class DateSet:
    __start_date: QDate
    __calc_date: QDate
    __description: str

    @staticmethod
    def get_data_set() -> tuple:
        return DateSet.__start_date, DateSet.__calc_date, DateSet.__description

    @staticmethod
    def set_data_set(start_date, calc_date, description):
        DateSet.__start_date = start_date
        DateSet.__calc_date = calc_date
        DateSet.__description = description


def save_to_file_history():
    # data_to_save = {'start': DateSet.get_data_set()[0],
    #                 'end': DateSet.get_data_set()[1],
    #                 'desc': DateSet.get_data_set()[2]
    #                 }
    data_to_save = {"start": DateSet.start_date,
                    'end': DateSet.calc_date,
                    'desc': DateSet.description}
    history = open(data_file, 'wb')
    pickle.dump(data_to_save, history)
    history.close()
    pass


def read_from_file_history():
    try:
        history = open(data_file, 'rb')
        data_to_load = pickle.load(history)
        history.close()
        DateSet.start_date_date = data_to_load['start']
        DateSet.calc_date = data_to_load['end']
        DateSet.description = data_to_load['desc']
        DateSet.start_date.toString(date_param), DateSet.calc_date.toString(date_param), DateSet.description
        form.calendarWidget.setSelectedDate(DateSet.calc_date)
        form.dateEdit.setDate(DateSet.calc_date)
        form.plainTextEdit.setPlainText(DateSet.description)
        print('\n', DateSet.calc_date.toString(date_param), '\n',
              DateSet.calc_date.toString(date_param), '\n', DateSet.description)
    except:
        print('Файл не существует')


def on_click():
    DateSet.calc_date = form.calendarWidget.selectedDate()
    DateSet.description = form.plainTextEdit.toPlainText()
    save_to_file_history()


def on_click_calendar():
    form.dateEdit.setDate(form.calendarWidget.selectedDate())
    DateSet.calc_date = form.calendarWidget.selectedDate()
    delta_days = DateSet.start_date.daysTo(DateSet.calc_date)
    form.label_2.setText("Дедлайн через : %s" % delta_days)


def on_data_edit_change():
    form.calendarWidget.setSelectedDate(form.dateEdit.date())
    DateSet.calc_date = form.dateEdit.date()
    delta_days = DateSet.start_date.daysTo(DateSet.calc_date)
    form.label_2.setText("Дедлайн через : %s" % delta_days)
    print('осталось ', delta_days, 'дней')


form.pushButton.clicked.connect(on_click)
form.calendarWidget.clicked.connect(on_click_calendar)
form.dateEdit.dateChanged.connect(on_data_edit_change)

DateSet.start_date = form.calendarWidget.selectedDate()
DateSet.calc_date = form.calendarWidget.selectedDate()
DateSet.description = form.plainTextEdit.toPlainText()
read_from_file_history()

form.label.setText("Сегодня: %s" % DateSet.start_date.toString(date_param))
on_click_calendar()

app.exec()
