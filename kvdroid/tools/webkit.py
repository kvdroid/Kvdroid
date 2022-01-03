from kvdroid.jclass.android.webkit import CookieManager


def get_cookies(site_name: str):
    cookieManager = CookieManager().getInstance()
    return cookieManager.getCookie(site_name)


def launch_url(url: str, color="#FFFFFF", color_scheme="system"):
    from kvdroid.jclass.android.graphics import Color
    from kvdroid.jclass.androidx.browser.customtabs import CustomTabColorSchemeParamsBuilder
    from kvdroid.jclass.androidx.browser.customtabs import CustomTabsIntentBuilder, CustomTabsIntent
    from kvdroid import activity
    from kvdroid.jclass.android.net import Uri
    CustomTabsIntent = CustomTabsIntent()
    schemes = {
        "system": CustomTabsIntent.COLOR_SCHEME_SYSTEM,
        "light": CustomTabsIntent.COLOR_SCHEME_LIGHT,
        "dark": CustomTabsIntent.COLOR_SCHEME_DARK
    }
    color_int = Color().parseColor(color)
    default_color = CustomTabColorSchemeParamsBuilder(instantiate=True).setToolbarColor(color_int).build()
    builder = CustomTabsIntentBuilder(instantiate=True)
    if color_scheme not in schemes:
        builder.setColorScheme(CustomTabsIntent.COLOR_SCHEME_SYSTEM)
    else:
        builder.setColorScheme(schemes[color_scheme])
    builder.setDefaultColorSchemeParams(default_color)
    custom_tabs_intent = builder.build()
    custom_tabs_intent.intent.setPackage("com.android.chrome")
    custom_tabs_intent.launchUrl(activity, Uri().parse(url))
