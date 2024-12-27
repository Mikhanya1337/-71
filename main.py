import requests
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from functools import partial
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime, timedelta
import sqlite3
import random

def show_notification(message, title="Уведомление"):
    content = BoxLayout(orientation='vertical', padding=10)
    content.add_widget(Label(text=message))
    close_button = Button(text="Закрыть")
    content.add_widget(close_button)

    popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 200))
    close_button.bind(on_press=popup.dismiss)

    popup.open()

# Экран авторизации
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        layout.add_widget(Label(text='СНИЛС'))
        self.snils_input = TextInput()
        layout.add_widget(self.snils_input)

        layout.add_widget(Label(text='Пароль'))
        self.password_input = TextInput(password=True)
        layout.add_widget(self.password_input)

        layout.add_widget(Button(
            text='',
            background_normal='images/login.png',
            size_hint=(None, None),
            width=980,  # Устанавливаем фиксированную ширину
            height=150,  # Устанавливаем фиксированную высоту
            on_press=self.login
        ))

        layout.add_widget(Button(
            text='',
            background_normal='images/register.png',
            size_hint=(None, None),
            width=980,  # Устанавливаем фиксированную ширину
            height=150,  # Устанавливаем фиксированную высоту
            on_press=self.go_to_register
        ))

        self.add_widget(layout)

    def login(self, instance):
        snils = self.snils_input.text
        password = self.password_input.text

        conn = sqlite3.connect('mfc_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM пользователи WHERE СНИЛС = ? AND пароль = ?', (snils, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.manager.current = 'main'
        else:
            show_notification('Неверный СНИЛС или пароль', 'Ошибка')

    def go_to_register(self, instance):
        self.manager.current = 'register'


# Экран регистрации
class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        layout.add_widget(Label(text='СНИЛС'))
        self.snils_input = TextInput()
        layout.add_widget(self.snils_input)

        layout.add_widget(Label(text='Фамилия'))
        self.last_name_input = TextInput()
        layout.add_widget(self.last_name_input)

        layout.add_widget(Label(text='Имя'))
        self.first_name_input = TextInput()
        layout.add_widget(self.first_name_input)

        layout.add_widget(Label(text='Отчество'))
        self.middle_name_input = TextInput()
        layout.add_widget(self.middle_name_input)

        layout.add_widget(Label(text='Пароль'))
        self.password_input = TextInput(password=True)
        layout.add_widget(self.password_input)

        layout.add_widget(Button(
            text='',
            background_normal='images/zaregister.png',
            size_hint=(None, None),
            width=980,  # Устанавливаем фиксированную ширину
            height=150,  # Устанавливаем фиксированную высоту
            on_press=self.register
        ))

        layout.add_widget(Button(
            text='',
            background_normal='images/back.png',
            size_hint=(None, None),
            width=980,  # Устанавливаем фиксированную ширину
            height=150,  # Устанавливаем фиксированную высоту
            on_press=self.go_back
        ))

        self.add_widget(layout)

    def register(self, instance):
        snils = self.snils_input.text
        last_name = self.last_name_input.text
        first_name = self.first_name_input.text
        middle_name = self.middle_name_input.text
        password = self.password_input.text

        conn = sqlite3.connect('mfc_app.db')
        cursor = conn.cursor()

        # Проверка, существует ли пользователь с таким СНИЛС
        cursor.execute('SELECT * FROM пользователи WHERE СНИЛС = ?', (snils,))
        if cursor.fetchone():
            show_notification('Пользователь с таким СНИЛС уже существует.', 'Ошибка')
        else:
            cursor.execute('INSERT INTO пользователи (СНИЛС, Фамилия, Имя, Отчество, пароль) VALUES (?, ?, ?, ?, ?)',
                           (snils, last_name, first_name, middle_name, password))
            conn.commit()
            show_notification('Пользователь успешно зарегистрирован.', 'Успех')
            self.manager.current = 'login'

        conn.close()

    def go_back(self, instance):
        self.manager.current = 'login'


# Обновим главный экран с кнопкой "Просмотр всех услуг"
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        layout.add_widget(Button(
            text='',
            background_normal='images/record.png',
            size_hint=(None, None),
            width=980,  # Устанавливаем фиксированную ширину
            height=150,  # Устанавливаем фиксированную высоту
            on_press=self.go_to_booking
        ))

        layout.add_widget(Button(
            text='',
            background_normal='images/ready_documents.png',
            size_hint=(None, None),
            width=980,  # Устанавливаем фиксированную ширину
            height=150,  # Устанавливаем фиксированную высоту
            on_press=self.go_to_status
        ))

        layout.add_widget(Button(
            text='',
            background_normal='images/technical_support.png',
            size_hint=(None, None),
            width=980,  # Устанавливаем фиксированную ширину
            height=150,  # Устанавливаем фиксированную высоту
            on_press=self.go_to_support
        ))

        # Добавляем кнопку для просмотра всех услуг
        layout.add_widget(Button(
            text='',
            background_normal='images/services.png',
            size_hint=(None, None),
            width=980,  # Устанавливаем фиксированную ширину
            height=150,  # Устанавливаем фиксированную высоту
            on_press=self.go_to_services
        ))

        layout.add_widget(Button(
            text='',
            background_normal='images/exit.png',
            size_hint=(None, None),
            width=980,  # Устанавливаем фиксированную ширину
            height=150,  # Устанавливаем фиксированную высоту
            on_press=self.logout
        ))

        self.add_widget(layout)

    def go_to_booking(self, instance):
        self.manager.current = 'booking'

    def go_to_status(self, instance):
        self.manager.current = 'status'

    def go_to_support(self, instance):
        self.manager.current = 'support'

    def go_to_services(self, instance):
        self.manager.current = 'services'

    def logout(self, instance):
        self.manager.current = 'login'


# Экран записи в МФЦ
class BookingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Выбор отделения
        layout.add_widget(Label(text='Выберите отделение'))
        self.branch_spinner = Spinner(values=self.get_branches())
        layout.add_widget(self.branch_spinner)

        # Выбор услуги
        layout.add_widget(Label(text='Выберите услугу'))
        self.service_spinner = Spinner(values=self.get_services())
        layout.add_widget(self.service_spinner)

        # Выбор даты
        layout.add_widget(Label(text='Выберите дату'))
        self.date_spinner = Spinner(values=self.get_available_dates())
        layout.add_widget(self.date_spinner)

        # Выбор времени
        layout.add_widget(Label(text='Выберите время'))
        self.time_spinner = Spinner(values=self.get_available_times())
        layout.add_widget(self.time_spinner)

        layout.add_widget(Button(
            text='',
            background_normal='images/recording.png',
            size_hint=(None, None),
            width=980,  # Устанавливаем фиксированную ширину
            height=150,  # Устанавливаем фиксированную высоту
            on_press=self.book
        ))

        layout.add_widget(Button(
            text='',
            background_normal='images/back.png',
            size_hint=(None, None),
            width=980,  # Устанавливаем фиксированную ширину
            height=150,  # Устанавливаем фиксированную высоту
            on_press=self.go_back
        ))

        self.add_widget(layout)

    def get_branches(self):
        # Получение отделений из БД
        conn = sqlite3.connect('mfc_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT Адрес FROM отделения')
        branches = [row[0] for row in cursor.fetchall()]
        conn.close()
        return branches

    def get_services(self):
        # Получение услуг из БД
        conn = sqlite3.connect('mfc_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT Название_услуги FROM услуги')
        services = [row[0] for row in cursor.fetchall()]
        conn.close()
        return services

    def get_available_dates(self):
        # Даты на 2 недели вперёд
        dates = [(datetime.now() + timedelta(days=i)).strftime('%d.%m.%Y') for i in range(14)]
        return dates

    def get_available_times(self):
        # Время от 08:00 до 20:00 с шагом в 1 час
        times = [f'{hour:02d}:00' for hour in range(8, 21)]
        return times

    def book(self, instance):
        branch = self.branch_spinner.text
        service = self.service_spinner.text
        date = self.date_spinner.text
        time = self.time_spinner.text

        conn = sqlite3.connect('mfc_app.db')
        cursor = conn.cursor()

        # Получение СНИЛС пользователя
        snils = self.manager.get_screen('login').snils_input.text
        cursor.execute('SELECT Фамилия, Имя, Отчество FROM пользователи WHERE СНИЛС = ?', (snils,))
        user = cursor.fetchone()
        if user:
            full_name = f'{user[0]} {user[1]} {user[2]}'
            ticket_number = f'К{random.randint(100, 999)}'

            # Проверка на существование записи с таким же СНИЛС, отделением, услугой, датой и временем
            cursor.execute(
                'SELECT * FROM записи WHERE СНИЛС = ? AND Отделение = ? AND Услуга = ? AND Дата = ? AND Время = ?',
                (snils, branch, service, date, time))
            existing_record = cursor.fetchone()

            if existing_record:
                show_notification(f"Ошибка: Вы уже записаны на услугу {service} в отделении {branch} на {date} {time}.",
                                  'Ошибка')
            else:
                cursor.execute(
                    'INSERT INTO записи (СНИЛС, Отделение, Услуга, Дата, Время, Талон) VALUES (?, ?, ?, ?, ?, ?)',
                    (snils, branch, service, date, time, ticket_number))
                conn.commit()
                show_notification(
                    f'Запись успешно создана: {full_name}, {branch}, {service}, {date} {time}, Талон: {ticket_number}',
                    'Успех')
        else:
            show_notification('Ошибка: Пользователь не найден.', 'Ошибка')

        conn.close()

    def go_back(self, instance):
        self.manager.current = 'main'

class ServicesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        conn = sqlite3.connect('mfc_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT Ведомство FROM услуги')
        branches = [row[0] for row in cursor.fetchall()]
        conn.close()

        self.branch_spinner = Spinner(
            text='Выберите ведомство',
            values=branches)
        self.branch_spinner.bind(text=self.update_services)  # Привязка события выбора к функции обновления
        layout.add_widget(self.branch_spinner)

        self.services_layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.services_layout)

        layout.add_widget(Button(
            text='',
            background_normal='images/back.png',
            size_hint=(None, None),
            width=980,  # Устанавливаем фиксированную ширину
            height=150,  # Устанавливаем фиксированную высоту
            on_press=self.go_back))

        self.add_widget(layout)

    def update_services(self, spinner, text):
        self.services_layout.clear_widgets()

        if text == 'Выберите ведомство':
            return

        # Используем правильное имя столбца
        conn = sqlite3.connect('mfc_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT Название_услуги FROM услуги WHERE Ведомство = ?', (text,))  # Проверьте имя столбца!
        services = cursor.fetchall()
        conn.close()

        if not services:
            self.services_layout.add_widget(Label(text='Нет доступных услуг для данного ведомства.'))
        else:
            for service in services:
                self.services_layout.add_widget(Label(text=service[0]))

    def go_back(self, instance):
        self.manager.current = 'main'


# Экран проверки статуса готовности документов
class DocumentStatusScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        layout.add_widget(Label(text='Введите номер документа:'))

        # Поле ввода номера документа
        self.document_number_input = TextInput()
        layout.add_widget(self.document_number_input)

        # Кнопка для проверки статуса
        layout.add_widget(Button(
            text='',
            background_normal='images/proverit.png',
            size_hint=(None, None),
            width=980,  # Устанавливаем фиксированную ширину
            height=150,  # Устанавливаем фиксированную высоту
            on_press=self.check_status
        ))

        # Кнопка для возврата на главный экран
        layout.add_widget(Button(
            text='',
            background_normal='images/back.png',
            size_hint=(None, None),
            width=980,  # Устанавливаем фиксированную ширину
            height=150,  # Устанавливаем фиксированную высоту
            on_press=self.go_back
        ))

        # Место для отображения статуса
        self.status_label = Label(text='')
        layout.add_widget(self.status_label)

        self.add_widget(layout)

    def check_status(self, instance):
        # Получаем номер документа из поля ввода
        document_number = self.document_number_input.text

        if not document_number:
            show_notification("Пожалуйста, введите номер документа.", "Ошибка")
            return

        # Запрос в базу данных для получения статуса по номеру документа
        conn = sqlite3.connect('mfc_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT Статус, Подача FROM готовность WHERE Номер_документа = ?', (document_number,))
        status = cursor.fetchone()
        conn.close()

        if status:
            self.status_label.text = f'Статус: {status[0]}, Подача: {status[1]}'
        else:
            self.status_label.text = 'Данные о готовности не найдены.'

    def go_back(self, instance):
        self.manager.current = 'main'


# Экран технической поддержки
class SupportScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        layout.add_widget(Label(text='Опишите проблему'))
        self.problem_input = TextInput()
        layout.add_widget(self.problem_input)

        layout.add_widget(Button(
            text='',
            background_normal='images/otpravit.png',
            size_hint=(None, None),
            width=980,  # Устанавливаем фиксированную ширину
            height=150,  # Устанавливаем фиксированную высоту
            on_press=self.send_message
        ))

        layout.add_widget(Button(
            text='',
            background_normal='images/back.png',
            size_hint=(None, None),
            width=980,  # Устанавливаем фиксированную ширину
            height=150,  # Устанавливаем фиксированную высоту
            on_press=self.go_back
        ))

        self.add_widget(layout)

    def send_message(self, instance):
        snils = self.manager.get_screen('login').snils_input.text
        message = self.problem_input.text

        conn = sqlite3.connect('mfc_app.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO поддержка (СНИЛС, Сообщение) VALUES (?, ?)', (snils, message))
        conn.commit()
        conn.close()

        show_notification('Сообщение отправлено. Обратная связь будет предоставлена в течение суток.', 'Успех')

    def go_back(self, instance):
        self.manager.current = 'main'


# Основной класс приложения
class MFCApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(BookingScreen(name='booking'))
        sm.add_widget(DocumentStatusScreen(name='status'))
        sm.add_widget(SupportScreen(name='support'))
        sm.add_widget(ServicesScreen(name='services'))
        return sm


if __name__ == '__main__':
    MFCApp().run()
