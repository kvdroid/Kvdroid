from kvdroid.jclass.java.util import Locale


def device_lang(option="Language", display_lang=None):
    locale = Locale().getDefault()
    options = {
        "Language": locale.getLanguage(),
        "ISO3Language": locale.getISO3Language(),
        "Country": locale.getCountry(),
        "ISO3Country": locale.getISO3Country(),
        "DisplayCountry": locale.getDisplayCountry(Locale(str(display_lang))),
        "DisplayName": locale.getDisplayName(Locale(str(display_lang))),
        "String": locale.toString(),
        "DisplayLanguage": locale.getDisplayLanguage(Locale(str(display_lang))),
        "LanguageTag": locale.toLanguageTag()}

    if option not in options.keys():
        raise ValueError(f"Invalid option. Expected one of: {list(options.keys())}")
    else:
        return options[option]


def supported_languages():
    langs = []
    for locale in Locale().getAvailableLocales():
        if locale.getLanguage() not in langs:
            langs.append(locale.getLanguage())
    return langs
