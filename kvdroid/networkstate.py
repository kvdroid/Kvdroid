from kvdroid import ConnectivityManager, activity, AndroidActivity


def network_state():
    con_mgr = activity.getSystemService(AndroidActivity.CONNECTIVITY_SERVICE)
    conn = con_mgr.getNetworkInfo(ConnectivityManager.TYPE_WIFI).isConnectedOrConnecting()
    try:
        if conn:
            return True
        conn = con_mgr.getNetworkInfo(ConnectivityManager.TYPE_MOBILE).isConnectedOrConnecting()
        return bool(conn)
    except:
        return False


network_state = network_state()
