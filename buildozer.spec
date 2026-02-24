[app]
title = Meteor Hunter
package.name = meteorhunter
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,ttf
version = 1.0

requirements = python3,pygame,sdl2,sdl2_image,sdl2_mixer,sdl2_ttf
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE.
orientation = portrait
fullscreen = 1

# Android API ayarları
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# P4A (Python for Android) ayarı
p4a.bootstrap = sdl2
