[app]
title = Meteor Hunter
package.name = meteorhunter
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,ttf,wav
version = 1.0

# Pygame reçetesi (recipe) sdl2 kütüphanelerini otomatik çeker. 
# Manuel eklemek bazen çakışma yaratır.
requirements = python3, pygame

# KRİTİK DÜZELTME: Sondaki nokta silindi, izinler temizlendi.
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

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
