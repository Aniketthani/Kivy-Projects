from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.text import LabelBase
from kivy.config import Config
from kivy.lang import Builder

#importing java classes required for our app
from jnius import autoclass

#java classes
Environment=autoclass('android.os.Environment')
MediaRecorder=autoclass('android.media.MediaRecorder')
AudioSource=autoclass('android.media.MediaRecorder$AudioSource')
OutputFormat=autoclass('android.media.MediaRecorder$OutputFormat')
AudioEncoder=autoclass('android.media.MediaRecorder$AudioEncoder')

#storage path
path=Environment.getExternalStorageDirectory().getAbsolutePath() + '/kivy_recording.3gp'

#instantiate The MediaRecorder
recorder=MediaRecorder()

#function for initializing our recorder
def init_recorder():
    recorder.setAudioSource(AudioSource.MIC)
    recorder.setOutputFormat(OutputFormat.THREE_GPP)
    recorder.setAudioEncoder(AudioEncoder.AMR_NB)
    recorder.setOutputFile(path)
    recorder.prepare()

#Media Player
MediaPlayer=autoclass('android.media.MediaPlayer')
player=MediaPlayer()

#import File Class  for deleting file
File=autoclass('java.io.File')


def reset_player():
    if (player.isPlaying()):
        player.stop()
    player.reset()

def restart_player():
    reset_player()
    try:
        player.setDataSource(path)
        player.prepare()
        player.start()
    except:
        player.reset()


#linking the .kv file
Builder.load_file("srecorder.kv")

class MyWidget(GridLayout):
    is_recording=False
    
    def begin_end_recording(self):
        if(self.is_recording):
            recorder.stop()
            recorder.reset()
            self.is_recording=False
            self.ids.begin_end_recording_btn.text="[font=modernpics][size=120]e[/size][/font]\nBegin Recording"
            return
        init_recorder()
        recorder.start()
        self.is_recording=True
        self.ids.begin_end_recording_btn.text="[font=modernpics][size=120]%[/size][/font]\nEnd Recording"
    def playback(self):
        restart_player()
    def delete_file(self):
        reset_player()
        File(path).delete()

class RecordingApp(App):
    def build(self):
        
        return MyWidget()

if __name__=="__main__":
    LabelBase.register(name="modernpics",
    fn_regular="modernpics/modernpics.ttf")
    Config.set('graphics','width','600')
    Config.set('graphics','height','800')
    RecordingApp().run()