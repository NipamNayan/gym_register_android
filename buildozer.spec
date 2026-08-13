[app]

# App metadata
title = Gym Registration
package.name = gymregister
package.domain = com.gymapp

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db

version = 1.0

# kivy/kivymd only — python3 and sqlite3 are runtime builtins, not pip packages
requirements = kivy==2.3.0,kivymd==1.2.0,pillow

# Android orientation
orientation = portrait

# Target Android API
android.api = 33
android.minapi = 21
android.ndk = 25b

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# Auto-accept Android SDK licenses during build
android.accept_sdk_license = True

# Architecture (arm64-v8a covers all modern phones; add armeabi-v7a for older)
android.archs = arm64-v8a, armeabi-v7a

# Fullscreen (0 = show status bar, which is friendlier)
fullscreen = 0

# Log level: 2 = info
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1
