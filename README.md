# Iron Level Tracker - Android Health App

A comprehensive Python-based Android application for tracking and monitoring blood iron levels. Built with Kivy/KivyMD, this app provides an intuitive interface for logging iron readings, visualizing trends, and receiving personalized health insights.

![Iron Level Tracker](https://img.shields.io/badge/platform-Android-green) ![Python](https://img.shields.io/badge/Python-3.7+-blue) ![Kivy](https://img.shields.io/badge/Kivy-2.2.1-orange)

## Features

### 📊 **Data Tracking**
- Log iron level readings with date and time
- Support for multiple test types (Serum Iron, Ferritin, TIBC, etc.)
- Add notes and context to readings
- Automatic data validation and normal range checking

### 📈 **Visualization & Analysis**
- Interactive trend line charts
- Distribution histograms
- Monthly average analysis
- Color-coded readings based on normal ranges

### 🧠 **Health Insights**
- Personalized recommendations based on iron levels
- Trend analysis and pattern recognition
- Educational content about iron health
- Profile-based normal range customization

### 💾 **Data Management**
- Local SQLite database storage
- Search and filter capabilities
- Export/backup functionality
- Data privacy - all data stays on device

## Screenshots

*(Add screenshots of your app here)*

## Installation

### Prerequisites

Before building the app, ensure you have:

- Python 3.7 or higher
- Android SDK (for building APK)
- Java 8 or higher
- Git

### Development Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/iron-tracker-android.git
cd iron-tracker-android
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install Kivy Garden matplotlib:**
```bash
garden install matplotlib
```

### Building for Android

1. **Install Buildozer:**
```bash
pip install buildozer
```

2. **Initialize buildozer (first time only):**
```bash
buildozer init
```

3. **Build the APK:**
```bash
buildozer android debug
```

4. **For release build:**
```bash
buildozer android release
```

The APK will be generated in the `bin/` directory.

## Usage

### First Launch
1. Open the Iron Level Tracker app
2. Navigate to "Insights" tab and set up your profile
3. Configure your normal iron range based on your doctor's recommendations

### Adding Readings
1. Tap the "Add Reading" tab
2. Enter your iron level value
3. Select date and time (defaults to current)
4. Choose test type from dropdown
5. Add optional notes
6. Tap "Save Reading"

### Viewing History
1. Go to "History" tab to view all readings
2. Use search bar to find specific readings
3. Filter by time periods (week, month, year)
4. Tap delete icon to remove readings

### Charts & Analysis
1. Visit "Charts" tab for visualizations
2. Switch between trend line, distribution, and monthly charts
3. Charts automatically show normal range indicators

### Health Insights
1. Check "Insights" tab for personalized recommendations
2. View current status and trend analysis
3. Read educational content about iron health
4. Update profile information as needed

## App Structure

```
iron_tracker/
├── main.py                 # Main application entry point
├── database/
│   └── db_manager.py      # SQLite database management
├── screens/
│   ├── input_screen.py    # Iron level input interface
│   ├── history_screen.py  # Historical data viewing
│   ├── charts_screen.py   # Data visualization
│   └── insights_screen.py # Health insights & recommendations
├── requirements.txt       # Python dependencies
├── buildozer.spec        # Android build configuration
└── README.md             # This file
```

## Database Schema

### iron_readings table
- `id`: Primary key
- `reading_date`: Date of reading
- `reading_time`: Time of reading
- `iron_level`: Iron level value (μg/dL)
- `unit`: Unit of measurement
- `notes`: Optional notes
- `test_type`: Type of iron test
- `created_at`: Timestamp

### user_profile table
- `id`: Primary key
- `age`: User age
- `gender`: User gender
- `normal_range_min`: Minimum normal iron level
- `normal_range_max`: Maximum normal iron level
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Customization

### Normal Range Values
The app uses these default normal ranges:
- **General Adult Range**: 60-170 μg/dL

You can customize these values in the Insights tab based on your healthcare provider's recommendations.

### Adding New Test Types
To add new iron test types, modify the `test_types` list in `screens/input_screen.py`:

```python
test_types = [
    "Serum Iron",
    "Transferrin Saturation", 
    "Ferritin",
    "TIBC (Total Iron Binding Capacity)",
    "UIBC (Unsaturated Iron Binding Capacity)",
    "Your New Test Type"  # Add here
]
```

## Development

### Running in Development Mode
```bash
cd iron_tracker
python main.py
```

### Code Structure
- **MVC Architecture**: Clear separation between data (database), views (screens), and logic
- **Material Design**: Uses KivyMD for modern Android UI components
- **Modular Design**: Each screen is a separate module for maintainability

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Health Disclaimer

⚠️ **Important Medical Notice:**

This app is for tracking and monitoring purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult your healthcare provider regarding:

- Iron level interpretation
- Normal range determination
- Treatment decisions
- Supplement recommendations
- Any health concerns

Never disregard professional medical advice or delay seeking it based on information from this app.

## Privacy & Data Security

- All data is stored locally on your device
- No data is transmitted to external servers
- Database is encrypted on modern Android devices
- You maintain full control of your health data

## Troubleshooting

### Common Issues

**App won't start:**
- Ensure all dependencies are installed
- Check Python version compatibility
- Verify Android SDK setup for building

**Charts not displaying:**
- Install Kivy Garden matplotlib: `garden install matplotlib`
- Check that numpy and matplotlib are properly installed

**Database errors:**
- Clear app data to reset database
- Check file permissions on Android device

**Build failures:**
- Update buildozer: `pip install --upgrade buildozer`
- Clear buildozer cache: `buildozer android clean`
- Check Android SDK and NDK versions

### Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with detailed error information
4. Include your environment details (Python version, OS, etc.)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Kivy/KivyMD**: For the excellent Python mobile development framework
- **Matplotlib**: For data visualization capabilities
- **SQLite**: For reliable local data storage
- **Material Design**: For modern UI guidelines

## Version History

### v1.0.0 (Current)
- Initial release
- Basic iron level tracking
- Charts and visualizations
- Health insights and recommendations
- Android APK support

---

**Developed with ❤️ for better health monitoring**

  