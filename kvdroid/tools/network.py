from kvdroid.jclass.android.app import AndroidActivity
from kvdroid.jclass.android.net import ConnectivityManager
from kvdroid import activity


def network_status():
    con_mgr = activity.getSystemService(AndroidActivity.CONNECTIVITY_SERVICE)
    conn = con_mgr.getNetworkInfo(ConnectivityManager.TYPE_WIFI).isConnectedOrConnecting()
    try:
        if conn:
            return True
        conn = con_mgr.getNetworkInfo(ConnectivityManager.TYPE_MOBILE).isConnectedOrConnecting()
        return bool(conn)
    except:
        return False


network_state = network_status()
