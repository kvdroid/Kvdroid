from jnius import autoclass

URLConnection = autoclass("java.net.URLConnection")
HttpURLConnection = autoclass("java.net.HttpURLConnection")
URL = autoclass("java.net.URL")
