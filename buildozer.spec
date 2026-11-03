[app]
p4a.branch = master
# (str) Title of your application
title = Virus Scanner Pro

# (str) Package name
package.name = virusscanner

# (str) Package domain
package.domain = org.yourname

# (str) Source code location
source.dir = .

# (str) Version of your application
version = 1.0

# (list) Application requirements
requirements = python3,kivy,requests

# (list) Permissions requested from the android manifest
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET

# (str) Orientation of the application
orientation = portrait
android.api = 33
android.minapi = 23
android.ndk = 25b
android.archs = arm64-v8a

# (list) Application services to use
services =

# (list) Application recipes to use
recipe.android =
