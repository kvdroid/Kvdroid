from jnius import PythonJavaClass, java_method


class ActivityResultCallback(PythonJavaClass):
    __javainterfaces__ = ["androidx/activity/result/ActivityResultCallback"]
    __javacontext__ = "app"

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    @java_method("(Ljava/lang/Object;)V")
    def onActivityResult(self, obj):
        self.callback(obj)
