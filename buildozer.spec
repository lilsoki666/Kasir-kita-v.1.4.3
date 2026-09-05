[app]

# (str) Title of your application
title = UT Kasir Kita

# (str) Package name
package.name = utkasir

# (str) Package domain (needed for android/ios packaging)
package.domain = org.kasir.kita

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,ttf,db

# (str) Application versioning
version = 1.4.3

# (list) Application requirements
requirements = python3,kivy,pillow,sqlite3

# --- ICON & PRESPLASH (PASTIKAN HANYA ADA 1 BARIS INI) ---
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

#
# Android specific
#

# (list) Permissions
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES

# Paksa Buildozer menggunakan SDK bawaan sistem/environment
android.sdk_path = /usr/local/lib/android/sdk

# Kunci Build-Tools ke 30.0.3
android.build_tools_version = 30.0.3

# (int) Target Android API
android.api = 33

# (int) Minimum API supported
android.minapi = 24

# (str) Android NDK version
android.ndk = 25b

# (int) Android NDK API
android.ndk_api = 24

# (bool) Private storage
android.private_storage = True

# (list) Architectures to build
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enable Android auto backup
android.allow_backup = True


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
