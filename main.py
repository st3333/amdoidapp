from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import phonenumbers
from phonenumbers import geocoder, carrier

class MyApp(App):
    def validate_phone(self, instance):
        phone_number = self.input_text.text
        try:
            parsed_number = phonenumbers.parse(phone_number)
            if phonenumbers.is_valid_number(parsed_number):
                country = geocoder.description_for_number(parsed_number, 'en')
                operator = carrier.name_for_number(parsed_number, 'en')
                result_text = f"Valid phone number\nCountry/City: {country}\nCarrier: {operator}"
                self.show_popup("Phone Number Validation", result_text)
            else:
                self.show_popup("Phone Number Validation", "Invalid phone number")
        except phonenumbers.phonenumberutil.NumberParseException:
            self.show_popup("Phone Number Validation", "Invalid phone number format")

    def show_popup(self, title, message):
        # Создаём BoxLayout для содержимого всплывающего окна
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        close_button = Button(text="Close", size_hint=(1, 0.3))
        content.add_widget(close_button)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(None, None),
            size=(400, 200),
            auto_dismiss=False  # Запретить закрытие окна по щелчку вне него
        )
        close_button.bind(on_press=popup.dismiss)  # Связать кнопку с закрытием окна
        popup.open()

    def build(self):
        layout = BoxLayout(padding=20, orientation='vertical')
        label = Label(text='Enter phone number:')
        layout.add_widget(label)
        self.input_text = TextInput(hint_text="e.g., +1234567890")  # Подсказка для ввода
        layout.add_widget(self.input_text)
        submit_button = Button(text='Submit', on_press=self.validate_phone)
        layout.add_widget(submit_button)
        return layout

if __name__ == '__main__':
    MyApp().run()
