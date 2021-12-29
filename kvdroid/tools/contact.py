from kvdroid import activity


def get_contact_details(option: str = "phone_book"):
    from kvdroid.jclass.android import Phone
    Phone = Phone()
    """
    option accepts this values : "phone_book", "mobile_no", "names"

    :param option: str: used to determine the return value
    :return: value
    """
    value = None
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
                        phone_book[name] = [number]
                    mobile_no_set.append(number)
        finally:
            cursor.close()

        if option == "mobile_no":
            value = mobile_no_set
        elif option == "names":
            value = list(phone_book.keys())
        elif option == "phone_book":
            value = phone_book
        else:
            raise TypeError("available options are ['names', 'mobile_no', 'phone_book'] for get_contact_details")
    return value
