[app]

# Application title
title = USB Connector Info

# Package name
package.name = usbconnector

# Package domain
package.domain = org.vincentmes

# Source files
source.dir = .

# Source includes
source.include_exts = py,png,jpg,kv,atlas,txt

# Version
version = 1.0

# Application requirements
requirements = python3,kivy

# Supported orientations
orientation = portrait

# Icon
# icon.filename = %(source.dir)s/data/icon.png

# Fullscreen
fullscreen = 0

# Android specific
[buildozer]

# Log level
log_level = 2

# Display warning
warn_on_root = 1

# Android SDK
android.api = 31
android.minapi = 21
android.ndk = 25b

# Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Features
android.features = 

# Meta-data
android.meta_data = 

# Gradle dependencies
# android.gradle_dependencies = 

# Java classes
# android.add_src = 

# Arch
android.archs = arm64-v8a

# Bootstrap
p4a.bootstrap = sdl2
p4a.local_recipes = ./recipes

# Build
android.release_artifact = apk
