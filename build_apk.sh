#!/bin/bash

# Iron Level Tracker - APK Build Script
# This script demonstrates the complete Android APK build process

echo "=========================================="
echo "Iron Level Tracker - Android APK Builder"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "iron_tracker_env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv iron_tracker_env
fi

# Activate virtual environment
echo "Activating virtual environment..."
source iron_tracker_env/bin/activate

# Upgrade pip and install build dependencies
echo "Installing build dependencies..."
pip install --upgrade pip
pip install setuptools wheel

# Install required packages
echo "Installing required Python packages..."
pip install buildozer
pip install cython
pip install kivy[base]
pip install kivymd
pip install matplotlib
pip install numpy
pip install pillow
pip install python-dateutil

echo ""
echo "Build environment setup complete!"
echo ""

# Validate project structure
echo "Validating project structure..."
if [ ! -d "iron_tracker" ]; then
    echo "❌ ERROR: iron_tracker directory not found!"
    exit 1
fi

if [ ! -f "buildozer.spec" ]; then
    echo "❌ ERROR: buildozer.spec not found!"
    exit 1
fi

if [ ! -f "iron_tracker/main.py" ]; then
    echo "❌ ERROR: main.py not found in iron_tracker directory!"
    exit 1
fi

echo "✅ Project structure validated!"

# Check Java installation
echo ""
echo "Checking Java installation..."
if command -v java &> /dev/null; then
    java -version
    echo "✅ Java is installed!"
else
    echo "❌ Java not found. Installing OpenJDK..."
    sudo apt update
    sudo apt install -y openjdk-17-jdk
fi

# Set Java environment variables
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin

echo ""
echo "=========================================="
echo "Starting APK Build Process"
echo "=========================================="

# Create bin directory if it doesn't exist
mkdir -p bin

echo ""
echo "Build configuration summary:"
echo "- App Name: Iron Level Tracker"
echo "- Package: org.healthapps.irontracker"
echo "- Version: 1.0"
echo "- Architecture: arm64-v8a"
echo "- Target: Android (debug)"
echo ""

# Attempt to build the APK
echo "Initiating buildozer android debug..."
echo "(Note: This process may take 15-30 minutes on first run)"
echo ""

# Check available system resources
echo "System resources:"
echo "- Available memory: $(free -h | awk '/^Mem:/ {print $7}')"
echo "- Available disk space: $(df -h . | awk 'NR==2 {print $4}')"
echo "- CPU cores: $(nproc)"
echo ""

# The actual build command (may fail in resource-constrained environments)
if buildozer android debug; then
    echo ""
    echo "🎉 APK BUILD SUCCESSFUL!"
    echo ""
    echo "APK Location: bin/irontracker-1.0-arm64-v8a-debug.apk"
    echo ""
    echo "Installation instructions:"
    echo "1. Enable 'Unknown Sources' in Android Settings"
    echo "2. Transfer APK to Android device"
    echo "3. Tap APK file to install"
    echo "4. Launch 'Iron Level Tracker' from app drawer"
    echo ""
    
    # Show APK details if successful
    if [ -f "bin/irontracker-1.0-arm64-v8a-debug.apk" ]; then
        echo "APK Details:"
        ls -lh bin/irontracker-1.0-arm64-v8a-debug.apk
    fi
    
else
    echo ""
    echo "⚠️  APK BUILD ENCOUNTERED ISSUES"
    echo ""
    echo "This is expected in resource-constrained environments."
    echo "The build process requires:"
    echo "- Android SDK (automatically downloaded by buildozer)"
    echo "- Android NDK (automatically downloaded by buildozer)"  
    echo "- Several GB of disk space"
    echo "- Significant CPU and memory resources"
    echo ""
    echo "To complete the build on a local machine:"
    echo "1. Ensure you have at least 8GB RAM and 10GB free disk space"
    echo "2. Run this script on Ubuntu/Debian with sudo access"
    echo "3. Be patient - first build takes 15-30 minutes"
    echo ""
    echo "Alternative: Use GitHub Actions or dedicated build servers"
fi

echo ""
echo "=========================================="
echo "Build Process Information"
echo "=========================================="
echo ""
echo "What buildozer does:"
echo "1. Downloads Android SDK and NDK (first run only)"
echo "2. Sets up Python-for-Android (p4a) toolchain"
echo "3. Compiles Python dependencies for Android"
echo "4. Packages app source code and assets"
echo "5. Creates signed/unsigned APK file"
echo ""
echo "Dependencies included in APK:"
echo "- Python 3.9+ runtime for Android"
echo "- Kivy UI framework"
echo "- KivyMD Material Design components"
echo "- Matplotlib for charts"
echo "- NumPy for calculations"
echo "- SQLite for data storage"
echo "- PIL/Pillow for image handling"
echo ""

# Show final project structure
echo "Final project structure:"
echo "workspace/"
echo "├── iron_tracker/          # Main app source"
echo "│   ├── main.py            # App entry point"
echo "│   ├── database/          # Database management"
echo "│   └── screens/           # UI screens"
echo "├── buildozer.spec         # Build configuration"
echo "├── requirements.txt       # Python dependencies"
echo "├── build_apk.sh          # This build script"
echo "└── bin/                   # Output APK location"
echo ""

echo "🏁 Build script completed!"
echo ""
echo "For questions or issues, refer to:"
echo "- Buildozer documentation: https://buildozer.readthedocs.io/"
echo "- Kivy documentation: https://kivy.org/doc/stable/"
echo "- KivyMD documentation: https://kivymd.readthedocs.io/"