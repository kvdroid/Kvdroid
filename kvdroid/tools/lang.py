from kvdroid.jclass.java.util import Locale


def device_lang(option = "Language"):
    locale = Locale().getDefault()
    options = {
        "Language" : locale.getLanguage() , 
        "ISO3Language" : locale.getISO3Language() ,
        "Country" : locale.getCountry() ,
        "ISO3Country" : locale.getISO3Country() ,
        "DisplayCountry" : locale.getDisplayCountry() ,
        "DisplayName" : locale.getDisplayName() ,
        "String" : locale.toString() ,
        "DisplayLanguage" : locale.getDisplayLanguage() ,
        "LanguageTag" : locale.toLanguageTag() }

    if option not in options.keys():
        raise ValueError(f"Invalid option. Expected one of: {list(options.keys())}")
    else:
        return options[str(option)]
