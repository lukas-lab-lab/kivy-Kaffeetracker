#Kivy Umgebung und dinge Installieren
from cProfile import label
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import csv
from datetime import datetime


## Main Screen
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = BoxLayout(orientation='vertical')
        self.info_label = Label(text='Wähle Kaffeesorte')

        espresso_button = Button(text='Espresso')
        normal_button = Button(text='Normal')
        cappucino_button = Button(text='Cappucino')
        status_button = Button(text='Statistik')

        espresso_button.bind(on_press = self.kaffee_hinzufuegen)
        normal_button.bind(on_press = self.kaffee_hinzufuegen)
        cappucino_button.bind(on_press = self.kaffee_hinzufuegen)
        status_button.bind(on_press = self.switch_to_stats)

        main_layout.add_widget(self.info_label)
        main_layout.add_widget(espresso_button)
        main_layout.add_widget(normal_button)
        main_layout.add_widget(cappucino_button)
        main_layout.add_widget(status_button)

        self.add_widget(main_layout)

    def kaffee_hinzufuegen(self, instance):
        kaffee_sorte = instance.text
        self.info_label.text = f"{kaffee_sorte}"

        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open('cofeedata.csv', mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, kaffee_sorte])

    def switch_to_stats(self, instance):
        self.manager.current = 'stats'

## Screen 2 mit Statistiken
class StatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        stats_layout = BoxLayout(orientation='vertical')
        self.stats_label = Label(text='Kaffee Statistik')

        back_button = Button(text='Zurück')
        back_button.bind(on_press = self.switch_to_main)

        stats_layout.add_widget(self.stats_label)
        stats_layout.add_widget(back_button)
        self.add_widget(stats_layout)

    def on_enter(self):
        self.calculate_stats()

    def calculate_stats(self):
        today = datetime.now().date()
        coffees_today = 0
        total_coffees = 0
        total_espressos = 0
        total_cappucinos = 0
        total_normal = 0

        try:
            with open('cofeedata.csv', mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    total_coffees += 1

                    kaffee_sorte_in_zeile = row[1]
                    if kaffee_sorte_in_zeile == 'Espresso':
                        total_espressos += 1
                    elif kaffee_sorte_in_zeile == 'Normal':
                        total_normal += 1
                    elif kaffee_sorte_in_zeile == 'Cappucino':
                        total_cappucinos += 1

                    entry_date = datetime.strptime(row[0], '%d/%m/%Y %H:%M:%S').date()
                    if entry_date == today:
                        coffees_today += 1

            self.stats_label.text = f"Kaffee heute: {coffees_today} \nGesamt: {total_coffees} \nEspresso gesamt: {total_espressos} \nCappucino gesamt: {total_cappucinos} \nNormale Kaffee gesamt:  {total_normal} \n\n "
        except FileNotFoundError:
            self.stats_label.text = "Keine Daten"

    def switch_to_main(self, instance):
        self.manager.current = 'main'


## Screen Manager
class CoffeeTrackerApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(StatsScreen(name='stats'))
        return sm

if __name__ == '__main__':
    CoffeeTrackerApp().run()