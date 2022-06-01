from kvdroid.jclass.android import PackageManager

from kvdroid import activity

context = activity.getApplicationContext()


def grant_uri_permission(intent, uri, permissions):
    packageManager = context.getPackageManager()
    activities = packageManager.queryIntentActivities(intent, PackageManager().MATCH_DEFAULT_ONLY)
    activities = activities.toArray()
    for resolveInfo in activities:
        packageName = resolveInfo.activityInfo.packageName
        context.grantUriPermission(packageName, uri, permissions)


def revoke_uri_permission(uri, permissions):
    context.revokeUriPermission(uri, permissions)
