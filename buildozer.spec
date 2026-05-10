# (str) Title of your application
title = Tera

# (str) Package name
package.name = tera

# (str) Package domain (needed for android packaging)
package.domain = org.lzvsrx

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,db,ttf,otf

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,*.ttf,*.otf

# (str) Application version
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,sqlite3,pillow

# (str) Presplash of your application
#presplash.filename = %(source.dir)s/assets/logo.png

# (str) Icon of your application
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (list) Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Allow skipping setup of pyjnius
android.skip_setup_pyjnius = 0

[buildozer]
log_level = 2
warn_on_root = 1
