from textwrap import dedent

kvdroid_tools = [
    {
        "text": "SHARE FILE",
        "exec": dedent(
            """
            from kvdroid.tools import share_file
            
            share_file('assets/image/icon.png')
            """
        )
    },
    {
        "text": "SHARE TEXT",
        "exec": dedent(
            """
            from kvdroid.tools import share_text

            share_text('Sent from KvDroid')
            """
        )
    },
    {
        "text": "RESTART APP",
        "exec": dedent(
            """
            from kvdroid.tools import restart_app
            
            restart_app()
            """
        )
    },
    {
        "text": "TOAST",
        "exec": dedent(
            """
            from kvdroid.tools import toast

            toast('Hello, Welcome to KvDroid')
            """
        )
    },
    {
        "text": "DOWNLOAD MANAGER",
        "exec": dedent(
            """
            from kvdroid.tools import download_manager

            download_manager('Downloading Egedege Song', 'Egedege ndi Igbo', 'https://bit.ly/3mHQdzZ')
            """
        )
    },
    {
        "text": "CHANGE STATUSBAR COLOR",
        "exec": dedent(
            """
            from kvdroid.tools import change_statusbar_color

            change_statusbar_color('#AA00FF', 'white')
            """
        )
    },
    {
        "text": "CHANGE NAVIGATION BAR COLOR",
        "exec": dedent(
            """
            from kvdroid.tools import navbar_color

            navbar_color('#AA00FF')
            """
        )

    },
    {
        "text": "SET WALLPAPER",
        "exec": dedent(
            """
            from kvdroid.tools import set_wallpaper

            set_wallpaper('assets/image/icon.png')
            """
        )
    },
    {
        "text": "TEXT TO SPEECH",
        "exec": dedent(
            """
            from kvdroid.tools import speech

            speech('This is KV Droid application talking', 'en')
            """
        )
    },
    {
        "text": "IMMERSIVE MODE",
        "exec": dedent(
            """
            from kvdroid.tools import immersive_mode
            
            immersive_mode()
            """
        )
    },
    {
        "text": "LAUNCH CHROME APPLICATION",
        "exec": dedent(
            """
            from kvdroid.tools import launch_app
            
            launch_app('com.android.chrome')
            """
        )
    },
    {
        "text": "GET CHROME DETAILS",
        "exec": dedent(
            """
            from kvdroid.tools import app_details
            
            app_details('com.android.chrome')
            """
        )
    },
    {
        "text": "PLAY LOCAL MUSIC",
        "exec": dedent(
            """
            from kvdroid.tools.audio import Player

            Player().play('assets/audio/Egedege.mp3')
            """
        )
    },
    {
        "text": "STREAM ONLINE MUSIC",
        "exec": dedent(
            """
            from kvdroid.tools.audio import Player
            from kvdroid.tools import toast
            
            toast('fetching music data')
            Player().stream('https://bit.ly/3mHQdzZ')
            """
        )
    },
    {
        "text": "CALL 911",
        "exec": dedent(
            """
            from kvdroid.tools.call import make_call
                
            make_call('911')
            """
        )
    },
    {
        "text": "DIAL 911",
        "exec": dedent(
            """
            from kvdroid.tools.call import dial_call
                
            dial_call('911')
            """
        )
    },
    {
        "text": "READ MY CONTACT",
        "exec": dedent(
            """
            from kvdroid.tools.contact import get_contact_details
            print(get_contact_details())
            
            from kvdroid.tools import toast
            toast(
                'use adb logcat -s python to view your contact list, '
                'will still provide a more user friendly way in the near future'
            )
            """
        )
    },
    {
        "text": "OPEN CUSTOM TAB WEBVIEW",
        "exec": dedent(
            """
            from kvdroid.tools.webkit import launch_url
            
            launch_url('https://github.com/kvdroid/Kvdroid')
            """
        )
    },
    {
        "text": "NOTIFICATION",
        "exec": dedent(
            """
            from kvdroid.tools.notification import create_notification
            from kvdroid.jclass.android import Color
            from kvdroid.tools import get_resource
            
            create_notification(
               small_icon=get_resource('drawable').ic_kvdroid,
               channel_id ='1',
               title='KvDroid',
               text='hello from kvdroid androidx notification',
               ids=1,
               channel_name='ch1',
               large_icon='assets/image/icon.png',
               big_picture='assets/image/icon.png',
               action_title1='CLICK',
               action_title2='PRESS',
               reply_title='REPLY', set_reply=True,
               expandable=True, set_large_icon=True,
               add_action_button1=True,
               add_action_button2=True,
               small_icon_color=Color().parseColor('#2962FF')
            )
            """
        )
    },
    {
        "text": "READ SMS",
        "exec": dedent(
            """
            from kvdroid.tools.notification import create_notification
            from kvdroid.tools.sms import get_all_sms
            
            get_all_sms()
            """
        )
    }
]
