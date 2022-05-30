from typing import List

from kvdroid.cast import cast_object

from kvdroid import activity
from kvdroid.jclass.java import File, String
from kvdroid.jclass.android import Intent, Uri, VERSION


def send_email(recipient: List[str], subject: str, body: str, file_path: str = None,
               create_chooser: bool = False, mime_type: str = "text/plain") -> None:
    """
    This method will open any default or selected email app and sends a body of message
    with or without an attachment depending on the chosen argument

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
    email_intent = Intent(Intent().ACTION_SEND)
    email_intent.setType(mime_type)
    email_intent.putExtra(Intent().EXTRA_EMAIL, recipient)
    email_intent.putExtra(Intent().EXTRA_SUBJECT, String(subject))
    email_intent.putExtra(Intent().EXTRA_TEXT, String(body))
    if file_path:
        file = File(file_path)
        if not file.exists() or not file.canRead():
            return
        uri = Uri().fromFile(file)
        parcelable = cast_object('parcelable', uri)
        email_intent.putExtra(Intent().EXTRA_STREAM, parcelable)
    if create_chooser:
        activity.startActivity(Intent().createChooser(email_intent, "Pick an Email provider"))
    else:
        email_intent.setClassName('com.google.android.gm', 'com.google.android.gm.ComposeActivityGmailExternal')
        activity.startActivity(email_intent)
