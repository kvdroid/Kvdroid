from kvdroid.jclass.android.webkit import CookieManager


def get_cookies(site_name: str):
    cookieManager = CookieManager.getInstance()
    return cookieManager.getCookie(site_name)
