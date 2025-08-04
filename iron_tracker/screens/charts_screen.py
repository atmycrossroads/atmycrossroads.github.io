from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.metrics import dp
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, date, timedelta
import numpy as np


class ChartsScreen(MDScreen):
    """Screen for displaying iron level charts and trends."""
    
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.db_manager = db_manager
        self.current_chart = "trend"
        self.build_ui()
    
    def build_ui(self):
        """Build the user interface for the charts screen."""
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )
        
        # Title and chart selection
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
            text="Iron Level Charts",
            theme_text_color="Primary",
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )
        
        # Chart type buttons
        button_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40),
            adaptive_width=True,
            pos_hint={"center_x": 0.5}
        )
        
        trend_button = MDFlatButton(
            text="Trend Line",
            on_release=lambda x: self.switch_chart("trend")
        )
        
        histogram_button = MDFlatButton(
            text="Distribution",
            on_release=lambda x: self.switch_chart("histogram")
        )
        
        monthly_button = MDFlatButton(
            text="Monthly Avg",
            on_release=lambda x: self.switch_chart("monthly")
        )
        
        button_layout.add_widget(trend_button)
        button_layout.add_widget(histogram_button)
        button_layout.add_widget(monthly_button)
        
        header_card.add_widget(title)
        header_card.add_widget(button_layout)
        
        # Chart container
        self.chart_card = MDCard(
            orientation="vertical",
            padding=dp(10),
            elevation=2,
            radius=[10]
        )
        
        self.chart_container = MDBoxLayout(
            orientation="vertical"
        )
        
        self.chart_card.add_widget(self.chart_container)
        
        # Add widgets to main layout
        main_layout.add_widget(header_card)
        main_layout.add_widget(self.chart_card)
        
        self.add_widget(main_layout)
        
        # Initialize with trend chart
        self.create_trend_chart()
    
    def refresh_charts(self):
        """Refresh the current chart with latest data."""
        if self.current_chart == "trend":
            self.create_trend_chart()
        elif self.current_chart == "histogram":
            self.create_histogram_chart()
        elif self.current_chart == "monthly":
            self.create_monthly_chart()
    
    def switch_chart(self, chart_type):
        """Switch to a different chart type."""
        self.current_chart = chart_type
        self.refresh_charts()
    
    def create_trend_chart(self):
        """Create a trend line chart showing iron levels over time."""
        self.chart_container.clear_widgets()
        
        try:
            readings = self.db_manager.get_all_readings()
            if not readings:
                self.show_no_data_message()
                return
            
            # Prepare data
            dates = []
            levels = []
            
            for reading in reversed(readings):  # Reverse to get chronological order
                date_obj = datetime.strptime(reading['reading_date'], '%Y-%m-%d').date()
                dates.append(date_obj)
                levels.append(reading['iron_level'])
            
            # Get normal range
            profile = self.db_manager.get_user_profile()
            normal_min = profile.get('normal_range_min', 60)
            normal_max = profile.get('normal_range_max', 170)
            
            # Create the plot
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor('#FAFAFA')
            
            # Plot the trend line
            ax.plot(dates, levels, marker='o', linewidth=2, markersize=6, 
                   color='#F44336', alpha=0.8, label='Iron Levels')
            
            # Add normal range bands
            ax.axhspan(normal_min, normal_max, alpha=0.2, color='green', 
                      label=f'Normal Range ({normal_min}-{normal_max} μg/dL)')
            ax.axhline(y=normal_min, color='green', linestyle='--', alpha=0.5)
            ax.axhline(y=normal_max, color='green', linestyle='--', alpha=0.5)
            
            # Formatting
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Iron Level (μg/dL)', fontsize=12)
            ax.set_title('Iron Level Trend Over Time', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # Format dates on x-axis
            if len(dates) > 10:
                ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
            else:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
            
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            
            # Adjust layout
            fig.tight_layout()
            
            # Add to Kivy
            canvas = FigureCanvasKivyAgg(fig)
            self.chart_container.add_widget(canvas)
            
        except Exception as e:
            print(f"Error creating trend chart: {e}")
            self.show_error_message("Error creating trend chart")
    
    def create_histogram_chart(self):
        """Create a histogram showing distribution of iron levels."""
        self.chart_container.clear_widgets()
        
        try:
            readings = self.db_manager.get_all_readings()
            if not readings:
                self.show_no_data_message()
                return
            
            # Prepare data
            levels = [reading['iron_level'] for reading in readings]
            
            # Get normal range
            profile = self.db_manager.get_user_profile()
            normal_min = profile.get('normal_range_min', 60)
            normal_max = profile.get('normal_range_max', 170)
            
            # Create the plot
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor('#FAFAFA')
            
            # Create histogram
            n_bins = min(15, len(levels) // 2 + 1) if len(levels) > 10 else 5
            counts, bins, patches = ax.hist(levels, bins=n_bins, alpha=0.7, 
                                          color='#2196F3', edgecolor='black')
            
            # Color bars based on normal range
            for i, patch in enumerate(patches):
                bin_center = (bins[i] + bins[i+1]) / 2
                if bin_center < normal_min:
                    patch.set_facecolor('#F44336')  # Red for low
                elif bin_center > normal_max:
                    patch.set_facecolor('#FF9800')  # Orange for high
                else:
                    patch.set_facecolor('#4CAF50')  # Green for normal
            
            # Add normal range indicators
            ax.axvline(x=normal_min, color='green', linestyle='--', alpha=0.7, 
                      label=f'Normal Range ({normal_min}-{normal_max} μg/dL)')
            ax.axvline(x=normal_max, color='green', linestyle='--', alpha=0.7)
            
            # Formatting
            ax.set_xlabel('Iron Level (μg/dL)', fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.set_title('Distribution of Iron Levels', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            ax.legend()
            
            # Add statistics text
            mean_level = np.mean(levels)
            std_level = np.std(levels)
            ax.text(0.02, 0.98, f'Mean: {mean_level:.1f} μg/dL\nStd Dev: {std_level:.1f} μg/dL', 
                   transform=ax.transAxes, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            # Adjust layout
            fig.tight_layout()
            
            # Add to Kivy
            canvas = FigureCanvasKivyAgg(fig)
            self.chart_container.add_widget(canvas)
            
        except Exception as e:
            print(f"Error creating histogram chart: {e}")
            self.show_error_message("Error creating histogram chart")
    
    def create_monthly_chart(self):
        """Create a chart showing monthly average iron levels."""
        self.chart_container.clear_widgets()
        
        try:
            readings = self.db_manager.get_all_readings()
            if not readings:
                self.show_no_data_message()
                return
            
            # Group readings by month
            monthly_data = {}
            for reading in readings:
                date_obj = datetime.strptime(reading['reading_date'], '%Y-%m-%d').date()
                month_key = date_obj.replace(day=1)  # First day of month as key
                
                if month_key not in monthly_data:
                    monthly_data[month_key] = []
                monthly_data[month_key].append(reading['iron_level'])
            
            # Calculate monthly averages
            months = sorted(monthly_data.keys())
            averages = [np.mean(monthly_data[month]) for month in months]
            
            if len(months) < 2:
                self.show_no_data_message("Need at least 2 months of data for monthly chart")
                return
            
            # Get normal range
            profile = self.db_manager.get_user_profile()
            normal_min = profile.get('normal_range_min', 60)
            normal_max = profile.get('normal_range_max', 170)
            
            # Create the plot
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor('#FAFAFA')
            
            # Plot monthly averages
            bars = ax.bar(months, averages, alpha=0.7, color='#9C27B0', 
                         edgecolor='black', linewidth=1)
            
            # Color bars based on normal range
            for i, (month, avg) in enumerate(zip(months, averages)):
                if avg < normal_min:
                    bars[i].set_facecolor('#F44336')  # Red for low
                elif avg > normal_max:
                    bars[i].set_facecolor('#FF9800')  # Orange for high
                else:
                    bars[i].set_facecolor('#4CAF50')  # Green for normal
            
            # Add normal range indicators
            ax.axhspan(normal_min, normal_max, alpha=0.2, color='green', 
                      label=f'Normal Range ({normal_min}-{normal_max} μg/dL)')
            ax.axhline(y=normal_min, color='green', linestyle='--', alpha=0.5)
            ax.axhline(y=normal_max, color='green', linestyle='--', alpha=0.5)
            
            # Formatting
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Average Iron Level (μg/dL)', fontsize=12)
            ax.set_title('Monthly Average Iron Levels', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            ax.legend()
            
            # Format dates on x-axis
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            
            # Adjust layout
            fig.tight_layout()
            
            # Add to Kivy
            canvas = FigureCanvasKivyAgg(fig)
            self.chart_container.add_widget(canvas)
            
        except Exception as e:
            print(f"Error creating monthly chart: {e}")
            self.show_error_message("Error creating monthly chart")
    
    def show_no_data_message(self, custom_message=None):
        """Show a message when no data is available."""
        message = custom_message or "No data available for charts.\nAdd some iron level readings first."
        
        no_data_label = MDLabel(
            text=message,
            theme_text_color="Secondary",
            halign="center",
            valign="center",
            font_style="H6"
        )
        
        self.chart_container.add_widget(no_data_label)
    
    def show_error_message(self, error_text):
        """Show an error message."""
        error_label = MDLabel(
            text=f"Error: {error_text}",
            theme_text_color="Error",
            halign="center",
            valign="center",
            font_style="H6"
        )
        
        self.chart_container.add_widget(error_label)