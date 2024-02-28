from os.path import join

from jnius import JavaException

from kvdroid.jclass.android import PackageManager, Environment, DocumentsContract, ContentUris, Uri, Intent, \
    MediaStoreAudioMedia, MediaStoreImagesMedia, MediaStoreVideoMedia, MediaStoreFiles
from kvdroid.jclass.java import Long
from kvdroid.tools.path import sdcard, get_storage_volumes
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


def resolve_uri(uri):
    """
    Resolve URI input from ``android.app.Activity.onActivityResult()``.
    """

    uri_authority = uri.getAuthority()
    uri_scheme = uri.getScheme().lower()

    path = None
    file_name = None
    selection = None
    downloads = None

    # This does not allow file selected from google photos or gallery
    # or even any other file explorer to work
    # not a document URI, nothing to convert from
    # if not DocumentsContract.isDocumentUri(mActivity, uri):
    #     return path

    if uri_authority == 'com.android.externalstorage.documents':
        return handle_external_documents(uri)

    # in case a user selects a file from 'Downloads' section
    # note: this won't be triggered if a user selects a path directly
    #       e.g.: Phone -> Download -> <some file>
    elif uri_authority == 'com.android.providers.downloads.documents':
        path = downloads = handle_downloads_documents(uri)

    elif uri_authority == 'com.android.providers.media.documents':
        file_name, selection, uri = handle_media_documents(uri)

    # parse content:// scheme to path
    if uri_scheme == 'content' and not downloads:
        try:
            path = parse_content(
                uri=uri, projection=['_data'], selection=selection,
                selection_args=file_name, sort_order=None
            )
        except JavaException:  # handles array error for selection_args
            path = parse_content(
                uri=uri, projection=['_data'], selection=selection,
                selection_args=[file_name], sort_order=None
            )

    # nothing to parse, file:// will return a proper path
    elif uri_scheme == 'file':
        path = uri.getPath()

    return path


def handle_downloads_documents(uri):
    """
    Selection from the system filechooser when using ``Downloads``
    option from menu. Might not work all the time due to:

    1) invalid URI:

    jnius.jnius.JavaException:
        JVM exception occurred: Unknown URI:
        content://downloads/public_downloads/1034

    2) missing URI / android permissions

    jnius.jnius.JavaException:
        JVM exception occurred:
        Permission Denial: reading
        com.android.providers.downloads.DownloadProvider uri
        content://downloads/all_downloads/1034 from pid=2532, uid=10455
        requires android.permission.ACCESS_ALL_DOWNLOADS,
        or grantUriPermission()

    Workaround:
        Selecting path from ``Phone`` -> ``Download`` -> ``<file>``
        (or ``Internal storage``) manually.
    """

    try:
        download_dir = Environment().getExternalStoragePublicDirectory(
            Environment().DIRECTORY_DOWNLOADS
        ).getPath()
        path = parse_content(
            uri=uri,
            projection=["_display_name"],
            selection=None,
            selection_args=None,
            sort_order=None,
        )
        return join(download_dir, path)

    except Exception:
        import traceback
        traceback.print_exc()

    # known locations, differ between machines
    downloads = [
        'content://downloads/public_downloads',
        'content://downloads/my_downloads',

        # all_downloads requires separate permission
        # android.permission.ACCESS_ALL_DOWNLOADS
        'content://downloads/all_downloads'
    ]

    file_id = DocumentsContract().getDocumentId(uri)
    try_uris = [
        ContentUris().withAppendedId(
            Uri().parse(down), Long().valueOf(file_id)
        )
        for down in downloads
    ]

    # try all known Download folder uris
    # and handle JavaExceptions due to different locations
    # for content:// downloads or missing permission
    path = None
    for down in try_uris:
        try:
            path = parse_content(
                uri=down, projection=['_data'],
                selection=None,
                selection_args=None,
                sort_order=None
            )

        except JavaException:
            import traceback
            traceback.print_exc()

        # we got a path, ignore the rest
        if path:
            break

    # alternative approach to Downloads by joining
    # all data items from Activity result
    if not path:
        for down in try_uris:
            try:
                path = parse_content(
                    uri=down, projection=None,
                    selection=None,
                    selection_args=None,
                    sort_order=None,
                    index_all=True
                )

            except JavaException:
                import traceback
                traceback.print_exc()

            # we got a path, ignore the rest
            if path:
                break
    return path


def handle_external_documents(uri):
    """
    Selection from the system filechooser when using ``Phone``
    or ``Internal storage`` or ``SD card`` option from menu.
    """

    file_id = DocumentsContract().getDocumentId(uri)
    file_type, file_name = file_id.split(':')

    primary_storage = sdcard()
    sdcard_storage = get_storage_volumes()

    if type(sdcard_storage) == list:
        sdcard_storage = sdcard_storage[0]

    directory = primary_storage

    if file_type == "primary":
        directory = primary_storage
    elif file_type == "home":
        directory = join(primary_storage, Environment().DIRECTORY_DOCUMENTS)
    elif sdcard_storage and file_type in sdcard_storage:
        directory = sdcard_storage

    return join(directory, file_name)


def handle_media_documents(uri):
    """
    Selection from the system filechooser when using ``Images``
    or ``Videos`` or ``Audio`` option from menu.
    """

    file_id = DocumentsContract().getDocumentId(uri)
    file_type, file_name = file_id.split(':')
    selection = '_id=?'

    if file_type == 'image':
        uri = MediaStoreImagesMedia().EXTERNAL_CONTENT_URI
    elif file_type == 'video':
        uri = MediaStoreVideoMedia().EXTERNAL_CONTENT_URI
    elif file_type == 'audio':
        uri = MediaStoreAudioMedia().EXTERNAL_CONTENT_URI

    # Other file type was selected (probably in the Documents folder)
    else:
        uri = MediaStoreFiles().getContentUri("external")

    return file_name, selection, uri


def parse_content(
        uri, projection, selection, selection_args, sort_order,
        index_all=False
):
    """
    Parser for ``content://`` URI returned by some Android resources.
    """

    result = None
    resolver = activity.getContentResolver()
    read = Intent().FLAG_GRANT_READ_URI_PERMISSION
    write = Intent().FLAG_GRANT_READ_URI_PERMISSION
    persist = Intent().FLAG_GRANT_READ_URI_PERMISSION

    # grant permission for our activity
    activity.grantUriPermission(
        activity.getPackageName(),
        uri,
        read | write | persist
    )

    if not index_all:
        cursor = resolver.query(
            uri, projection, selection,
            selection_args, sort_order
        )

        idx = cursor.getColumnIndex(projection[0])
        if idx != -1 and cursor.moveToFirst():
            result = cursor.getString(idx)
    else:
        result = []
        cursor = resolver.query(
            uri, projection, selection,
            selection_args, sort_order
        )
        while cursor.moveToNext():
            for idx in range(cursor.getColumnCount()):
                result.append(cursor.getString(idx))
        result = '/'.join(result)
    return result
