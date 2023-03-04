from kvdroid import activity


def app_source():
    packageName = activity.getPackageName()
    installer = activity.getPackageManager().getInstallerPackageName(packageName)
    if installer == "com.android.vending":
        return "playstore"
    else:
        return "unknown"


def app_info(info: str):
    infos = {
        "name": activity.getApplicationInfo().loadLabel(activity.getPackageManager()),
        "package": activity.getApplicationContext().getPackageName(),
        "version_name": activity.getPackageManager().getPackageInfo(activity.getPackageName(), 0).versionName,
        "version_code": activity.getPackageManager().getPackageInfo(activity.getPackageName(), 0).versionCode
        }
    if info in infos.keys():
        return infos[info]
    else:
        return None



def app_dirs(directory: str, slash: bool = False):
    dirs = {
        "files": activity.getFilesDir().getAbsolutePath(),
        "cache": activity.getCacheDir().getAbsolutePath(),
        "app": activity.getFilesDir().getAbsolutePath() + "/app",
        "ext_files": activity.getExternalFilesDir(None).getAbsolutePath(),
        "ext_cache": activity.getExternalCacheDir().getAbsolutePath(),
        "data": activity.getFilesDir().getParent()
        }
    if directory in dirs.keys():
        return dirs[directory] + ("/" if slash else "")
    else:
        return None