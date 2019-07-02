# -*- coding: utf-8 -*-

__author__ = "Lone Wolf"
__site__ = "github.com/Fox520"
__version__ = 0.1

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from plyer.platforms.android import activity, SDK_INT

from jnius import autoclass, cast

Context = autoclass("android.content.Context")
Build = autoclass("android.os.Build")
NotificationBuilder = autoclass("android.support.v4.app.NotificationCompat$Builder")
Notification = autoclass("android.app.Notification")
NotificationChannel = autoclass("android.app.NotificationChannel")
NotificationManager = autoclass("android.app.NotificationManager")
NotificationCompat = autoclass("android.support.v4.app.NotificationCompat")
NotificationManagerCompat = autoclass("android.support.v4.app.NotificationManagerCompat")
BitmapFactory = autoclass("android.graphics.BitmapFactory")
CHANNEL_ID_1 = "channel1"
CHANNEL_NAME_1 = "FIRSTCHANNEL"
mNotificationManagerCompat = ""
aString = autoclass('java.lang.String')

PythonActivity = autoclass('org.kivy.android.PythonActivity')
currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
activityContext = cast('android.content.Context', currentActivity.getApplicationContext())

test_image_path = "image.jpg"

Builder.load_string('''

<MusicPlayer>:
    BoxLayout:
        orientation: "vertical"
        Button:
            text: "Send notification channel 1"
            on_release: root.sendNoti()    
    

''')


def create_notification_channel():
    global mNotificationManagerCompat
    if SDK_INT >= 26:
        channel1 = NotificationChannel(CHANNEL_ID_1, CHANNEL_NAME_1, NotificationManager.IMPORTANCE_HIGH)
        channel1.setLockscreenVisibility(Notification.VISIBILITY_PUBLIC)

        manager = cast(NotificationManager, currentActivity.getSystemService(Context.NOTIFICATION_SERVICE))
        manager.createNotificationChannel(channel1)

    mNotificationManagerCompat = getattr(NotificationManagerCompat, 'from')(activityContext)

def send_notification():

    MediaStyle = autoclass("android.support.v4.media.app.NotificationCompat$MediaStyle")

    artwork = BitmapFactory.decodeFile(test_image_path)
    channel1 = NotificationBuilder(activityContext, CHANNEL_ID_1)\
        .setSmallIcon(17301618)\
        .setLargeIcon(artwork)\
        .setContentTitle(aString("Let me Love you - DJ snake"))\
        .setContentText(aString("Song by Justin Bieber"))\
        .addAction(17301541, aString("previous"), None)\
        .addAction(17301540, aString("play"), None)\
        .addAction(17301538, aString("next"), None)\
        .setStyle(MediaStyle()
                  .setShowActionsInCompactView(0, 1, 2)) \
        .setSubText("Subtext")\
        .setPriority(NotificationCompat.PRIORITY_LOW)\
        .setAutoCancel(False)\
        .setOngoing(True)\
        .build()
    mNotificationManagerCompat.notify(1, channel1)

class MusicPlayer(Screen):

    def __init__(self, **kwargs):
        super(MusicPlayer, self).__init__()
        create_notification_channel()

    def sendNoti(self):
        send_notification()

class MusicApp(App):

    def build(self):
        return sm

    def on_pause(self):
        return True

    def on_resume(self):
        pass


sm = ScreenManager()
sm.add_widget(MusicPlayer(name="music_player"))

if __name__ == "__main__":
    MusicApp().run()
