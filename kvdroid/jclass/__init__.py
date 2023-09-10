from jnius import autoclass, JavaException  # NOQA


def _class_call(cls, args: tuple, instantiate: bool):
    if not args:
        return cls() if instantiate else cls
    else:
        return cls(*args)


def _browserx_except_cls_call(namespace: str, args: tuple, instantiate: bool):
    try:
        return _class_call(autoclass(namespace), args, instantiate)
    except JavaException as e:
        raise JavaException(
            f"{e}\nEnable androidx in your buildozer.spec file\nadd 'androidx.browser:browser:1.4.0' to "
            f"buildozer.spec file: android.gradle_dependencies"
        ) from e
