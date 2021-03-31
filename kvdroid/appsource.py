from kvdroid import activity


def app_source():
    packageName = activity.getPackageName()
    installer = activity.getPackageManager().getInstallerPackageName(packageName)
    if installer == "com.android.vending":
        return "playstore"
    else:
        return "unknown"


app_source = app_source()
