from jnius import autoclass, JavaException

try:
    CustomTabsIntent = autoclass("androidx.browser.customtabs.CustomTabsIntent")
    CustomTabsIntentBuilder = autoclass("androidx.browser.customtabs.CustomTabsIntent$Builder")
    CustomTabColorSchemeParams = autoclass("androidx.browser.customtabs.CustomTabColorSchemeParams")
    CustomTabColorSchemeParamsBuilder = autoclass("androidx.browser.customtabs.CustomTabColorSchemeParams$Builder")
except JavaException as e:
    raise JavaException(
        f"{e}\nEnable androidx in your buildozer.spec file\nadd 'androidx.browser:browser:1.4.0' to buildozer.spec "
        f"file: android.gradle_dependencies"
    )
