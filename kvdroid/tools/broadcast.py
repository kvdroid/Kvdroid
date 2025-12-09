# -------------------------------------------------------------------
# Broadcast receiver bridge
import logging

from jnius import autoclass, PythonJavaClass, java_method  # NOQA
from android.config import JNI_NAMESPACE  # NOQA

from kvdroid.jclass.androidx import ContextCompat
from kvdroid.jclass.org import GenericBroadcastReceiver
from kvdroid.jclass.android import IntentFilter, HandlerThread, Intent, Handler
from kvdroid import activity

logger = logging.getLogger("BroadcastReceiver")
logger.setLevel(logging.DEBUG)


class BroadcastReceiver(object):

    class Callback(PythonJavaClass):
        __javainterfaces__ = [f"{JNI_NAMESPACE}/GenericBroadcastReceiverCallback"]
        __javacontext__ = "app"

        def __init__(self, callback, *args, **kwargs):
            self.callback = callback
            PythonJavaClass.__init__(self, *args, **kwargs)

        @java_method("(Landroid/content/Context;Landroid/content/Intent;)V")
        def onReceive(self, context, intent):
            self.callback(context, intent)

    def __init__(self, callback, actions=None, categories=None, use_intent_action=True):
        super().__init__()
        self.handler = None
        self.callback = callback

        if not actions and not categories:
            raise ValueError("You need to define at least actions or categories")

        def _expand_partial_name(partial_name):
            if "." in partial_name:
                return partial_name  # Its actually a full dotted name
            name = "ACTION_{}".format(partial_name.upper())
            if not hasattr(Intent(), name):
                raise AttributeError("The intent {} doesnt exist".format(name))
            return getattr(Intent(), name)

        if use_intent_action:
            # resolve actions/categories first
            resolved_actions = [_expand_partial_name(x) for x in actions or []]
            resolved_categories = [_expand_partial_name(x) for x in categories or []]
        else:
            resolved_actions = actions or []
            resolved_categories = categories or []

        # resolve android API

        # create a thread for handling events from the receiver
        self.handler_thread = HandlerThread("handlerthread")

        # create a listener
        self.listener = BroadcastReceiver.Callback(self.callback)
        self.receiver = GenericBroadcastReceiver(self.listener)
        self.receiver_filter = IntentFilter(instantiate=True)
        for x in resolved_actions:
            self.receiver_filter.addAction(x)
        for x in resolved_categories:
            self.receiver_filter.addCategory(x)

    def start(self):
        if hasattr(self, "handlerthread") and self.handlerthread.isAlive():
            logger.debug("HandlerThread already running, skipping start")
            return
        self.handler_thread.start()
        self.handler = Handler(self.handler_thread.getLooper())
        ContextCompat().registerReceiver(
            activity,
            self.receiver,
            self.receiver_filter,
            None,
            self.handler,
            ContextCompat().RECEIVER_NOT_EXPORTED,
        )

    def stop(self):
        activity.unregisterReceiver(self.receiver)
        self.handler_thread.quit()
