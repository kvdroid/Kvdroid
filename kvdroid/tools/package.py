from kvdroid import activity
from kvdroid.jclass.android import ApplicationInfo, PackageManager, ComponentName, VERSION
from kvdroid.jclass.java import File


def all_packages():
    pkgAppsList = activity.getPackageManager().getInstalledPackages(0)
    package_list = []
    for i in range(pkgAppsList.size()):
        package = pkgAppsList.get(i).applicationInfo
        package_list.append(package.packageName)
    return package_list


def all_main_activities():
    from kvdroid.jclass.android import Intent
    mainIntent = Intent(Intent().ACTION_MAIN)
    mainIntent.addCategory(Intent().CATEGORY_LAUNCHER)
    pkgAppsList = activity.getPackageManager().queryIntentActivities(mainIntent, 0)
    activity_list = []
    for i in range(pkgAppsList.size()):
        package = pkgAppsList.get(i).activityInfo
        activity_list.append({package.packageName: package.name})
    return activity_list


def is_system_package(package):
    pManager = activity.getPackageManager()
    package = pManager.getApplicationInfo(
        package, PackageManager().GET_META_DATA)
    if (package.flags & (ApplicationInfo().FLAG_SYSTEM | ApplicationInfo().FLAG_UPDATED_SYSTEM_APP)) != 0:
        return True
    else:
        return False

    
def is_package_enabled(package):
    pManager = activity.getPackageManager()
    return pManager.getApplicationInfo(package, 0).enabled


def is_package_installed(package):
    pManager = activity.getPackageManager()
    try:
        pManager.getApplicationInfo(package, 0)
        return True
    except:
        return False


def package_source(package):
    installer = activity.getPackageManager().getInstallerPackageName(package)
    if installer == "com.android.vending":
        return "playstore"
    else:
        return "unknown"


def package_info(package):
    pManager = activity.getPackageManager()
    appInfo = pManager.getPackageInfo(package, 0)
    installTime = appInfo.firstInstallTime
    updateTime = appInfo.lastUpdateTime
    if VERSION().SDK_INT >= 28:
        versionCode = appInfo.getLongVersionCode()
    versionName = appInfo.versionName
    targetSdkVersion = appInfo.applicationInfo.targetSdkVersion
    minSdkVersion = appInfo.applicationInfo.minSdkVersion
    enabled = is_package_enabled(package)    
    application = pManager.getApplicationInfo(
        package, PackageManager().GET_META_DATA)
    applicationName=pManager.getApplicationLabel(pManager.getApplicationInfo(package, pManager.GET_META_DATA))
    size = File(application.publicSourceDir).length()
    loadLabel = application.loadLabel(pManager)
    loadIcon = application.loadIcon(pManager)
    packageName = application.packageName
    sourceDir = application.sourceDir
    dataDir = application.dataDir
    processName = application.processName
    publicSourceDir = application.publicSourceDir
    sharedLibraryFiles = application.sharedLibraryFiles
    packagePerms = pManager.getPackageInfo(
        packageName, PackageManager().GET_PERMISSIONS)
    requestedPermissions = packagePerms.requestedPermissions
    permissions = []
    if requestedPermissions != None:
        for i in range(len(requestedPermissions)):
            permissions.append(requestedPermissions[i])
    activities = []
    activity_list = pManager.getPackageInfo(
        packageName, PackageManager().GET_ACTIVITIES).activities
    if activity_list:
        for act in activity_list:
            activities.append(act.name)
    infos = {"packageName": packageName,
             "applicationName":applicationName,
            "loadLabel": loadLabel,
            "loadIcon": loadIcon,
            "sourceDir": sourceDir,
            "dataDir": dataDir,
            "processName": processName,
            "publicSourceDir": publicSourceDir,
            "sharedLibraryFiles": sharedLibraryFiles,
            "installTime": installTime,
            "updateTime": updateTime,
            "versionName": versionName,
            "versionCode": versionCode,
            "targetSdkVersion": targetSdkVersion,
            "minSdkVersion": minSdkVersion,
            "permissions": permissions,
            "activities": activities,
            "enabled": enabled,
            "size": size
            }
    return infos

    
def is_activity_exported(package, act):
    component = ComponentName(package, act)
    activityInfo = activity.getPackageManager().getActivityInfo(
        component, PackageManager().MATCH_DEFAULT_ONLY)
    if activityInfo != None and activityInfo.exported:
        return True
    else:
        return False


def activity_info(package, act):
    pManager = activity.getPackageManager()
    component = ComponentName(package, act)
    activityInfo = activity.getPackageManager().getActivityInfo(
        component, PackageManager().GET_META_DATA)
    loadLabel = activityInfo.loadLabel(pManager)
    loadIcon = activityInfo.loadIcon(pManager)
    exported = is_activity_exported(package,act)
    infos = {
        "loadLabel": loadLabel,
        "loadIcon": loadIcon,
        "exported": exported
    }
    return infos
