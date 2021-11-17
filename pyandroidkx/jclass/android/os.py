from jnius import autoclass

Environment = autoclass("android.os.Environment")
Build = autoclass("android.os.Build")
VERSION = autoclass('android.os.Build$VERSION')
VERSION_CODES = autoclass("android.os.Build$VERSION_CODES")
StrictMode = autoclass('android.os.StrictMode')
StatFs = autoclass("android.os.StatFs")
BatteryManager = autoclass("android.os.BatteryManager")
