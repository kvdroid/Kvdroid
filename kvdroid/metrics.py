from kvdroid import activity, Point
import re

class Metrics(object):
    config = activity.getResources().getConfiguration()
    metric = activity.getResources().getDisplayMetrics()

    def height_dp(self):
        return self.config.screenHeightDp

    def width_dp(self):
        return self.config.screenWidthDp

    def height_px(self):
        return self.metric.heightPixels

    def width_px(self):
        return self.metric.widthPixels

    def orientation(self):
        if self.config.orientation == 1:
            return "portrait"
        else:
            return "landscape"
            
    def resolution(self):
        point = Point()
        activity.getWindowManager().getDefaultDisplay().getRealSize(point)
        size = re.findall("\d+",point.toString())
        return size[1]+"x"+size[0]

screen = Metrics()
