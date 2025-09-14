#Kivy Umgebung und dinge Installieren
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import csv
from datetime import datetime

#Klasse CoffeeTrackerApp definieren
## So erbt die App alle relevanten Funktionen der Standard Kivy-App
class CoffeTrackerApp(App):

    def build(self):

        main_layout = BoxLayout(orientation='vertical')
        self.info_label = Label(text='Wähle Kaffeesorte')
        espresso_button = Button(text='Espresso')
        Normal_button = Button(text='Normal')
        cappuccion_button = Button(text='Cappuccion')

        espresso_button.bind(on_press=self.kaffee_hinzufuegen)
        cappuccion_button.bind(on_press=self.kaffee_hinzufuegen)
        Normal_button.bind(on_press=self.kaffee_hinzufuegen)

        main_layout.add_widget(self.info_label)
        main_layout.add_widget(espresso_button)
        main_layout.add_widget(Normal_button)
        main_layout.add_widget(cappuccion_button)

        return main_layout

    def kaffee_hinzufuegen(self, instance):
        kaffee_sorte = instance.text
        self.info_label.text = f"Zuletst: {kaffee_sorte}"
        print(f"Ein {kaffee_sorte} wurde hinzugefügt")

        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open('cofeedata.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, kaffee_sorte])

if __name__ == '__main__':
    CoffeTrackerApp().run()


