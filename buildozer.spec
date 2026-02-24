[app]

# (str) Title of your application
title = Meteor Hunter

# (str) Package name
package.name = meteorhunter

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (Görseller ve yazı tipleri dahil)
source.include_exts = py,png,jpg,ttf,wav,json

# (str) Application versioning
version = 1.0

# (list) Application requirements
# Pygame reçetesi sdl2 kütüphanelerini otomatik olarak çeker.
requirements = python3,pygame

# (list) Permissions 
# KRİTİK DÜZELTME: Satır sonundaki noktayı sildik.
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (list) Supported orientations
orientation = portrait

# (bool) Fullscreen or not
fullscreen = 1

# --- Android Spesifik Ayarlar ---

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android NDK directory (empty = auto download)
android.ndk_path = 

# (str) Android SDK directory (empty = auto download)
android.sdk_path = 

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (str) Bootstrap to use for android builds
# Pygame için sdl2 kullanılmalıdır.
p4a.bootstrap = sdl2

[buildozer]

# (int) Log level (2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
