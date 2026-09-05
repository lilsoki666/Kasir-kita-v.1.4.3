[app]

# (str) Title of your application
title = UT Kasir Kita

# (str) Package name
package.name = utkasir

# (str) Package domain (needed for android/ios packaging)
package.domain = org.kasir.kita

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (include icon and presplash image extensions)
source.include_exts = py,png,jpg,kv,atlas,ttf,db

# (str) Application versioning
version = 1.4.3

# (list) Application requirements
# Python, Kivy, Pillow (gambar), SQLite3
requirements = python3,kivy,pillow,sqlite3

# (str) Custom source folders for requirements
# (str) Presplash of the application
presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

#
# Android specific
#

# (list) Permissions
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use
android.ndk_api = 24

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded)
# android.ndk_path =

# (list) List of architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enable Android auto backup feature (API >= 23)
android.allow_backup = True

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# android.arch = arm64-v8a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = disable, 1 = enable)
warn_on_root = 1
