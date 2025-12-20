# from jnius import autoclass, JavaException
#
# try:
#     autoclass("androidx.media3.common.MediaItem")
# except JavaException as e:
#     raise JavaException(
#         f"{e}\nadd androidx.media3:media3-common:1.8.0, androidx.media3:media3-exoplayer:1.8.0 and "
#         f"org.jetbrains.kotlin:kotlin-stdlib-jdk8:1.8.0 to buildozer.spec file: "
#         f"android.gradle_dependencies. Make sure your target API is 36 or higher."
#     )
