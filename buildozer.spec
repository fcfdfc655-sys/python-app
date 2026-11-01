[app]
title = Kali Guard Pro
version = 1.0.0
package.name = kaliguard
package.domain = org.kali.guard

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

requirements = python3,kivy,requests,urllib3,certifi

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

android.allow_backup = False

[buildozer]
log_level = 2
warn_on_root = 1
