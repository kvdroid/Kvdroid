from kvdroid import activity
from kvdroid.jclass.android import TelephonySms
from datetime import datetime

get_date = datetime.fromtimestamp


def get_all_sms(content_resolver=activity.getContentResolver()):
    # sourcery skip: use-named-expression
    Sms = TelephonySms()
    cursor = content_resolver.query(Sms.CONTENT_URI, None, None, None, None)
    if cursor:
        total_sms = cursor.getCount()
        messages = []
        sms_types = {0: "all", 1: "inbox", 2: "sent", 3: "draft", 4: "outbox", 5: "failed", 6: "queued"}
        try:
            while cursor.moveToNext():
                messages.append({
                    "date": get_date(float(cursor.getString(cursor.getColumnIndexOrThrow("date"))) / 1000),
                    "number": cursor.getString(cursor.getColumnIndexOrThrow("address")),
                    "body": cursor.getString(cursor.getColumnIndexOrThrow("body")),
                    "type": sms_types[cursor.getInt(cursor.getColumnIndexOrThrow("type"))]
                })
        finally:
            cursor.close()
        return total_sms, messages
    return
