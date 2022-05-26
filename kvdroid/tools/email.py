from kvdroid import activity

from kvdroid.jclass.java import File

from kvdroid.jclass.android import Intent, Uri


def send_email(recipient: str, subject: str, body: str, file_path: str = None,
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
    email_intent = Intent(Intent().ACTION_SEND)
    email_intent.setType(mime_type)
    email_intent.putExtra(Intent().EXTRA_EMAIL, [recipient])
    email_intent.putExtra(Intent().EXTRA_SUBJECT, subject)
    email_intent.putExtra(Intent().EXTRA_TEXT, body)
    if file_path:
        file = File(file_path)
        if not file.exists() or not file.canRead():
            return
        uri = Uri().fromFile(file)
        email_intent.putExtra(Intent().EXTRA_STREAM, uri)
    if create_chooser:
        activity.startActivity(Intent().createChooser(email_intent, "Pick an Email provider"))
    else:
        activity.startActivity(email_intent)
