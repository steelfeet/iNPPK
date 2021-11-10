[app]
title = iNPPK
package.name = iNPPK
package.domain = ru.iNPPK
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 0.3.6
#requirements = kivy==master,python3crystax==3.5
requirements = python3,kivy,requests,kivymd,opencv-python,urllib3,charset-normalizer,idna,Pillow,base64
orientation = all
osx.python_version = 3
osx.kivy_version = 2.0.0
fullscreen = 0
#android.presplash_color = #1d3b3e
android.permissions = WRITE_EXTERNAL_STORAGE,INTERNET,CAMERA,READ_EXTERNAL_STORAGE, INTERNET
android.api = 27
android.minapi = 27
android.sdk = 28
#private = False
android.ndk_path = /home/kivy/Android/crystax-ndk-10.3.2/
android.arch = armeabi-v7a
p4a.source_dir = /home/kivy/Repos/python-for-android/
android.logcat_filters = *:S python:D
[buildozer]
log_level = 2
warn_on_root = 1