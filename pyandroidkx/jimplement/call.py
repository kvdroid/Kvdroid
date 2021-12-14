from pyandroidkx.jclass.android.net import Uri

from pyandroidkx.jclass.android.content import Intent
from pyandroidkx import activity


def make_call(tel):
    intent = Intent(Intent.ACTION_CALL, Uri.parse(f"tel:{tel}"))
    activity.startActivity(intent)


def dial_call(tel):
    intent = Intent(Intent.ACTION_DIAL, Uri.parse(f"tel:{tel}"))
    activity.startActivity(intent)
