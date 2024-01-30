import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.widget = QVideoWidget()
        self.setCentralWidget(self.widget)
        self.player.setVideoOutput(self.widget)

        # State variable to indicate if generic video is playing
        self.generic_video_playing = True
        self.current_gender = "none"  # Store the current gender

        # Timer to check for gender updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_gender)
        self.timer.start(1000)  # Check every second

        # Connect to mediaStatusChanged signal
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)

        # Initially play the generic video
        self.play_video("none")

    def check_gender(self):
        if self.generic_video_playing:  # Check for gender only if generic video is playing
            try:
                with open("/home/athena/Documents/Upwork/Ad/age-gender/age-and-gender/example/gender_detected.txt", "r") as file:
                    gender = file.read().strip()
                    print(gender)
                    if gender in ["male", "female"]:  # If a specific gender is detected
                        if gender != self.current_gender:  # Check if gender has changed
                            self.current_gender = gender
                            self.play_video(gender)
            except FileNotFoundError:
                pass
    def check_gender_x(self):
        try:
            with open("/home/athena/Documents/Upwork/Ad/age-gender/age-and-gender/example/gender_detected.txt", "r") as file:
                gender = file.read().strip()
                print(gender)
                if gender in ["male", "female","none"]:  # If a specific gender is detected
                    if gender != self.current_gender:  # Check if gender has changed
                        self.current_gender = gender
                        self.play_video(gender)
        except FileNotFoundError:
            pass

    def play_video(self, gender):
        if gender == "none":
            self.generic_video_playing = True
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile("/home/athena/Documents/Upwork/Ad/age-gender/age-and-gender/video/generic/video.mp4")))
        else:
            self.generic_video_playing = False
            video_path = "/home/athena/Documents/Upwork/Ad/age-gender/age-and-gender/video/male/video.mp4" if gender == "male" else "/home/athena/Documents/Upwork/Ad/age-gender/age-and-gender/video/female/video.mp4"
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.player.play()

    def on_media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            # Restart the video when it reaches the end
            self.check_gender_x()
            print(self.current_gender)
            self.play_video(self.current_gender)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.showMaximized()  # Maximize the main window
    sys.exit(app.exec_())
