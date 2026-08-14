[app]

# --------------------------------------------------
# Application
# --------------------------------------------------
title = Gym Registration
package.name = gymregister
package.domain = com.gymapp

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,db,json

version = 1.0

# --------------------------------------------------
# Python / Kivy dependencies
# --------------------------------------------------
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow

# --------------------------------------------------
# Python-for-Android
# --------------------------------------------------
p4a.fork = kivy
p4a.branch = master

# --------------------------------------------------
# Screen
# --------------------------------------------------
orientation = portrait
fullscreen = 0

# --------------------------------------------------
# Android
# --------------------------------------------------
android.api = 33
android.minapi = 21
android.ndk = 25b

android.archs = arm64-v8a,armeabi-v7a

# --------------------------------------------------
# Permissions
# --------------------------------------------------
android.permissions = INTERNET

# --------------------------------------------------
# Android application settings
# --------------------------------------------------
android.allow_backup = True

# Build debug APK
android.debug_artifact = apk


[buildozer]

# --------------------------------------------------
# Buildozer
# --------------------------------------------------
log_level = 2
warn_on_root = 1