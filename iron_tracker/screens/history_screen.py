from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
from datetime import datetime, date, timedelta
import calendar


class HistoryScreen(MDScreen):
    """Screen for viewing historical iron level readings."""
    
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.db_manager = db_manager
        self.all_readings = []
        self.filtered_readings = []
        self.delete_dialog = None
        self.build_ui()
    
    def build_ui(self):
        """Build the user interface for the history screen."""
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )
        
        # Title and stats header
        header_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            elevation=2,
            radius=[10],
            size_hint_y=None,
            height=dp(120)
        )
        
        title = MDLabel(
            text="Reading History",
            theme_text_color="Primary",
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )
        
        self.stats_label = MDLabel(
            text="Loading statistics...",
            theme_text_color="Secondary",
            font_style="Body2",
            halign="center",
            size_hint_y=None,
            height=dp(60)
        )
        
        header_card.add_widget(title)
        header_card.add_widget(self.stats_label)
        
        # Search and filter section
        filter_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            elevation=1,
            radius=[10],
            size_hint_y=None,
            height=dp(120)
        )
        
        # Search field
        self.search_field = MDTextField(
            hint_text="Search readings...",
            mode="outlined",
            size_hint_y=None,
            height=dp(56),
            on_text=self.on_search_text_change
        )
        
        # Filter buttons
        filter_buttons_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40),
            adaptive_width=True
        )
        
        all_button = MDFlatButton(
            text="All",
            on_release=lambda x: self.filter_readings("all")
        )
        
        week_button = MDFlatButton(
            text="This Week",
            on_release=lambda x: self.filter_readings("week")
        )
        
        month_button = MDFlatButton(
            text="This Month",
            on_release=lambda x: self.filter_readings("month")
        )
        
        year_button = MDFlatButton(
            text="This Year",
            on_release=lambda x: self.filter_readings("year")
        )
        
        filter_buttons_layout.add_widget(all_button)
        filter_buttons_layout.add_widget(week_button)
        filter_buttons_layout.add_widget(month_button)
        filter_buttons_layout.add_widget(year_button)
        
        filter_card.add_widget(self.search_field)
        filter_card.add_widget(filter_buttons_layout)
        
        # Readings list
        self.readings_scroll = MDScrollView()
        self.readings_list = MDList()
        self.readings_scroll.add_widget(self.readings_list)
        
        # Add widgets to main layout
        main_layout.add_widget(header_card)
        main_layout.add_widget(filter_card)
        main_layout.add_widget(self.readings_scroll)
        
        self.add_widget(main_layout)
    
    def refresh_data(self):
        """Refresh the readings data and update the display."""
        self.load_readings()
        self.update_statistics()
        self.update_readings_list()
    
    def load_readings(self):
        """Load all readings from the database."""
        try:
            self.all_readings = self.db_manager.get_all_readings()
            self.filtered_readings = self.all_readings.copy()
        except Exception as e:
            print(f"Error loading readings: {e}")
            self.all_readings = []
            self.filtered_readings = []
    
    def update_statistics(self):
        """Update the statistics display."""
        try:
            if not self.all_readings:
                self.stats_label.text = "No readings found"
                return
            
            stats = self.db_manager.get_statistics()
            total = stats.get('total_readings', 0)
            avg = stats.get('average_level', 0)
            
            if avg:
                avg_text = f"{avg:.1f} μg/dL"
            else:
                avg_text = "N/A"
            
            normal_count = stats.get('normal_readings', 0)
            low_count = stats.get('low_readings', 0)
            high_count = stats.get('high_readings', 0)
            
            self.stats_label.text = (
                f"Total Readings: {total}  •  Average: {avg_text}\n"
                f"Normal: {normal_count}  •  Low: {low_count}  •  High: {high_count}"
            )
            
        except Exception as e:
            print(f"Error updating statistics: {e}")
            self.stats_label.text = "Error loading statistics"
    
    def update_readings_list(self):
        """Update the readings list display."""
        self.readings_list.clear_widgets()
        
        if not self.filtered_readings:
            no_data_label = MDLabel(
                text="No readings found",
                theme_text_color="Secondary",
                halign="center",
                size_hint_y=None,
                height=dp(100)
            )
            self.readings_list.add_widget(no_data_label)
            return
        
        # Get normal range for color coding
        profile = self.db_manager.get_user_profile()
        normal_min = profile.get('normal_range_min', 60)
        normal_max = profile.get('normal_range_max', 170)
        
        for reading in self.filtered_readings:
            # Determine color based on iron level
            iron_level = reading['iron_level']
            if iron_level < normal_min:
                icon_color = "red"
                status = "Low"
            elif iron_level > normal_max:
                icon_color = "orange"
                status = "High"
            else:
                icon_color = "green"
                status = "Normal"
            
            # Format the reading item
            primary_text = f"{iron_level} μg/dL - {status}"
            secondary_text = f"{reading['reading_date']} at {reading['reading_time']}"
            
            if reading.get('notes'):
                secondary_text += f" • {reading['notes'][:30]}..."
            
            list_item = TwoLineAvatarIconListItem(
                text=primary_text,
                secondary_text=secondary_text,
                IconLeftWidget(
                    icon="water",
                    theme_icon_color="Custom",
                    icon_color=icon_color
                ),
                IconRightWidget(
                    icon="delete",
                    theme_icon_color="Custom",
                    icon_color="red",
                    on_release=lambda x, reading_id=reading['id']: self.confirm_delete(reading_id)
                )
            )
            
            self.readings_list.add_widget(list_item)
    
    def on_search_text_change(self, instance, text):
        """Handle search text changes."""
        if not text.strip():
            self.filtered_readings = self.all_readings.copy()
        else:
            search_term = text.lower().strip()
            self.filtered_readings = []
            
            for reading in self.all_readings:
                # Search in multiple fields
                searchable_text = " ".join([
                    str(reading.get('iron_level', '')),
                    str(reading.get('reading_date', '')),
                    str(reading.get('notes', '')),
                    str(reading.get('test_type', ''))
                ]).lower()
                
                if search_term in searchable_text:
                    self.filtered_readings.append(reading)
        
        self.update_readings_list()
    
    def filter_readings(self, filter_type):
        """Filter readings by time period."""
        today = date.today()
        
        if filter_type == "all":
            self.filtered_readings = self.all_readings.copy()
        elif filter_type == "week":
            start_date = today - timedelta(days=7)
            self.filtered_readings = [
                reading for reading in self.all_readings
                if datetime.strptime(reading['reading_date'], '%Y-%m-%d').date() >= start_date
            ]
        elif filter_type == "month":
            start_date = today.replace(day=1)
            self.filtered_readings = [
                reading for reading in self.all_readings
                if datetime.strptime(reading['reading_date'], '%Y-%m-%d').date() >= start_date
            ]
        elif filter_type == "year":
            start_date = today.replace(month=1, day=1)
            self.filtered_readings = [
                reading for reading in self.all_readings
                if datetime.strptime(reading['reading_date'], '%Y-%m-%d').date() >= start_date
            ]
        
        self.update_readings_list()
    
    def confirm_delete(self, reading_id):
        """Show confirmation dialog for deleting a reading."""
        if not self.delete_dialog:
            self.delete_dialog = MDDialog(
                title="Delete Reading",
                text="Are you sure you want to delete this reading? This action cannot be undone.",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=self.close_delete_dialog
                    ),
                    MDFlatButton(
                        text="DELETE",
                        theme_text_color="Custom",
                        text_color="red",
                        on_release=lambda x: self.delete_reading(reading_id)
                    ),
                ],
            )
        else:
            # Update the dialog for the new reading ID
            self.delete_dialog.buttons[1].on_release = lambda x: self.delete_reading(reading_id)
        
        self.delete_dialog.open()
    
    def close_delete_dialog(self, instance):
        """Close the delete confirmation dialog."""
        if self.delete_dialog:
            self.delete_dialog.dismiss()
    
    def delete_reading(self, reading_id):
        """Delete the specified reading."""
        try:
            success = self.db_manager.delete_reading(reading_id)
            if success:
                self.show_snackbar("Reading deleted successfully")
                self.refresh_data()
            else:
                self.show_snackbar("Error deleting reading")
        except Exception as e:
            print(f"Error deleting reading: {e}")
            self.show_snackbar("Error deleting reading")
        finally:
            self.close_delete_dialog(None)
    
    def show_snackbar(self, message):
        """Show a snackbar with the given message."""
        snackbar = Snackbar(text=message, duration=3)
        snackbar.open()