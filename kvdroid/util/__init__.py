from kvdroid.jclass.java import System


def garbage_collect():
    System().gc()
    System().runFinalization()