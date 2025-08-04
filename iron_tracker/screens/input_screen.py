from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivy.metrics import dp
from datetime import datetime, date
import re


class InputScreen(MDScreen):
    """Screen for inputting new iron level readings."""
    
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.db_manager = db_manager
        self.selected_date = date.today()
        self.selected_time = datetime.now().strftime("%H:%M")
        self.build_ui()
    
    def build_ui(self):
        """Build the user interface for the input screen."""
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15),
            adaptive_height=True
        )
        
        # Title
        title = MDLabel(
            text="Add Iron Level Reading",
            theme_text_color="Primary",
            font_style="H4",
            halign="center",
            size_hint_y=None,
            height=dp(60)
        )
        
        # Main input card
        input_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15),
            elevation=2,
            radius=[10],
            size_hint_y=None,
            height=dp(450)
        )
        
        # Iron level input
        self.iron_level_field = MDTextField(
            hint_text="Enter iron level (μg/dL)",
            helper_text="Normal range: 60-170 μg/dL for adults",
            helper_text_mode="persistent",
            input_filter="float",
            required=True,
            mode="outlined"
        )
        
        # Date and time selection
        date_time_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(56)
        )
        
        self.date_field = MDTextField(
            hint_text="Date",
            text=self.selected_date.strftime("%Y-%m-%d"),
            readonly=True,
            mode="outlined",
            size_hint_x=0.6
        )
        
        date_button = MDIconButton(
            icon="calendar",
            on_release=self.open_date_picker,
            size_hint_x=0.2
        )
        
        self.time_field = MDTextField(
            hint_text="Time",
            text=self.selected_time,
            readonly=True,
            mode="outlined",
            size_hint_x=0.6
        )
        
        time_button = MDIconButton(
            icon="clock",
            on_release=self.open_time_picker,
            size_hint_x=0.2
        )
        
        date_time_layout.add_widget(self.date_field)
        date_time_layout.add_widget(date_button)
        date_time_layout.add_widget(self.time_field)
        date_time_layout.add_widget(time_button)
        
        # Test type selection
        self.test_type_field = MDTextField(
            hint_text="Test Type",
            text="Serum Iron",
            readonly=True,
            mode="outlined",
            on_focus=self.open_test_type_menu
        )
        
        # Notes field
        self.notes_field = MDTextField(
            hint_text="Notes (optional)",
            helper_text="Any additional information about this reading",
            helper_text_mode="persistent",
            multiline=True,
            max_height=dp(100),
            mode="outlined"
        )
        
        # Save button
        save_button = MDRaisedButton(
            text="Save Reading",
            size_hint_y=None,
            height=dp(50),
            on_release=self.save_reading,
            md_bg_color=self.theme_cls.primary_color
        )
        
        # Add widgets to card
        input_card.add_widget(self.iron_level_field)
        input_card.add_widget(date_time_layout)
        input_card.add_widget(self.test_type_field)
        input_card.add_widget(self.notes_field)
        input_card.add_widget(save_button)
        
        # Recent readings card
        recent_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            elevation=1,
            radius=[10],
            size_hint_y=None,
            height=dp(150)
        )
        
        recent_title = MDLabel(
            text="Recent Readings",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        )
        
        self.recent_readings_label = MDLabel(
            text="Loading recent readings...",
            theme_text_color="Secondary",
            font_style="Body2",
            text_size=(None, None),
            valign="top"
        )
        
        recent_card.add_widget(recent_title)
        recent_card.add_widget(self.recent_readings_label)
        
        # Add all widgets to main layout
        main_layout.add_widget(title)
        main_layout.add_widget(input_card)
        main_layout.add_widget(recent_card)
        
        self.add_widget(main_layout)
        
        # Initialize test type menu
        self.init_test_type_menu()
        
        # Load recent readings
        self.load_recent_readings()
    
    def init_test_type_menu(self):
        """Initialize the test type dropdown menu."""
        test_types = [
            "Serum Iron",
            "Transferrin Saturation",
            "Ferritin",
            "TIBC (Total Iron Binding Capacity)",
            "UIBC (Unsaturated Iron Binding Capacity)"
        ]
        
        menu_items = []
        for test_type in test_types:
            menu_items.append({
                "text": test_type,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=test_type: self.set_test_type(x),
            })
        
        self.test_type_menu = MDDropdownMenu(
            caller=self.test_type_field,
            items=menu_items,
            width_mult=4,
        )
    
    def open_test_type_menu(self, instance):
        """Open the test type selection menu."""
        self.test_type_menu.open()
    
    def set_test_type(self, test_type):
        """Set the selected test type."""
        self.test_type_field.text = test_type
        self.test_type_menu.dismiss()
    
    def open_date_picker(self, instance):
        """Open date picker dialog."""
        date_dialog = MDDatePicker(
            year=self.selected_date.year,
            month=self.selected_date.month,
            day=self.selected_date.day
        )
        date_dialog.bind(on_save=self.get_date)
        date_dialog.open()
    
    def get_date(self, instance, value, date_range):
        """Handle date selection."""
        self.selected_date = value
        self.date_field.text = value.strftime("%Y-%m-%d")
    
    def open_time_picker(self, instance):
        """Open time picker dialog."""
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()
    
    def get_time(self, instance, time):
        """Handle time selection."""
        self.selected_time = time.strftime("%H:%M")
        self.time_field.text = self.selected_time
    
    def save_reading(self, instance):
        """Save the iron level reading to database."""
        # Validate input
        if not self.iron_level_field.text.strip():
            self.show_snackbar("Please enter an iron level value")
            return
        
        try:
            iron_level = float(self.iron_level_field.text.strip())
            if iron_level <= 0:
                self.show_snackbar("Iron level must be a positive number")
                return
        except ValueError:
            self.show_snackbar("Please enter a valid numeric iron level")
            return
        
        # Save to database
        success = self.db_manager.add_reading(
            iron_level=iron_level,
            reading_date=self.selected_date,
            reading_time=self.selected_time,
            notes=self.notes_field.text.strip(),
            test_type=self.test_type_field.text
        )
        
        if success:
            self.show_snackbar("Reading saved successfully!")
            self.clear_form()
            self.load_recent_readings()
        else:
            self.show_snackbar("Error saving reading. Please try again.")
    
    def clear_form(self):
        """Clear the input form."""
        self.iron_level_field.text = ""
        self.notes_field.text = ""
        self.selected_date = date.today()
        self.selected_time = datetime.now().strftime("%H:%M")
        self.date_field.text = self.selected_date.strftime("%Y-%m-%d")
        self.time_field.text = self.selected_time
        self.test_type_field.text = "Serum Iron"
    
    def load_recent_readings(self):
        """Load and display recent readings."""
        try:
            recent_readings = self.db_manager.get_recent_readings(3)
            if recent_readings:
                readings_text = ""
                for reading in recent_readings:
                    date_str = reading['reading_date']
                    level = reading['iron_level']
                    readings_text += f"• {date_str}: {level} μg/dL\n"
                self.recent_readings_label.text = readings_text.strip()
            else:
                self.recent_readings_label.text = "No recent readings found"
        except Exception as e:
            self.recent_readings_label.text = "Error loading recent readings"
            print(f"Error loading recent readings: {e}")
    
    def show_snackbar(self, message):
        """Show a snackbar with the given message."""
        snackbar = Snackbar(text=message, duration=3)
        snackbar.open()