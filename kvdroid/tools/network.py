from kvdroid.jclass.android import Activity
from kvdroid import activity


def network_status():
    from kvdroid.jclass.android import ConnectivityManager
    ConnectivityManager = ConnectivityManager()
    con_mgr = activity.getSystemService(Activity().CONNECTIVITY_SERVICE)
    try:
        wifi = con_mgr.getNetworkInfo(ConnectivityManager.TYPE_WIFI).isConnectedOrConnecting()
        mobile = con_mgr.getNetworkInfo(ConnectivityManager.TYPE_MOBILE).isConnectedOrConnecting()
        return wifi or mobile
    except:
        return False


network_state = network_status()
