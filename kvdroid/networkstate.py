from kvdroid import ConnectivityManager, con_mgr


def network_state():
    conn = con_mgr.getNetworkInfo(ConnectivityManager.TYPE_WIFI).isConnectedOrConnecting()
    try:
        if conn:
            return True
        else:
            conn = con_mgr.getNetworkInfo(ConnectivityManager.TYPE_MOBILE).isConnectedOrConnecting()
            if conn:
                return True
            else:
                return False
    except:
         return False
network_state = network_state()
