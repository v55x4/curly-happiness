[app]
title = Sakkak Premium
package.name = sakkakapp
package.domain = org.sakkak
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.1.0,kivymd,sqlite3,pillow
orientation = portrait
fullscreen = 0
android.arch = armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
