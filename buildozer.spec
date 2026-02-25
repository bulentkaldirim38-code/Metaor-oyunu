[app]
title = Meteor Hunter
package.name = meteorhunter
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,ttf,wav
version = 1.0

# Pygame reçetesi (recipe) sdl2 kütüphanelerini otomatik çeker. 
# Manuel eklemek bazen çakışma yaratır ancak ttf ve image modülleri bazen eksik kalabiliyor.
requirements = python3, pygame, sdl2_image, sdl2_ttf

# KRİTİK DÜZELTME: Sondaki nokta silindi, izinler temizlendi.
android.permissions = INTERNET

orientation = portrait
fullscreen = 1

# Android API ve Build Ayarları
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
