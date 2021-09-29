from kvdroid import CookieManager


def get_cookies(site_name: str):
    cookieManager = CookieManager.getInstance()
    cookies = cookieManager.getCookie(site_name)
    return cookies
