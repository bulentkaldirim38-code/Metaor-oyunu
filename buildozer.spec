[app]
title = Meteor Hunter
package.name = meteorhunter
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,ttf,wav
version = 1.0

# Gerekli kütüphaneler (Pygame için en güvenli liste)
requirements = python3, pygame, sdl2_image, sdl2_ttf, sdl2_mixer, hostpython3

# İzinler
android.permissions = INTERNET, VIBRATE

orientation = portrait
fullscreen = 1

# Android API Ayarları
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
