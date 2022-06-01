from typing import List

from kvdroid.tools import toast
from kvdroid.cast import cast_object

from kvdroid import activity
from kvdroid.jclass.java import File, String
from kvdroid.jclass.android import Intent, VERSION
from kvdroid.jclass.androidx import FileProvider
from kvdroid.tools.uri import grant_uri_permission

context = activity.getApplicationContext()


def send_email(recipient: List[str], subject: str, body: str, file_path: str = None,
               create_chooser: bool = False, mime_type: str = "message/rfc822",
               authority: str = f"{context.getPackageName()}.fileprovider") -> None:
    """
    This method will open any default or selected email app and sends a body of message
    with or without an attachment depending on the chosen argument

    :param authority: file provider authority name
    :param recipient: email address of the receiver
    :param subject: subject of the email
    :param body: body of the email
    :param file_path: file path of the attachment to be sent (default is None)
    :param create_chooser: whether to create an option to choose a specific app for sending email
    :param mime_type: body text type (defaults to "text/plain")
    :rtype: None
    """
    if VERSION().SDK_INT >= 24:
        from kvdroid.jclass.android import StrictMode
        StrictMode().disableDeathOnFileUriExposure()
    uri = None
    email_intent = Intent(Intent().ACTION_SEND)
    email_intent.setType(mime_type)
    email_intent.putExtra(Intent().EXTRA_EMAIL, recipient)
    email_intent.putExtra(Intent().EXTRA_SUBJECT, String(subject))
    email_intent.putExtra(Intent().EXTRA_TEXT, String(body))
    email_intent.addFlags(Intent().FLAG_GRANT_READ_URI_PERMISSION | Intent().FLAG_GRANT_WRITE_URI_PERMISSION)
    if file_path:
        file = File(file_path)
        if not file.exists() or not file.canRead():
            toast(f"{file_path} does not exist")
            return
        uri = FileProvider().getUriForFile(activity, authority, file)
        parcelable = cast_object('parcelable', uri)
        email_intent.setDataAndType(uri, activity.getContentResolver().getType(uri))
        email_intent.putExtra(Intent().EXTRA_STREAM, parcelable)
    if create_chooser:
        chooser_intent = Intent().createChooser(
            email_intent, cast_object("charSequence", String("Pick an Email Provider")))
        if file_path:
            grant_uri_permission(chooser_intent, uri,
                                 Intent().FLAG_GRANT_WRITE_URI_PERMISSION |
                                 Intent().FLAG_GRANT_READ_URI_PERMISSION)
        activity.startActivity(chooser_intent)
    else:
        email_intent.setClassName('com.google.android.gm', 'com.google.android.gm.ComposeActivityGmailExternal')
        if file_path:
            context.grantUriPermission(String('com.google.android.gm'), uri,
                                       Intent().FLAG_GRANT_WRITE_URI_PERMISSION |
                                       Intent().FLAG_GRANT_READ_URI_PERMISSION)
        activity.startActivity(email_intent)
