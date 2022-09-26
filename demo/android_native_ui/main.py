from kvdroid import activity
from android.runnable import run_on_ui_thread

from kvdroid.app import App
from kvdroid.jclass.android import RelativeLayout, ViewGroupLayoutParams, TextView
from kvdroid.jclass.java import String


class TestApp(App):

    def build_view(self):
        relative_layout = RelativeLayout(activity)
        layout_params = ViewGroupLayoutParams()
        text_view = TextView(activity)
        text_view.setText(String("Hello World"))
        relative_layout.addView(text_view, layout_params(layout_params.Wrap, layout_params.FILL_PARENT))
        return relative_layout


TestApp().run()
