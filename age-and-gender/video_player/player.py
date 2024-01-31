import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer
import os
class VideoPlayer(QMainWindow):
    def __init__(self, video_folder_path):
        super().__init__()
        self.videos_folder_path = video_folder_path
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
                with open("../example/gender_detected.txt", "r") as file:
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
            with open("../example/gender_detected.txt", "r") as file:
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
            generic_video_path = os.path.join(self.videos_folder_path, "generic")
            self.play_random_video_in_folder(generic_video_path)
        else:
            self.generic_video_playing = False
            gender_subfolder = "male" if gender == "male" else "female"
            gender_video_path = os.path.join(self.videos_folder_path, gender_subfolder)
            self.play_random_video_in_folder(gender_video_path)
    def play_random_video_in_folder(self, folder_path):
        # Get a list of all video files in the folder
        video_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp4', '.avi', '.mkv'))]
        if video_files:
            # Select and play the first video in the folder
            video_filename = video_files[0]
            video_path = os.path.join(folder_path, video_filename)
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
            self.player.play()
    def on_media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            # Restart the video when it reaches the end
            self.check_gender_x()
            print(self.current_gender)
            self.play_video(self.current_gender)
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python video_player.py <videos_folder_path>")
        sys.exit(1)
    app = QApplication(sys.argv)
    videos_folder_path = sys.argv[1]
    player = VideoPlayer(videos_folder_path)
    player.showMaximized()  # Maximize the main window
    sys.exit(app.exec_())