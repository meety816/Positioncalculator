# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.properties import ObjectProperty

class PositionCalculator(BoxLayout):
    entry_price_input = ObjectProperty(None)
    stop_loss_input = ObjectProperty(None)
    position_type_spinner = ObjectProperty(None)
    results_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        
        # Title
        self.add_widget(Label(
            text='Position Target Calculator',
            size_hint_y=None,
            height=50,
            font_size='20sp'
        ))
        
        # Position Type Spinner
        self.position_type_spinner = Spinner(
            text='long',
            values=('long', 'short'),
            size_hint_y=None,
            height=44
        )
        self.add_widget(self.position_type_spinner)
        
        # Entry Price Input
        self.add_widget(Label(text='Entry Price:', size_hint_y=None, height=30))
        self.entry_price_input = TextInput(
            multiline=False,
            input_filter='float',
            size_hint_y=None,
            height=44
        )
        self.add_widget(self.entry_price_input)
        
        # Stop Loss Input
        self.add_widget(Label(text='Stop Loss:', size_hint_y=None, height=30))
        self.stop_loss_input = TextInput(
            multiline=False,
            input_filter='float',
            size_hint_y=None,
            height=44
        )
        self.add_widget(self.stop_loss_input)
        
        # Calculate Button
        self.add_widget(Button(
            text='Calculate Targets',
            size_hint_y=None,
            height=50,
            on_press=self.calculate_targets
        ))
        
        # Results Label
        self.results_label = Label(
            text='Results will appear here',
            size_hint_y=None,
            height=200,
            text_size=(Window.width - 40, None),
            halign='left',
            valign='top'
        )
        self.add_widget(self.results_label)

    def validate_inputs(self):
        try:
            entry_price = float(self.entry_price_input.text)
            stop_loss = float(self.stop_loss_input.text)
            position_type = self.position_type_spinner.text

            if position_type == 'long' and stop_loss >= entry_price:
                self.results_label.text = 'For long positions, stop loss must be below entry price'
                return None
            elif position_type == 'short' and stop_loss <= entry_price:
                self.results_label.text = 'For short positions, stop loss must be above entry price'
                return None

            return entry_price, stop_loss, position_type
        except ValueError:
            self.results_label.text = 'Please enter valid numbers'
            return None

    def calculate_targets(self, instance):
        validated = self.validate_inputs()
        if not validated:
            return

        entry_price, stop_loss, position_type = validated
        risk = abs(entry_price - stop_loss)
        
        if position_type == 'long':
            target_2r = entry_price + (risk * 2)
            target_3r = entry_price + (risk * 3)
            target_4r = entry_price + (risk * 4)
        else:
            target_2r = entry_price - (risk * 2)
            target_3r = entry_price - (risk * 3)
            target_4r = entry_price - (risk * 4)
        
        avg_price = (entry_price + stop_loss) / 2
        
        self.results_label.text = (
            f'Entry Price: {entry_price:.4f}\n'
            f'Stop Loss: {stop_loss:.4f}\n'
            f'Risk Amount: {risk:.4f}\n'
            f'Average Price: {avg_price:.4f}\n\n'
            f'Target (1:2): {target_2r:.4f}\n'
            f'Target (1:3): {target_3r:.4f}\n'
            f'Target (1:4): {target_4r:.4f}'
        )

class PositionCalculatorApp(App):
    def build(self):
        return PositionCalculator()

if __name__ == '__main__':
    PositionCalculatorApp().run()
