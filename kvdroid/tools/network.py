from kvdroid.jclass.android import Activity
from kvdroid import activity


def network_status():
    if wifi_status() or mobile_status():
        return True
    else:
        return False
            
def wifi_status():
    from kvdroid.jclass.android import ConnectivityManager
    ConnectivityManager = ConnectivityManager()
    con_mgr = activity.getSystemService(Activity().CONNECTIVITY_SERVICE)
    try:
        return con_mgr.getNetworkInfo(ConnectivityManager.TYPE_WIFI).isConnectedOrConnecting()
    except:
        return False
            
def mobile_status():
    from kvdroid.jclass.android import ConnectivityManager
    ConnectivityManager = ConnectivityManager()
    con_mgr = activity.getSystemService(Activity().CONNECTIVITY_SERVICE)
    try:
        return con_mgr.getNetworkInfo(ConnectivityManager.TYPE_MOBILE).isConnectedOrConnecting()
    except:
        return False
