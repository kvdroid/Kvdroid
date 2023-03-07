from kvdroid.jclass.android import Activity
from kvdroid import activity
from jnius import JavaException, cast
from kvdroid.jclass.android import WifiManager, Formatter, Context


def network_status() -> bool:
    """
    Checks if Mobile data or Wi-Fi network is connected

    :rtype: bool
    :return: network status
    """
    return bool(wifi_status() or mobile_status())


def wifi_status() -> bool:
    """
    Checks if th phone Wi-Fi is connected to any network

    :rtype: bool
    :return: Wi-Fi status
    """
    from kvdroid.jclass.android import ConnectivityManager
    ConnectivityManager = ConnectivityManager()
    con_mgr = activity.getSystemService(Activity().CONNECTIVITY_SERVICE)
    try:
        return con_mgr.getNetworkInfo(ConnectivityManager.TYPE_WIFI).isConnectedOrConnecting()
    except JavaException:
        return False


def mobile_status() -> bool:
    """
    Checks if Mobile data is connected

    :rtype: bool
    :return: Mobile data status
    """
    from kvdroid.jclass.android import ConnectivityManager
    ConnectivityManager = ConnectivityManager()
    con_mgr = activity.getSystemService(Activity().CONNECTIVITY_SERVICE)
    try:
        return con_mgr.getNetworkInfo(ConnectivityManager.TYPE_MOBILE).isConnectedOrConnecting()
    except JavaException:
        return False


def get_wifi_ip_address() -> str:
    """
    Gets the Wi-Fi IP Address. But when the Wi-Fi is off, it
    returns a string value of "0.0.0.0"

    :rtype: str
    :return: Wi-Fi Ip Address
    """
    formatter = Formatter()
    context = activity.getApplicationContext()
    wifi_manager = cast(WifiManager(), context.getSystemService(Context().WIFI_SERVICE))
    return formatter.formatIpAddress(wifi_manager.getConnectionInfo().getIpAddress())


def network_latency() -> float:
    import time
    from kvdroid.jclass.java import InetAddress
    InetAddress = InetAddress()
    def ping(host):
        start_time = time.time()
        address = InetAddress.getByName(host)
        if address.isReachable(1000):
            end_time = time.time()
            return (end_time - start_time) * 1000
        else:
            return None
    return ping('google.com')


def get_wifi_signal() -> float:
    wm = activity.getSystemService(activity.WIFI_SERVICE)
    wifi_info = wm.getConnectionInfo()
    signal_strength = wifi_info.getRssi()
    if signal_strength < -100:
        signal_percent = 0.0
    else:
        signal_percent = 100.0 * (signal_strength + 100) / 200.0
    return signal_percent