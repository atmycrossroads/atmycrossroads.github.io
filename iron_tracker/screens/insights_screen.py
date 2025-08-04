from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
from datetime import datetime, date, timedelta
import statistics


class InsightsScreen(MDScreen):
    """Screen for displaying health insights and recommendations based on iron levels."""
    
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.db_manager = db_manager
        self.profile_dialog = None
        self.build_ui()
    
    def build_ui(self):
        """Build the user interface for the insights screen."""
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )
        
        # Scrollable content
        scroll = MDScrollView()
        content_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            adaptive_height=True,
            size_hint_y=None
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Title
        title = MDLabel(
            text="Health Insights & Recommendations",
            theme_text_color="Primary",
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=dp(50)
        )
        
        # Profile section
        self.profile_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            elevation=2,
            radius=[10],
            size_hint_y=None,
            height=dp(120)
        )
        
        profile_title = MDLabel(
            text="Your Profile",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        )
        
        self.profile_info_label = MDLabel(
            text="Loading profile...",
            theme_text_color="Secondary",
            font_style="Body2",
            size_hint_y=None,
            height=dp(40)
        )
        
        update_profile_button = MDFlatButton(
            text="Update Profile",
            on_release=self.open_profile_dialog,
            size_hint_y=None,
            height=dp(40)
        )
        
        self.profile_card.add_widget(profile_title)
        self.profile_card.add_widget(self.profile_info_label)
        self.profile_card.add_widget(update_profile_button)
        
        # Current status section
        self.status_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            elevation=2,
            radius=[10],
            size_hint_y=None,
            height=dp(150)
        )
        
        status_title = MDLabel(
            text="Current Status",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        )
        
        self.status_label = MDLabel(
            text="Loading status...",
            theme_text_color="Secondary",
            font_style="Body2",
            text_size=(None, None),
            size_hint_y=None,
            height=dp(100)
        )
        
        self.status_card.add_widget(status_title)
        self.status_card.add_widget(self.status_label)
        
        # Trends section
        self.trends_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            elevation=2,
            radius=[10],
            size_hint_y=None,
            height=dp(200)
        )
        
        trends_title = MDLabel(
            text="Trends & Patterns",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        )
        
        self.trends_label = MDLabel(
            text="Loading trends...",
            theme_text_color="Secondary",
            font_style="Body2",
            text_size=(None, None),
            size_hint_y=None,
            height=dp(150)
        )
        
        self.trends_card.add_widget(trends_title)
        self.trends_card.add_widget(self.trends_label)
        
        # Recommendations section
        self.recommendations_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            elevation=2,
            radius=[10],
            size_hint_y=None,
            height=dp(300)
        )
        
        recommendations_title = MDLabel(
            text="Recommendations",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        )
        
        self.recommendations_label = MDLabel(
            text="Loading recommendations...",
            theme_text_color="Secondary",
            font_style="Body2",
            text_size=(None, None),
            size_hint_y=None,
            height=dp(250)
        )
        
        self.recommendations_card.add_widget(recommendations_title)
        self.recommendations_card.add_widget(self.recommendations_label)
        
        # Educational content section
        education_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            elevation=1,
            radius=[10],
            size_hint_y=None,
            height=dp(250)
        )
        
        education_title = MDLabel(
            text="About Iron Levels",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        )
        
        education_content = MDLabel(
            text=self.get_educational_content(),
            theme_text_color="Secondary",
            font_style="Body2",
            text_size=(None, None),
            size_hint_y=None,
            height=dp(200)
        )
        
        education_card.add_widget(education_title)
        education_card.add_widget(education_content)
        
        # Add all cards to content layout
        content_layout.add_widget(title)
        content_layout.add_widget(self.profile_card)
        content_layout.add_widget(self.status_card)
        content_layout.add_widget(self.trends_card)
        content_layout.add_widget(self.recommendations_card)
        content_layout.add_widget(education_card)
        
        scroll.add_widget(content_layout)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)
    
    def refresh_insights(self):
        """Refresh all insights and recommendations."""
        self.update_profile_display()
        self.analyze_current_status()
        self.analyze_trends()
        self.generate_recommendations()
    
    def update_profile_display(self):
        """Update the profile information display."""
        try:
            profile = self.db_manager.get_user_profile()
            if profile:
                age = profile.get('age', 'Not set')
                gender = profile.get('gender', 'Not set').title()
                normal_min = profile.get('normal_range_min', 60)
                normal_max = profile.get('normal_range_max', 170)
                
                self.profile_info_label.text = (
                    f"Age: {age}  •  Gender: {gender}\n"
                    f"Normal Range: {normal_min}-{normal_max} μg/dL"
                )
            else:
                self.profile_info_label.text = "Profile not set up"
        except Exception as e:
            print(f"Error updating profile display: {e}")
            self.profile_info_label.text = "Error loading profile"
    
    def analyze_current_status(self):
        """Analyze current iron level status."""
        try:
            recent_readings = self.db_manager.get_recent_readings(5)
            if not recent_readings:
                self.status_label.text = "No readings available for analysis"
                return
            
            latest_reading = recent_readings[0]
            iron_level = latest_reading['iron_level']
            reading_date = latest_reading['reading_date']
            
            profile = self.db_manager.get_user_profile()
            normal_min = profile.get('normal_range_min', 60)
            normal_max = profile.get('normal_range_max', 170)
            
            # Determine status
            if iron_level < normal_min:
                status = "LOW"
                status_color = "🔴"
                interpretation = "Your iron level is below normal range"
            elif iron_level > normal_max:
                status = "HIGH"
                status_color = "🟠"
                interpretation = "Your iron level is above normal range"
            else:
                status = "NORMAL"
                status_color = "🟢"
                interpretation = "Your iron level is within normal range"
            
            # Calculate days since last reading
            days_ago = (date.today() - datetime.strptime(reading_date, '%Y-%m-%d').date()).days
            
            if days_ago == 0:
                time_text = "today"
            elif days_ago == 1:
                time_text = "yesterday"
            else:
                time_text = f"{days_ago} days ago"
            
            self.status_label.text = (
                f"{status_color} Latest Reading: {iron_level} μg/dL ({time_text})\n"
                f"Status: {status}\n"
                f"{interpretation}\n"
                f"Normal range: {normal_min}-{normal_max} μg/dL"
            )
            
        except Exception as e:
            print(f"Error analyzing current status: {e}")
            self.status_label.text = "Error analyzing current status"
    
    def analyze_trends(self):
        """Analyze iron level trends and patterns."""
        try:
            # Get readings from last 3 months
            three_months_ago = date.today() - timedelta(days=90)
            recent_readings = self.db_manager.get_readings_by_date_range(three_months_ago, date.today())
            
            if len(recent_readings) < 3:
                self.trends_label.text = "Need at least 3 readings for trend analysis"
                return
            
            # Extract iron levels and dates
            levels = [reading['iron_level'] for reading in recent_readings]
            dates = [datetime.strptime(reading['reading_date'], '%Y-%m-%d').date() for reading in recent_readings]
            
            # Calculate trend
            if len(levels) >= 3:
                recent_levels = levels[-3:]
                if recent_levels[-1] > recent_levels[0]:
                    trend = "INCREASING 📈"
                elif recent_levels[-1] < recent_levels[0]:
                    trend = "DECREASING 📉"
                else:
                    trend = "STABLE ➡️"
            else:
                trend = "INSUFFICIENT DATA"
            
            # Calculate statistics
            avg_level = statistics.mean(levels)
            std_dev = statistics.stdev(levels) if len(levels) > 1 else 0
            min_level = min(levels)
            max_level = max(levels)
            
            # Calculate variability
            if std_dev < 10:
                variability = "Low variability (stable)"
            elif std_dev < 20:
                variability = "Moderate variability"
            else:
                variability = "High variability (fluctuating)"
            
            # Get normal range for comparison
            profile = self.db_manager.get_user_profile()
            normal_min = profile.get('normal_range_min', 60)
            normal_max = profile.get('normal_range_max', 170)
            
            # Count readings in each range
            low_count = sum(1 for level in levels if level < normal_min)
            normal_count = sum(1 for level in levels if normal_min <= level <= normal_max)
            high_count = sum(1 for level in levels if level > normal_max)
            
            self.trends_label.text = (
                f"Trend (last 3 readings): {trend}\n"
                f"Average: {avg_level:.1f} μg/dL\n"
                f"Range: {min_level:.1f} - {max_level:.1f} μg/dL\n"
                f"{variability}\n\n"
                f"Reading distribution:\n"
                f"• Normal: {normal_count}/{len(levels)} readings\n"
                f"• Low: {low_count}/{len(levels)} readings\n"
                f"• High: {high_count}/{len(levels)} readings"
            )
            
        except Exception as e:
            print(f"Error analyzing trends: {e}")
            self.trends_label.text = "Error analyzing trends"
    
    def generate_recommendations(self):
        """Generate personalized recommendations based on iron levels."""
        try:
            recent_readings = self.db_manager.get_recent_readings(5)
            if not recent_readings:
                self.recommendations_label.text = "No data available for recommendations"
                return
            
            latest_reading = recent_readings[0]
            iron_level = latest_reading['iron_level']
            
            profile = self.db_manager.get_user_profile()
            normal_min = profile.get('normal_range_min', 60)
            normal_max = profile.get('normal_range_max', 170)
            
            recommendations = []
            
            if iron_level < normal_min:
                # Low iron recommendations
                recommendations.extend([
                    "🍖 Increase iron-rich foods: red meat, poultry, fish",
                    "🥬 Include iron-rich vegetables: spinach, lentils, beans",
                    "🍊 Combine with Vitamin C sources to enhance absorption",
                    "☕ Avoid tea and coffee with meals (they reduce absorption)",
                    "💊 Consider iron supplements (consult your doctor first)",
                    "👨‍⚕️ Schedule follow-up with healthcare provider"
                ])
            elif iron_level > normal_max:
                # High iron recommendations
                recommendations.extend([
                    "🥗 Reduce iron-rich foods temporarily",
                    "🫖 Drink tea with meals to reduce iron absorption",
                    "🥛 Increase calcium-rich foods (they inhibit iron absorption)",
                    "🚫 Avoid iron supplements unless prescribed",
                    "👨‍⚕️ Consult doctor - high iron can indicate health issues",
                    "💧 Stay well hydrated"
                ])
            else:
                # Normal iron recommendations
                recommendations.extend([
                    "✅ Maintain your current diet and lifestyle",
                    "🏃‍♂️ Continue regular exercise",
                    "📊 Keep monitoring your iron levels regularly",
                    "🥗 Maintain balanced diet with variety of nutrients",
                    "💧 Stay well hydrated"
                ])
            
            # General recommendations
            recommendations.extend([
                "",
                "General Health Tips:",
                "📱 Track your readings regularly in this app",
                "📝 Note any symptoms or changes you experience",
                "🏥 Bring your iron tracking data to doctor visits",
                "📚 Stay informed about iron and health"
            ])
            
            # Add timing recommendation
            days_since_last = (date.today() - datetime.strptime(latest_reading['reading_date'], '%Y-%m-%d').date()).days
            if days_since_last > 30:
                recommendations.append("⏰ Consider getting a new iron level test soon")
            
            self.recommendations_label.text = "\n".join(recommendations)
            
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            self.recommendations_label.text = "Error generating recommendations"
    
    def get_educational_content(self):
        """Get educational content about iron levels."""
        return (
            "Iron is essential for:\n"
            "• Oxygen transport in blood (hemoglobin)\n"
            "• Energy production in cells\n"
            "• Immune system function\n"
            "• Brain development and function\n\n"
            
            "Normal ranges vary by:\n"
            "• Age and gender\n"
            "• Pregnancy status\n"
            "• Individual health conditions\n\n"
            
            "Symptoms of low iron:\n"
            "• Fatigue and weakness\n"
            "• Pale skin and nails\n"
            "• Shortness of breath\n"
            "• Cold hands and feet\n\n"
            
            "Symptoms of high iron:\n"
            "• Joint pain\n"
            "• Fatigue\n"
            "• Abdominal pain\n"
            "• Heart problems (severe cases)"
        )
    
    def open_profile_dialog(self, instance):
        """Open dialog to update user profile."""
        if not self.profile_dialog:
            # Get current profile
            profile = self.db_manager.get_user_profile()
            
            content = MDBoxLayout(
                orientation="vertical",
                spacing=dp(10),
                size_hint_y=None,
                height=dp(300)
            )
            
            self.age_field = MDTextField(
                hint_text="Age",
                text=str(profile.get('age', '')),
                input_filter="int",
                mode="outlined"
            )
            
            self.gender_field = MDTextField(
                hint_text="Gender (male/female/other)",
                text=profile.get('gender', ''),
                mode="outlined"
            )
            
            self.normal_min_field = MDTextField(
                hint_text="Normal Range Minimum (μg/dL)",
                text=str(profile.get('normal_range_min', 60)),
                input_filter="float",
                mode="outlined"
            )
            
            self.normal_max_field = MDTextField(
                hint_text="Normal Range Maximum (μg/dL)",
                text=str(profile.get('normal_range_max', 170)),
                input_filter="float",
                mode="outlined"
            )
            
            content.add_widget(self.age_field)
            content.add_widget(self.gender_field)
            content.add_widget(self.normal_min_field)
            content.add_widget(self.normal_max_field)
            
            self.profile_dialog = MDDialog(
                title="Update Profile",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=self.close_profile_dialog
                    ),
                    MDFlatButton(
                        text="SAVE",
                        on_release=self.save_profile
                    ),
                ],
            )
        
        self.profile_dialog.open()
    
    def close_profile_dialog(self, instance):
        """Close the profile dialog."""
        if self.profile_dialog:
            self.profile_dialog.dismiss()
    
    def save_profile(self, instance):
        """Save the updated profile."""
        try:
            age = int(self.age_field.text) if self.age_field.text.strip() else None
            gender = self.gender_field.text.strip().lower() if self.gender_field.text.strip() else None
            normal_min = float(self.normal_min_field.text) if self.normal_min_field.text.strip() else None
            normal_max = float(self.normal_max_field.text) if self.normal_max_field.text.strip() else None
            
            success = self.db_manager.update_user_profile(
                age=age, 
                gender=gender, 
                normal_range_min=normal_min, 
                normal_range_max=normal_max
            )
            
            if success:
                self.show_snackbar("Profile updated successfully!")
                self.refresh_insights()
            else:
                self.show_snackbar("Error updating profile")
                
        except ValueError:
            self.show_snackbar("Please enter valid numeric values")
        except Exception as e:
            print(f"Error saving profile: {e}")
            self.show_snackbar("Error updating profile")
        finally:
            self.close_profile_dialog(None)
    
    def show_snackbar(self, message):
        """Show a snackbar with the given message."""
        snackbar = Snackbar(text=message, duration=3)
        snackbar.open()