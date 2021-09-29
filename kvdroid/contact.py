from kvdroid import activity
from kvdroid import Phone


def get_contact_details():
    PROJECTION = ["contact_id", "display_name", Phone.NUMBER]
    cr = activity.getContentResolver()
    cursor = cr.query(Phone.CONTENT_URI, PROJECTION, None, None, "display_name" + " ASC")
    mobile_no_set: list = []
    phone_book: dict = {}
    if cursor:
        try:
            name_index: int = cursor.getColumnIndex("display_name")
            number_index: int = cursor.getColumnIndex(Phone.NUMBER)

            while cursor.moveToNext():
                name = cursor.getString(name_index)
                number = cursor.getString(number_index)
                number = number.replace(" ", "")
                if number not in mobile_no_set:
                    if name in phone_book:
                        phone_book[name].append(number)
                    else:
                        phone_book.update({name: [number]})
                    mobile_no_set.append(number)
        finally:
            cursor.close()
    return phone_book


def get_contact_names():
    return list(get_contact_details().keys())


def get_contact_numbers():
    return list(get_contact_details().values())
