[app]

title = Gym Registration
package.name = gymregister
package.domain = com.gymapp

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,db

version = 1.0

requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow

orientation = portrait

fullscreen = 0

# Python-for-Android
p4a.fork = kivy
p4a.branch = master
p4a.commit = 58d2114

# Android
android.api = 33
android.minapi = 21
android.ndk = 25b

android.archs = arm64-v8a,armeabi-v7a

android.permissions = INTERNET

android.allow_backup = True

android.debug_artifact = apk


[buildozer]

log_level = 2
warn_on_root = 1