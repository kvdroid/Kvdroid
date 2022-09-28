from kvdroid.jclass.android import Uri, Intent, CallLogCalls
from kvdroid import activity
from datetime import datetime

get_date = datetime.fromtimestamp


def make_call(tel):
    intent = Intent(Intent().ACTION_CALL, Uri().parse(f"tel:{tel}"))
    activity.startActivity(intent)


def dial_call(tel):
    intent = Intent(Intent().ACTION_DIAL, Uri().parse(f"tel:{tel}"))
    activity.startActivity(intent)


def get_call_log(content_resolver=activity.getContentResolver()):
    # sourcery skip: use-named-expression
    Calls = CallLogCalls()
    cursor = content_resolver.query(Calls.CONTENT_URI, None, None, None, None)
    if cursor:
        total_log = cursor.getCount()
        call_logs = []
        call_logs_type = {1: "incoming", 2: "outgoing", 3: "missed", 4: "voicemail", 5: "rejected", 6: "blocked"}
        try:
            while cursor.moveToNext():
                call_logs.append({
                    "date": get_date(float(cursor.getString(cursor.getColumnIndexOrThrow(Calls.DATE))) / 1000),
                    "name": cursor.getString(cursor.getColumnIndexOrThrow(Calls.CACHED_NAME)),
                    "number": cursor.getString(cursor.getColumnIndexOrThrow(Calls.NUMBER)),
                    "duration": cursor.getString(cursor.getColumnIndexOrThrow(Calls.DURATION)),
                    "type": call_logs_type[cursor.getInt(cursor.getColumnIndexOrThrow(Calls.TYPE))]
                })
        finally:
            cursor.close()
        return total_log, call_logs
    return
