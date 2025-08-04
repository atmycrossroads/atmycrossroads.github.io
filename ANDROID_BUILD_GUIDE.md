# Iron Level Tracker - Android APK Build Guide

## 🚀 Complete Instructions for Building the Android APK

Due to the resource-intensive nature of Android APK compilation (requiring 8+ GB RAM, 10+ GB disk space, and significant CPU time), the build process is best completed on a local development machine or dedicated build server.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Ubuntu 20.04+ or Debian-based Linux
- **RAM**: Minimum 8GB (16GB recommended)
- **Disk Space**: At least 10GB free space
- **CPU**: Multi-core processor (build time: 15-30 minutes first run)
- **Internet**: Stable connection for downloading Android SDK/NDK

### Required Software
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-venv python3-pip python3-dev 
sudo apt install -y build-essential git zip unzip
sudo apt install -y openjdk-17-jdk

# Verify Java installation
java -version
```

## 🛠️ Build Process

### Step 1: Prepare the Environment
```bash
# Clone or download the Iron Tracker project
git clone <your-repo-url>
cd iron-tracker-android

# Create and activate virtual environment
python3 -m venv build_env
source build_env/bin/activate

# Upgrade pip and install build tools
pip install --upgrade pip
pip install setuptools wheel cython
```

### Step 2: Install Dependencies
```bash
# Install buildozer and dependencies
pip install buildozer
pip install kivy[base] kivymd
pip install matplotlib numpy pillow python-dateutil

# Install additional requirements
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
```bash
# Set Java environment
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin

# Optional: Set Android SDK path (buildozer will download if not set)
# export ANDROID_HOME=$HOME/.buildozer/android/platform/android-sdk
```

### Step 4: Build the APK
```bash
# Initialize buildozer (creates buildozer.spec if needed)
buildozer init

# Build debug APK (first run downloads ~2GB of Android tools)
buildozer android debug

# For release build (requires signing):
# buildozer android release
```

### Step 5: Locate Your APK
```bash
# Find the generated APK
ls -la bin/
# Output: irontracker-1.0-arm64-v8a-debug.apk
```

## 📱 APK Installation

### On Android Device
1. **Enable Developer Options**:
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times
   - Go back to Settings > Developer Options
   - Enable "USB Debugging" and "Install via USB"

2. **Enable Unknown Sources**:
   - Settings > Security > Unknown Sources (enable)
   - Or Settings > Apps > Special Access > Install Unknown Apps

3. **Install APK**:
   ```bash
   # Via ADB (if connected via USB)
   adb install bin/irontracker-1.0-arm64-v8a-debug.apk
   
   # Or transfer APK to device and tap to install
   ```

## 🔧 Build Configuration

The `buildozer.spec` file contains all build settings:

```ini
[app]
title = Iron Level Tracker
package.name = irontracker
package.domain = org.healthapps
source.dir = iron_tracker
version = 1.0
requirements = python3,kivy,kivymd,matplotlib,numpy,pillow,python-dateutil

[android]
android.arch = arm64-v8a
android.allow_backup = True

# Add permissions if needed:
# android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. Build Fails with "No module named 'distutils'"
```bash
pip install setuptools
```

#### 2. Java Not Found
```bash
sudo apt install openjdk-17-jdk
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
```

#### 3. Insufficient Memory
```bash
# Increase swap space
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### 4. NDK/SDK Download Issues
```bash
# Clear buildozer cache and retry
buildozer android clean
rm -rf ~/.buildozer
buildozer android debug
```

#### 5. Permission Errors
```bash
# Fix permissions
chmod -R 755 ~/.buildozer
```

## 🚀 Automated Build Script

Save this as `build.sh` and run `chmod +x build.sh && ./build.sh`:

```bash
#!/bin/bash
set -e

echo "🏗️  Building Iron Level Tracker APK..."

# Create virtual environment
python3 -m venv build_env
source build_env/bin/activate

# Install dependencies
pip install --upgrade pip setuptools wheel
pip install buildozer cython
pip install -r requirements.txt

# Set environment
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Build APK
echo "⚡ Starting buildozer..."
buildozer android debug

# Check result
if [ -f "bin/irontracker-1.0-arm64-v8a-debug.apk" ]; then
    echo "✅ APK built successfully!"
    echo "📍 Location: bin/irontracker-1.0-arm64-v8a-debug.apk"
    echo "📦 Size: $(du -h bin/irontracker-1.0-arm64-v8a-debug.apk | cut -f1)"
else
    echo "❌ APK build failed!"
    exit 1
fi
```

## 📊 What's Included in the APK

The compiled APK includes:
- **Python Runtime**: Full Python 3.9+ interpreter for Android
- **Kivy Framework**: Cross-platform Python UI framework
- **KivyMD Components**: Material Design UI components
- **Matplotlib**: Scientific plotting and charting library
- **NumPy**: Numerical computing library
- **SQLite**: Database engine (built into Android)
- **App Source Code**: All Iron Tracker screens and logic
- **Assets**: Icons, fonts, and resources

## 🎯 Expected APK Size
- **Debug APK**: ~50-80 MB (includes debugging symbols)
- **Release APK**: ~40-60 MB (optimized and compressed)

## 🔄 CI/CD Options

For automated builds, consider:

### GitHub Actions
```yaml
name: Build APK
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Build APK
      run: |
        sudo apt install openjdk-17-jdk
        pip install buildozer cython
        buildozer android debug
    - name: Upload APK
      uses: actions/upload-artifact@v2
      with:
        name: iron-tracker-apk
        path: bin/*.apk
```

### Docker Build
```dockerfile
FROM ubuntu:22.04
RUN apt update && apt install -y python3 python3-pip openjdk-17-jdk
COPY . /app
WORKDIR /app
RUN pip install buildozer cython
RUN buildozer android debug
```

## 📝 Build Logs

Build process generates logs in:
- `.buildozer/android/platform/`
- `.buildozer/android/logs/`

Check these for detailed error information if build fails.

## 🎉 Success Indicators

Build successful when you see:
```
# Package the application
...
# APK generated successfully
# Command: buildozer android debug
# Build completed successfully
```

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review buildozer logs in `.buildozer/android/logs/`
3. Search [Buildozer GitHub Issues](https://github.com/kivy/buildozer/issues)
4. Ask on [Kivy Discord](https://discord.gg/kivy)

---

**Happy Building! 🚀📱**