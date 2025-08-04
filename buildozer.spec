[app]

# (str) Title of your application
title = Iron Level Tracker

# (str) Package name
package.name = irontracker

# (str) Package domain (needed for android/ios packaging)
package.domain = org.healthapps

# (str) Source code where the main.py live
source.dir = iron_tracker

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,db

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
requirements = python3,kivy==2.2.1,kivymd==1.1.1,matplotlib==3.7.2,python-dateutil==2.8.2,pillow==10.0.0,numpy==1.24.3

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (landscape, sensorLandscape, portrait, sensorPortrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

[android]

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (list) Pattern to whitelist for the whole project
#android.whitelist = 

# (str) Android app theme, default is ok for Kivy-based app
# android.theme = "@android:style/Theme.NoTitleBar"

# (list) Android application meta-data to set (key=value format)
#android.meta_data = 

# (list) Android library project to add (will be added in the libs dir)
#android.library_references = 

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = arm64-v8a

# (int) overrides automatic versionCode computation (used in build.gradle)
# this is not the same as app version and should only be edited if you know what you're doing
# android.numeric_version = 1

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for Android backup rules
# android.backup_rules = 

# (str) If you need to insert variables into your AndroidManifest.xml file,
# you can do so with the manifestPlaceholders property.
# This property takes a map of key-value pairs. (via a string)
# android.manifest_placeholders = [:]

# (bool) Skip byte compile for .py files
# android.no-byte-compile-python = False

# (str) The format used to package the app for release mode (aab or apk).
# android.release_artifact = aab

[python]

# (str) python-for-android fork to use, defaults to upstream (kivy)
#p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#p4a.source_dir = 

# (str) The directory in which python-for-android should look for your own build recipes (if any)
#p4a.local_recipes = 

# (str) Filename to the hook for p4a
#p4a.hook = 

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
#p4a.port = 

# Control passing the --private-data-dir python-for-android bootstrap option
# p4a.private_data_dir = True

# Pass --use-setup-py or --ignore-setup-py to p4a
# --use-setup-py is the default behaviour in p4a
# --ignore-setup-py by default ignores setup.py
# Setting either one to false will pass the other one to p4a
# (bool) Use setup.py (True) or ignore (False)
#p4a.setup_py = false

# (str) extra command line arguments to pass when invoking pythonforandroid.toolchain
#p4a.extra_args = 

[garden]

# (str) URL to use to checkout garden sources
# May be git, hg or a local path
# garden.source_url = 

# (str) filename to checkout from garden sources
# garden.filename = 

# (bool) whether kivy garden modules should be included into the package
# garden.requirements = 

# (list) Garden modules to include
garden.requirements = matplotlib