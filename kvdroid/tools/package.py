from kvdroid import activity
from kvdroid.jclass.android import ApplicationInfo, PackageManager, ComponentName


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
    if ((package.flags & (ApplicationInfo().FLAG_SYSTEM | ApplicationInfo().FLAG_UPDATED_SYSTEM_APP)) != 0):
        return True
    else:
        return False

    
def is_package_enabled(package):
    pManager = activity.getPackageManager()
    return pManager.getApplicationInfo(package,0).enabled


def package_source(package):
    installer = activity.getPackageManager().getInstallerPackageName(package)
    if installer == "com.android.vending":
        return "playstore"
    else:
        return "unknown"


def package_info(package):
    pManager = activity.getPackageManager()
    package = pManager.getApplicationInfo(
        package, PackageManager().GET_META_DATA)
    loadLabel = package.loadLabel(pManager)
    loadIcon = package.loadIcon(pManager)
    packageName = package.packageName
    sourceDir = package.sourceDir
    dataDir = package.dataDir
    processName = package.processName
    publicSourceDir = package.publicSourceDir
    sharedLibraryFiles = package.sharedLibraryFiles
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
             "loadLabel": loadLabel,
             "loadIcon": loadIcon,
             "sourceDir": sourceDir,
             "dataDir": dataDir,
             "processName": processName,
             "publicSourceDir": publicSourceDir,
             "sharedLibraryFiles": sharedLibraryFiles,
             "permissions": permissions,
             "activities": activities
             }
    return infos


def activity_info(package, act):
    pManager = activity.getPackageManager()
    component = ComponentName(package, act)
    activityInfo = activity.getPackageManager().getActivityInfo(
        component, PackageManager().GET_META_DATA)
    loadLabel = activityInfo.loadLabel(pManager)
    loadIcon = activityInfo.loadIcon(pManager)
    infos = {
        "loadLabel": loadLabel,
        "loadIcon": loadIcon
    }
    return infos
