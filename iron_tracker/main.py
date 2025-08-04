from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.icon_definitions import md_icons
from kivy.clock import Clock
import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from screens.input_screen import InputScreen
from screens.history_screen import HistoryScreen
from screens.charts_screen import ChartsScreen
from screens.insights_screen import InsightsScreen
from database.db_manager import DatabaseManager


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_manager = DatabaseManager()
        
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.material_style = "M3"
        
        # Initialize database
        self.db_manager.init_db()
        
        # Create screen manager
        self.screen_manager = MDScreenManager()
        
        # Create main container
        main_layout = MDBoxLayout(orientation="vertical")
        
        # Add screens
        self.input_screen = InputScreen(name="input", db_manager=self.db_manager)
        self.history_screen = HistoryScreen(name="history", db_manager=self.db_manager)
        self.charts_screen = ChartsScreen(name="charts", db_manager=self.db_manager)
        self.insights_screen = InsightsScreen(name="insights", db_manager=self.db_manager)
        
        self.screen_manager.add_widget(self.input_screen)
        self.screen_manager.add_widget(self.history_screen)
        self.screen_manager.add_widget(self.charts_screen)
        self.screen_manager.add_widget(self.insights_screen)
        
        # Create navigation bar
        self.navigation_bar = MDNavigationBar(
            MDNavigationItem(
                icon="plus-circle",
                text="Add Reading",
                active=True,
            ),
            MDNavigationItem(
                icon="history",
                text="History",
            ),
            MDNavigationItem(
                icon="chart-line",
                text="Charts",
            ),
            MDNavigationItem(
                icon="lightbulb",
                text="Insights",
            ),
        )
        
        # Bind navigation
        self.navigation_bar.bind(on_item_switch=self.on_tab_switch)
        
        main_layout.add_widget(self.screen_manager)
        main_layout.add_widget(self.navigation_bar)
        
        return main_layout
    
    def on_tab_switch(self, instance_navigation_bar, instance_navigation_item, instance_navigation_item_icon, instance_navigation_item_text):
        """Handle navigation bar item switches."""
        text = instance_navigation_item_text.lower()
        
        if "add" in text or "reading" in text:
            self.screen_manager.current = "input"
        elif "history" in text:
            self.screen_manager.current = "history"
            self.history_screen.refresh_data()
        elif "charts" in text:
            self.screen_manager.current = "charts"
            self.charts_screen.refresh_charts()
        elif "insights" in text:
            self.screen_manager.current = "insights"
            self.insights_screen.refresh_insights()


if __name__ == "__main__":
    MainApp().run()