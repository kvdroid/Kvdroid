from kvdroid import activity


def app_source():
    packageName = activity.getPackageName()
    installer = activity.getPackageManager().getInstallerPackageName(packageName)
    return "playstore" if installer == "com.android.vending" else "unknown"


def app_info(info: str):
    infos = {
        "name": activity.getApplicationInfo().loadLabel(activity.getPackageManager()),
        "package": activity.getApplicationContext().getPackageName(),
        "version_name": activity.getPackageManager().getPackageInfo(activity.getPackageName(), 0).versionName,
        "version_code": activity.getPackageManager().getPackageInfo(activity.getPackageName(), 0).versionCode
    }
    return infos.get(info)


def app_dirs(directory: str):
    dirs = {
        "files": activity.getFilesDir().getAbsolutePath(),
        "cache": activity.getCacheDir().getAbsolutePath(),
        "app": f"{activity.getFilesDir().getAbsolutePath()}/app",
        "ext_files": activity.getExternalFilesDir(None).getAbsolutePath(),
        "ext_cache": activity.getExternalCacheDir().getAbsolutePath(),
        "data": activity.getFilesDir().getParent(),
    }
    return dirs[directory] if directory in dirs else None
