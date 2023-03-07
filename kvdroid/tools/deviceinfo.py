from kvdroid.jclass.android.app import MemoryInfo
from kvdroid.jclass.android import IntentFilter, Intent
from kvdroid.jclass.android import StatFs
from kvdroid.jclass.java import Runtime
from kvdroid import activity


def device_info(text:str="", convert=False):
    from kvdroid.jclass.android import Context, Build, BatteryManager, VERSION, Environment
    Environment = Environment()
    VERSION = VERSION()
    Build = Build()
    BatteryManager = BatteryManager()
    Context = Context()
    bm = activity.getSystemService(Context.BATTERY_SERVICE)
    count = bm.getIntProperty(BatteryManager.BATTERY_PROPERTY_CHARGE_COUNTER)
    cap = bm.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
    intent = activity.registerReceiver(None, IntentFilter(Intent().ACTION_BATTERY_CHANGED))

    def convert_bytes(num):
        step_unit = 1000.0  # 1024 bad the size
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < step_unit:
                return "%3.1f %s" % (num, x)
            num /= step_unit

    def avail_mem():
        stat = StatFs(Environment.getDataDirectory().getPath())
        bytesAvailable = stat.getBlockSize() * stat.getAvailableBlocks()
        if convert:
            return convert_bytes(bytesAvailable)
        else:
            return bytesAvailable

    def total_mem():
        stat = StatFs(Environment.getDataDirectory().getPath())
        bytesAvailable = stat.getBlockSize() * stat.getBlockCount()
        if convert:
            return convert_bytes(bytesAvailable)
        else:
            return bytesAvailable

    def used_mem():
        stat = StatFs(Environment.getDataDirectory().getPath())
        total = stat.getBlockSize() * stat.getBlockCount()
        avail = stat.getBlockSize() * stat.getAvailableBlocks()
        if convert:
            return convert_bytes(total - avail)
        else:
            return total - avail

    def avail_ram():
        memInfo = MemoryInfo(instantiate=True)
        service = activity.getSystemService(Context.ACTIVITY_SERVICE)
        service.getMemoryInfo(memInfo)
        if convert:
            return convert_bytes(memInfo.availMem)
        else:
            return memInfo.availMem

    def total_ram():
        memInfo = MemoryInfo(instantiate=True)
        service = activity.getSystemService(Context.ACTIVITY_SERVICE)
        service.getMemoryInfo(memInfo)
        if convert:
            return convert_bytes(memInfo.totalMem)
        else:
            return memInfo.totalMem

    def used_ram():
        memInfo = MemoryInfo(instantiate=True)
        service = activity.getSystemService(Context.ACTIVITY_SERVICE)
        service.getMemoryInfo(memInfo)
        if convert:
            return convert_bytes(memInfo.totalMem - memInfo.availMem)
        else:
            return memInfo.totalMem - memInfo.availMem
        
    def bat_health():
        context = activity.getApplicationContext()
        intent_filter = IntentFilter(Intent().ACTION_BATTERY_CHANGED)
        intent = context.registerReceiver(None, intent_filter)
        health = intent.getIntExtra(BatteryManager.EXTRA_HEALTH, -1)
        if health == BatteryManager.BATTERY_HEALTH_GOOD:
            return "Good"
        elif health == BatteryManager.BATTERY_HEALTH_OVERHEAT:
            return "Overheated"
        elif health == BatteryManager.BATTERY_HEALTH_DEAD:
            return "Dead"
        elif health == BatteryManager.BATTERY_HEALTH_OVER_VOLTAGE:
            return "Over voltage"
        elif health == BatteryManager.BATTERY_HEALTH_UNSPECIFIED_FAILURE:
            return "Unspecified"
        else:
            return "Unknown"
        
        
    def bat_status():
        context = activity.getApplicationContext()
        intent_filter = IntentFilter(Intent().ACTION_BATTERY_CHANGED)
        intent = context.registerReceiver(None, intent_filter)
        status = intent.getIntExtra(BatteryManager.EXTRA_STATUS, -1)
        if status == BatteryManager.BATTERY_STATUS_CHARGING:
            return "Charging"
        elif status == BatteryManager.BATTERY_STATUS_DISCHARGING:
            return "Discharging"
        elif status == BatteryManager.BATTERY_STATUS_FULL:
            return "Full"
        elif status == BatteryManager.BATTERY_STATUS_NOT_CHARGING:
            return "Not charging"
        else:
            return "Unknown"



    infos = {
        'model': Build.MODEL,
        'brand': Build.BRAND,
        'manufacturer': Build.MANUFACTURER,
        'version': VERSION.RELEASE,
        'sdk': VERSION.SDK,
        'product': Build.PRODUCT,
        'base': VERSION.BASE_OS,
        'rom': VERSION.INCREMENTAL,
        'security': VERSION.SECURITY_PATCH,
        'hardware': Build.HARDWARE,
        'tags': Build.TAGS,
        'sdk_int': VERSION.SDK_INT,
        'cpu_abi': Build.CPU_ABI,
        'cpu_cores': Runtime().getRuntime().availableProcessors(),
        'avail_mem': avail_mem(),
        'total_mem': total_mem(),
        'used_mem': used_mem(),
        'avail_ram': avail_ram(),
        'total_ram': total_ram(),
        'used_ram': used_ram(),
        'bat_level': bm.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY),
        'bat_capacity': round((count / cap) * 100),
        'bat_tempeture': intent.getIntExtra(BatteryManager.EXTRA_TEMPERATURE, 0) / 10,
        'bat_voltage': float(intent.getIntExtra(BatteryManager.EXTRA_VOLTAGE, 0) * 0.001),
        'bat_health' : bat_health(),
        'bat_status' : bat_status(),
        'bat_technology': intent.getStringExtra(BatteryManager.EXTRA_TECHNOLOGY)
    }
    
    if text:
        if text in infos.keys():
            return infos[text]
        else:
            raise KeyError(f"Invalid key. Expected one of {list(infos.keys())}")
    else:
        return infos
