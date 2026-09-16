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
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,sqlite3


# --------------------------------------------------
# Python-for-Android
# --------------------------------------------------
# Pin to stable release branch (uses Python 3.11.5 and Kivy 2.3.0)
p4a.branch = release-2024.01.21


# --------------------------------------------------
# Screen
# --------------------------------------------------
orientation = portrait

fullscreen = 0


# --------------------------------------------------
# Android
# --------------------------------------------------

# Target Android API
android.api = 33

# Minimum Android API
android.minapi = 21

# Android NDK
android.ndk = 25b

# Architectures
android.archs = arm64-v8a


# --------------------------------------------------
# Android permissions
# --------------------------------------------------
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE


# --------------------------------------------------
# Automatically accept Android SDK licenses
# --------------------------------------------------
android.accept_sdk_license = True


# --------------------------------------------------
# Android application settings
# --------------------------------------------------
android.allow_backup = True

android.debug_artifact = apk


# --------------------------------------------------
# Buildozer
# --------------------------------------------------
[buildozer]

log_level = 2

warn_on_root = 1