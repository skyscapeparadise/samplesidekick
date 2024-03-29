"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

samplesidekick
by skyscapeparadise (kady and friends? come on guys help me out)

special thanks to: juan the python genius for helping me implement the
renaming feature! finn foley for giving me a reason to get this thing
finished already, moonriver for being so chill about me being super
obsessed with stuff like this, guy white for encouraging me to get
this onto github, zena and drew for believing i was capable of doing
stuff like this before i ever did stuff like this.
"""

# We import all the libraries we need to rename files, have a flashy video GUI, play a fake progress bar video, etc

import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QMenu
from PySide6.QtCore import QTimer, Qt, Signal, QUrl, QSize
from PySide6.QtGui import QPixmap, QImage, QAction, QPainter, QPaintEvent, QIcon, QColor, QBrush
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
import cv2
import platform
import subprocess
import shutil
from itertools import cycle, islice, product

# Define all the elements of the final sample filenames

chromaticscale = ["C0", "C#0", "D0", "D#0", "E0", "F0", "F#0", "G0", "G#0", "A0", "A#0", "B0", "C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1", "G#1", "A1", "A#1", "B1", "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2", "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3", "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4", "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5", "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6", "C7", "C#7", "D7", "D#7", "E7", "F7", "F#7", "G7", "G#7", "A7", "A#7", "B7", "C8", "C#8", "D8", "D#8", "E8", "F8", "F#8", "G8", "G#8", "A8", "A#8", "B8", "C9", "C#9", "D9", "D#9", "E9", "F9", "F#9", "G9", "G#9", "A9", "A#9", "B9"]

velocitydivisions = {
	10: [" 1 13 ", " 14 25 ", " 26 38 ", " 39 51 ", " 52 64 ", " 65 76 ", " 77 89 ", " 90 102 ", " 103 114 ", " 115 127 "],
	9: [" 1 14 ", " 15 28 ", " 29 42 ", " 43 56 ", " 57 71 ", " 72 85 ", " 86 99 ", " 100 113 ", " 114 127 "],
	8: [" 1 16 ", " 17 32 ", " 33 48 ", " 49 64 ", " 65 79 ", " 80 95 ", " 96 111 ", " 112 127 "],
	7: [" 1 18 ", " 19 36 ", " 37 54 ", " 55 73 ", " 74 91 ", " 92 109 ", " 110 127 "],
	6: [" 1 21 ", " 22 42 ", " 43 64 ", " 65 85 ", " 86 106 ", " 107 127 "],
	5: [" 1 25 ", " 26 51 ", " 52 76 ", " 77 102 ", " 103 127 "],
	4: [" 1 32 ", " 33 64 ", " 65 95 ", " 96 127 "],
	3: [" 1 42 ", " 43 85 ", " 86 127 "],
	2: [" 1 64 ", " 65 127 "],
	1: [""]
	}
	
velocitydivisions = {
	10: [" 1 13 ", " 14 25 ", " 26 38 ", " 39 51 ", " 52 64 ", " 65 76 ", " 77 89 ", " 90 102 ", " 103 114 ", " 115 127 "],
	9: [" 1 14 ", " 15 28 ", " 29 42 ", " 43 56 ", " 57 71 ", " 72 85 ", " 86 99 ", " 100 113 ", " 114 127 "],
	8: [" 1 16 ", " 17 32 ", " 33 48 ", " 49 64 ", " 65 79 ", " 80 95 ", " 96 111 ", " 112 127 "],
	7: [" 1 18 ", " 19 36 ", " 37 54 ", " 55 73 ", " 74 91 ", " 92 109 ", " 110 127 "],
	6: [" 1 21 ", " 22 42 ", " 43 64 ", " 65 85 ", " 86 106 ", " 107 127 "],
	5: [" 1 25 ", " 26 51 ", " 52 76 ", " 77 102 ", " 103 127 "],
	4: [" 1 32 ", " 33 64 ", " 65 95 ", " 96 127 "],
	3: [" 1 42 ", " 43 85 ", " 86 127 "],
	2: [" 1 64 ", " 65 127 "],
	1: [""]
	}
	
velocitydivisionsdescending = {
	10: [' 103 127 ', ' 90 102 ', ' 77 89 ', ' 65 76 ', ' 52 64 ', ' 39 51 ', ' 26 38 ', ' 14 25 ', '  1 13 '],
	9: [' 100 127 ', ' 72 85 ', ' 57 71 ', ' 43 56 ', ' 29 42 ', ' 15 28 ', '  1 14 '],
	8: [' 112 127 ', ' 96 111 ', ' 80 95 ', ' 65 79 ', ' 49 64 ', ' 33 48 ', ' 17 32 ', '  1 16 '],
	7: [' 110 127 ', ' 92 109 ', ' 74 91 ', ' 55 73 ', ' 37 54 ', ' 19 36 ', '  1 18 '],
	6: [' 107 127 ', ' 86 106 ', ' 65 85 ', ' 43 64 ', ' 22 42 ', '  1 21 '],
	5: [' 103 127 ', ' 77 102 ', ' 52 76 ', ' 26 51 ', '  1 25 '],
	4: [' 96 127 ', ' 65 95 ', ' 33 64 ', '  1 32 '],
	3: [' 86 127 ', ' 43 85 ', '  1 42 '],
	2: [' 65 127 ', '  1 64 '],
	1: ['']
	}

roundrobindict = {
	10: [" rr 1 ", " rr 2 ", " rr 3 ", " rr 4 ", " rr 5 ", " rr 6 ", " rr 7 ", " rr 8 ", " rr 9 ", " rr 10 "],
	9: [" rr 1 ", " rr 2 ", " rr 3 ", " rr 4 ", " rr 5 ", " rr 6 ", " rr 7 ", " rr 8 ", " rr 9 "],
	8: [" rr 1 ", " rr 2 ", " rr 3 ", " rr 4 ", " rr 5 ", " rr 6 ", " rr 7 ", " rr 8 "],
	7: [" rr 1 ", " rr 2 ", " rr 3 ", " rr 4 ", " rr 5 ", " rr 6 ", " rr 7 "],
	6: [" rr 1 ", " rr 2 ", " rr 3 ", " rr 4 ", " rr 5 ", " rr 6 "],
	5: [" rr 1 ", " rr 2 ", " rr 3 ", " rr 4 ", " rr 5 "],
	4: [" rr 1 ", " rr 2 ", " rr 3 ", " rr 4 "],
	3: [" rr 1 ", " rr 2 ", " rr 3 "],
	2: [" rr 1 ", " rr 2 "],
	1: [""]
	}

signaltracksdict = {
	10: ["track1 ", "track2 ", "track3 ", "track4 ", "track5 ", "track6 ", "track7 ", "track8 ", "track9 ", "track10 "],
	9: ["track1 ", "track2 ", "track3 ", "track4 ", "track5 ", "track6 ", "track7 ", "track8 ", "track9 "],
	8: ["track1 ", "track2 ", "track3 ", "track4 ", "track5 ", "track6 ", "track7 ", "track8 "],
	7: ["track1 ", "track2 ", "track3 ", "track4 ", "track5 ", "track6 ", "track7 "],
	6: ["track1 ", "track2 ", "track3 ", "track4 ", "track5 ", "track6 "],
	5: ["track1 ", "track2 ", "track3 ", "track4 ", "track5 "],
	4: ["track1 ", "track2 ", "track3 ", "track4 "],
	3: ["track1 ", "track2 ", "track3 "],
	2: ["track1 ", "track2 "],
	1: [""]
	}

# Declare the options variables

signaltracks = 1
startingnote = "C"
startingnumber = 3
skippednotes = 0
velocitylayers = 1
roundrobins = 1
startingnoteandnumber = startingnote + str(startingnumber)
original_directory = ""
new_directory = ""
velocitydirection = True

# Define a way to link to the user interface graphics

def resource_path(relative_path):
	if hasattr(sys, '_MEIPASS'):
		return os.path.join(sys._MEIPASS, relative_path)
	return os.path.join(os.path.abspath("."), relative_path)

# Define the way to draw the directory location text

class RightAlignedLabel(QLabel):
	def paintEvent(self, event):
		painter = QPainter(self)
		rect = self.contentsRect()
		elided_text = painter.fontMetrics().elidedText(self.text(), Qt.TextElideMode.ElideLeft, rect.width())
		painter.drawText(rect, Qt.AlignmentFlag.AlignRight, elided_text)
		
class ImageDialog(QDialog):
	def __init__(self, image_path):
		super().__init__()
		
		# Make the dialog box borderless and on the top of the window stack
		self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
		
		# Load the image, get its dimensions, and scale it down to 50%
		original_pixmap = QPixmap(image_path)
		width = int(original_pixmap.width() * 0.5)
		height = int(original_pixmap.height() * 0.5)
		pixmap = original_pixmap.scaled(QSize(width, height))
		
		# Create a QLabel to display the image
		label = QLabel(self)
		label.setPixmap(pixmap)
		
		# Set up the layout
		layout = QVBoxLayout(self)
		layout.addWidget(label)
		
		# Set layout margin to zero
		layout.setContentsMargins(0, 0, 0, 0)
		
		# Set dialog stylesheet to remove border
		self.setStyleSheet("QDialog {border: 0px;}")
		
		self.closedialog_button = SpriteButton(self)
		self.closedialog_button.setGeometry(177, 129, 84, 20)
		self.closedialog_button.setFixedSize(84, 20)
		self.closedialog_button.setSpriteImage(resource_path("media/closesprite.png"))
		self.closedialog_button.clickedToOff.connect(self.close)
		
# Define the main window (This is where most of the application logic is including the renaming routine)

class VideoWindow(QMainWindow):
	def __init__(self, intro_video_path, day_video_path, night_video_path):
		super().__init__()

		# Create a label to display the video frames
		self.video_label = QLabel(self)
		self.video_label.setGeometry(0, 0, 960, 540)
		self.setCentralWidget(self.video_label)

		# Disable window resizing
		flags = self.windowFlags()
		flags &= ~Qt.WindowType.WindowMaximizeButtonHint
		flags &= ~Qt.WindowType.WindowMinimizeButtonHint
		self.setWindowFlags(flags)

		# Create labels for target and destination directories
		self.target_directory = RightAlignedLabel("", self)
		self.target_directory.setStyleSheet("color: white;")
		self.target_directory.setGeometry(48, 410, 180, 30)

		self.destination_directory = RightAlignedLabel("", self)
		self.destination_directory.setStyleSheet("color: white;")
		self.destination_directory.setGeometry(321, 410, 180, 30)

		# Hide the labels initially
		self.target_directory.hide()
		self.destination_directory.hide()

		# Create buttons for selecting directories
		self.target_directory_button = SpriteButton(self)
		self.target_directory_button.setGeometry(92, 464, 84, 20)
		self.target_directory_button.setFixedSize(84, 20)
		self.target_directory_button.setText("Select Target Directory")
		self.target_directory_button.setSpriteImage(resource_path("media/selectsprite.png"))
		self.target_directory_button.clickedToOff.connect(self.select_target_directory)
		self.target_directory_button.hide()

		self.destination_directory_button = SpriteButton(self)
		self.destination_directory_button.setGeometry(375, 464, 84, 20)
		self.destination_directory_button.setFixedSize(84, 20)
		self.destination_directory_button.setSpriteImage(resource_path("media/selectsprite.png"))
		self.destination_directory_button.setText("Select Destination Directory")
		self.destination_directory_button.clickedToOff.connect(self.select_destination_directory)
		self.destination_directory_button.hide()

		# Create the start button that executes the renaming operation
		self.rename_button = SpriteButton(self)
		self.rename_button.setGeometry(843, 168, 84, 20)
		self.rename_button.setFixedSize(84, 20)
		self.rename_button.setSpriteImage(resource_path("media/startsprite.png"))
		self.rename_button.setText("Start")
		self.rename_button.clickedToOff.connect(lambda: samplerename(signaltracks, startingnote, startingnumber, skippednotes, velocitylayers, roundrobins, chromaticscale, velocitydivisions, roundrobindict, signaltracksdict, original_directory, new_directory, velocitydirection))
		self.rename_button.hide()
		
		# Create the signal tracks button
		self.signaltracks_button = SignalTracksButton(self)
		self.signaltracks_button.setGeometry(837, 255, 40, 20)
		self.signaltracks_button.setFixedSize(40,20)
		self.signaltracks_button.setSpriteImage(resource_path(resource_path("media/ddbutton.png")))
		self.signaltracks_button.setText("Signal Tracks")
		self.signaltracks_button.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
		self.signaltracks_button.hide()
		
		# Create the starting note button
		self.startingnote_button = NoteButton(self)
		self.startingnote_button.setGeometry(837, 292, 40, 20)
		self.startingnote_button.setFixedSize(40,20)
		self.startingnote_button.setSpriteImage(resource_path("media/ddbutton.png"))
		self.startingnote_button.setText("Starting Note")
		self.startingnote_button.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
		self.startingnote_button.hide()

		# Create the starting note number button
		self.startingnumber_button = NumberButton(self)
		self.startingnumber_button.setGeometry(887, 292, 40, 20)
		self.startingnumber_button.setFixedSize(40,20)
		self.startingnumber_button.setSpriteImage(resource_path("media/ddbutton.png"))
		self.startingnumber_button.setText("Starting Note Number")
		self.startingnumber_button.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
		self.startingnumber_button.hide()
		
		# Create the skipped notes button
		self.skippednotes_button = SkippedButton(self)
		self.skippednotes_button.setGeometry(837, 329, 40, 20)
		self.skippednotes_button.setFixedSize(40,20)
		self.skippednotes_button.setSpriteImage(resource_path("media/ddbutton.png"))
		self.skippednotes_button.setText("Skipped Notes")
		self.skippednotes_button.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
		self.skippednotes_button.hide()
		
		# Create the velocity layers button
		self.velocitylayers_button = VelocityButton(self)
		self.velocitylayers_button.setGeometry(837, 365, 40, 20)
		self.velocitylayers_button.setFixedSize(40,20)
		self.velocitylayers_button.setSpriteImage(resource_path("media/ddbutton.png"))
		self.velocitylayers_button.setText("Velocity Layers")
		self.velocitylayers_button.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
		self.velocitylayers_button.hide()

		# Create the velocity direction button
		self.velocitydirection_button = DirectionButton(self)
		self.velocitydirection_button.setGeometry(887, 365, 40, 20)
		self.velocitydirection_button.setFixedSize(40,20)
		self.velocitydirection_button.setSpriteImage(resource_path("media/ddbutton.png"))
		self.velocitydirection_button.setText("Velocity Direction")
		self.velocitydirection_button.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
		self.velocitydirection_button.hide()

		# Create the round robins button
		self.roundrobins_button = RoundRobinsButton(self)
		self.roundrobins_button.setGeometry(837, 401, 40, 20)
		self.roundrobins_button.setFixedSize(40,20)
		self.roundrobins_button.setSpriteImage(resource_path("media/ddbutton.png"))
		self.roundrobins_button.setText("Skipped Notes")
		self.roundrobins_button.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
		self.roundrobins_button.hide()
		
		# Create the progress bar
		self.progressbar = AnimatedSprite(self, darkness=False)
		self.progressbar.label.setGeometry(162, 121, 765, 35)

		# Open the video files
		self.intro_cap = cv2.VideoCapture(intro_video_path)
		self.day_cap = cv2.VideoCapture(day_video_path)
		self.night_cap = cv2.VideoCapture(night_video_path)

		if not self.intro_cap.isOpened() or not self.day_cap.isOpened() or not self.night_cap.isOpened():
			print("Error opening video file")
			sys.exit(1)

		# Create a QTimer to update the video frames
		self.timer = QTimer()
		self.timer.timeout.connect(self.update_frame)

		# Track state transition
		self.transition_to_main = False

		# Start playing intro video
		self.intro_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
		self.timer.start(30)

		# Monitor dark mode changes
		self.last_dark_mode = self.is_dark_mode()
		self.timer_dark_mode = QTimer()
		self.timer_dark_mode.timeout.connect(self.check_dark_mode)
		self.timer_dark_mode.start(1000)
				
	def is_dark_mode(self):
		if platform.system() == "Darwin":
			return self.is_dark_mode_mac()
		elif platform.system() == "Windows":
			return self.is_dark_mode_windows()
		elif platform.system() == "Linux":
			return self.is_dark_mode_linux()
		else:
			return False
	
	def is_dark_mode_mac(self):
		# Execute 'defaults' command to read system preferences
		cmd = ['defaults', 'read', '-g', 'AppleInterfaceStyle']
		result = subprocess.run(cmd, capture_output=True, text=True)
	
		if result.returncode == 0:
			# Check the output for dark mode status
			output = result.stdout.strip()
			if output == 'Dark':
				return True
			elif output == 'Light':
				return False
	
		# Default fallback value if unable to determine dark mode status
		return False
	
	# Dark mode will likely only be supported on macOS but feel free to implement dark mode for other operating systems it if you want
	
	def is_dark_mode_windows(self):
		# Perform Windows-specific dark mode detection here
		# You can use Windows registry or other Windows-specific APIs to determine the dark mode status
		# Return True if dark mode is enabled, False otherwise
		return False
	
	def is_dark_mode_linux(self):
		# Perform Linux-specific dark mode detection here
		# You can use system commands or other Linux-specific methods to determine the dark mode status
		# Return True if dark mode is enabled, False otherwise
		return False
	
	def check_dark_mode(self):
		current_dark_mode = self.is_dark_mode()
		if current_dark_mode != self.last_dark_mode:
			self.handle_dark_mode_change()
			self.last_dark_mode = current_dark_mode
	
	# The "main video" is the GUI background. I might want to make the background animated in the future, for now, the video files depict still images.
	# The backgrounds for both day and night mode are HEVC .mp4 files saved in the "media" folder
	
	def start_main_video(self):
		current_mode = self.is_dark_mode()
		video_cap = self.night_cap if current_mode else self.day_cap
		video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
		self.timer.start(30)
	
	def update_frame(self):
		if not self.transition_to_main:
			ret, frame = self.intro_cap.read()
		
			if not ret:
				self.transition_to_main = True
				self.start_main_video()
				return
		else:
			current_mode = self.is_dark_mode()
			video_cap = self.night_cap if current_mode else self.day_cap
			ret, frame = video_cap.read()
		
			if not ret:
				video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
				ret, frame = video_cap.read()
		
		frame_resized = cv2.resize(frame, (960, 540))
		frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
		img = QPixmap.fromImage(
			QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format.Format_RGB888)
		)
		self.video_label.setPixmap(img)


		if self.transition_to_main:
			# Show the buttons during the transition to the main section
			self.target_directory.show()
			self.destination_directory.show()
			self.target_directory_button.show()
			self.destination_directory_button.show()
			self.rename_button.show()
			self.signaltracks_button.show()
			self.startingnote_button.show()
			self.startingnumber_button.show()
			self.skippednotes_button.show()
			self.velocitylayers_button.show()
			self.velocitydirection_button.show()
			self.roundrobins_button.show()
		else:
			# Hide the buttons during the intro video playback
			self.target_directory.hide()
			self.destination_directory.hide()
			self.target_directory_button.hide()
			self.destination_directory_button.hide()
			self.rename_button.hide()
			self.signaltracks_button.hide()
			self.startingnote_button.hide()
			self.startingnumber_button.hide()
			self.skippednotes_button.hide()
			self.velocitylayers_button.hide()
			self.velocitydirection_button.hide()
			self.roundrobins_button.hide()
	
	def handle_dark_mode_change(self):
		if self.transition_to_main:
			self.transition_to_main = False
			self.start_main_video()
	
	def select_target_directory(self):
		global original_directory
		original_directory = QFileDialog.getExistingDirectory(self, "Select Target Directory")
		self.target_directory.setText(original_directory)
	
	def select_destination_directory(self):
		global new_directory
		new_directory = QFileDialog.getExistingDirectory(self, "Select Destination Directory")
		self.destination_directory.setText(new_directory)
	
	def hide_buttons(self):
		self.target_directory_button.hide()
		self.destination_directory_button.hide()
		
	def playprogress(self):	
		self.progressbar.start_animation(self.is_dark_mode())

# Define the sprite based buttons
		
class SpriteButton(QPushButton):
	clickedToOff = Signal()  # Signal emitted when the button is clicked and should return to the off state
		
	def __init__(self, parent=None):
		super().__init__(parent)
		self.off_state = True
		self.hovered = False
		self.sprite_sheet = QPixmap()
	
	def setSpriteImage(self, sprite_path):
		self.sprite_sheet = QPixmap(sprite_path)
		self.update()
	
	def paintEvent(self, event: QPaintEvent):
		painter = QPainter(self)
		painter.drawPixmap(self.rect(), self.getSpriteForState())
	
	def getSpriteForState(self) -> QPixmap:
		sprite_height = 20
		sprite_index = 0
		if self.isDown():
			sprite_index += 2
		elif self.off_state and self.hovered:
			sprite_index += 4
		return self.sprite_sheet.copy(0, sprite_index * sprite_height, self.width(), sprite_height)
	
	def enterEvent(self, event):
		if self.isEnabled() and not self.isDown():
			self.hovered = True
			self.update()
	
	def leaveEvent(self, event):
		if self.isEnabled() and not self.isDown():
			self.hovered = False
			self.update()
	
	def mouseReleaseEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton and self.isEnabled() and self.isDown():
			self.clickedToOff.emit()
			self.setDown(False)  # Reset the button state
			self.off_state = True
			self.hovered = False  # Set hovered to False to return to the initial state
			self.update()
		else:
			super().mouseReleaseEvent(event)

class NoteButton(QPushButton):
	clickedToOff = Signal()  # Signal emitted when the button is clicked and should return to the off state
	
	def __init__(self, parent=None):
		super().__init__(parent)
		self.off_state = True
		self.hovered = False
		self.sprite_sheet = QPixmap()
	
	def setSpriteImage(self, sprite_path):
		self.sprite_sheet = QPixmap(sprite_path)
		self.update()
	
	def paintEvent(self, event: QPaintEvent):
		painter = QPainter(self)
		painter.drawPixmap(self.rect(), self.getSpriteForState())
	
	def getSpriteForState(self) -> QPixmap:
		sprite_height = 20
		sprite_index = 0
		if self.isDown():
			sprite_index += 2
		elif self.off_state and self.hovered:
			sprite_index += 4
		return self.sprite_sheet.copy(0, sprite_index * sprite_height, self.width(), sprite_height)
	
	def enterEvent(self, event):
		if self.isEnabled() and not self.isDown():
			self.hovered = True
			self.update()
	
	def leaveEvent(self, event):
		if self.isEnabled() and not self.isDown():
			self.hovered = False
			self.update()
	
	def mousePressEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton and self.isEnabled():
			self.show_menu()
		else:
			super().mousePressEvent(event)
	
	def show_menu(self):
		# Create and show the menu at the button's position
		menu = SpriteMenu(self)
		menu.addActionWithSprite(resource_path("media/c.png"),  lambda: setstartingnote("C"))
		menu.addActionWithSprite(resource_path("media/c#.png"), lambda: setstartingnote("C#"))
		menu.addActionWithSprite(resource_path("media/d.png"),  lambda: setstartingnote("D"))
		menu.addActionWithSprite(resource_path("media/d#.png"), lambda: setstartingnote("D#"))
		menu.addActionWithSprite(resource_path("media/e.png"),  lambda: setstartingnote("E"))
		menu.addActionWithSprite(resource_path("media/f.png"),  lambda: setstartingnote("F"))
		menu.addActionWithSprite(resource_path("media/f#.png"), lambda: setstartingnote("F#"))
		menu.addActionWithSprite(resource_path("media/g.png"),  lambda: setstartingnote("G"))
		menu.addActionWithSprite(resource_path("media/g#.png"), lambda: setstartingnote("G#"))
		menu.addActionWithSprite(resource_path("media/a.png"),  lambda: setstartingnote("A"))
		menu.addActionWithSprite(resource_path("media/a#.png"), lambda: setstartingnote("A#"))
		menu.addActionWithSprite(resource_path("media/b.png"),  lambda: setstartingnote("B"))
		menu.exec(self.mapToGlobal(self.rect().bottomLeft()))
	
	def mouseReleaseEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton and self.isEnabled() and self.isDown():
			self.clickedToOff.emit()
			self.setDown(False)  # Reset the button state
			self.off_state = True
			self.hovered = False  # Set hovered to False to return to the initial state
			self.update()
		else:
			super().mouseReleaseEvent(event)

class NumberButton(QPushButton):
	clickedToOff = Signal()  # Signal emitted when the button is clicked and should return to the off state
	
	def __init__(self, parent=None):
		super().__init__(parent)
		self.off_state = True
		self.hovered = False
		self.sprite_sheet = QPixmap()
	
	def setSpriteImage(self, sprite_path):
		self.sprite_sheet = QPixmap(sprite_path)
		self.update()
	
	def paintEvent(self, event: QPaintEvent):
		painter = QPainter(self)
		painter.drawPixmap(self.rect(), self.getSpriteForState())
	
	def getSpriteForState(self) -> QPixmap:
		sprite_height = 20
		sprite_index = 0
		if self.isDown():
			sprite_index += 2
		elif self.off_state and self.hovered:
			sprite_index += 4
		return self.sprite_sheet.copy(0, sprite_index * sprite_height, self.width(), sprite_height)
	
	def enterEvent(self, event):
		if self.isEnabled() and not self.isDown():
			self.hovered = True
			self.update()
	
	def leaveEvent(self, event):
		if self.isEnabled() and not self.isDown():
			self.hovered = False
			self.update()
	
	def mousePressEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton and self.isEnabled():
			self.show_menu()
		else:
			super().mousePressEvent(event)
	
	def show_menu(self):
		# Create and show the menu at the button's position
		menu = SpriteMenu(self)
		menu.addActionWithSprite(resource_path("media/0.png"),  lambda: setstartingnumber(0))
		menu.addActionWithSprite(resource_path("media/1.png"),  lambda: setstartingnumber(1))
		menu.addActionWithSprite(resource_path("media/2.png"),  lambda: setstartingnumber(2))
		menu.addActionWithSprite(resource_path("media/3.png"),  lambda: setstartingnumber(3))
		menu.addActionWithSprite(resource_path("media/4.png"),  lambda: setstartingnumber(4))
		menu.addActionWithSprite(resource_path("media/5.png"),  lambda: setstartingnumber(5))
		menu.addActionWithSprite(resource_path("media/6.png"),  lambda: setstartingnumber(6))
		menu.addActionWithSprite(resource_path("media/7.png"),  lambda: setstartingnumber(7))
		menu.addActionWithSprite(resource_path("media/8.png"),  lambda: setstartingnumber(8))
		menu.addActionWithSprite(resource_path("media/9.png"),  lambda: setstartingnumber(9))
		menu.addActionWithSprite(resource_path("media/10.png"), lambda: setstartingnumber(10))
		menu.exec(self.mapToGlobal(self.rect().bottomLeft()))
	
	def mouseReleaseEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton and self.isEnabled() and self.isDown():
			self.clickedToOff.emit()
			self.setDown(False)  # Reset the button state
			self.off_state = True
			self.hovered = False  # Set hovered to False to return to the initial state
			self.update()
		else:
			super().mouseReleaseEvent(event)

class SkippedButton(QPushButton):
	clickedToOff = Signal()  # Signal emitted when the button is clicked and should return to the off state
	
	def __init__(self, parent=None):
		super().__init__(parent)
		self.off_state = True
		self.hovered = False
		self.sprite_sheet = QPixmap()
	
	def setSpriteImage(self, sprite_path):
		self.sprite_sheet = QPixmap(sprite_path)
		self.update()
	
	def paintEvent(self, event: QPaintEvent):
		painter = QPainter(self)
		painter.drawPixmap(self.rect(), self.getSpriteForState())
	
	def getSpriteForState(self) -> QPixmap:
		sprite_height = 20
		sprite_index = 0
		if self.isDown():
			sprite_index += 2
		elif self.off_state and self.hovered:
			sprite_index += 4
		return self.sprite_sheet.copy(0, sprite_index * sprite_height, self.width(), sprite_height)
	
	def enterEvent(self, event):
		if self.isEnabled() and not self.isDown():
			self.hovered = True
			self.update()
	
	def leaveEvent(self, event):
		if self.isEnabled() and not self.isDown():
			self.hovered = False
			self.update()
	
	def mousePressEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton and self.isEnabled():
			self.show_menu()
		else:
			super().mousePressEvent(event)
	
	def show_menu(self):
		# Create and show the menu at the button's position
		menu = SpriteMenu(self)
		menu.addActionWithSprite(resource_path("media/0.png"),  lambda: setskippednotes(0))
		menu.addActionWithSprite(resource_path("media/1.png"),  lambda: setskippednotes(1))
		menu.addActionWithSprite(resource_path("media/2.png"),  lambda: setskippednotes(2))
		menu.addActionWithSprite(resource_path("media/3.png"),  lambda: setskippednotes(3))
		menu.addActionWithSprite(resource_path("media/4.png"),  lambda: setskippednotes(4))
		menu.addActionWithSprite(resource_path("media/5.png"),  lambda: setskippednotes(5))
		menu.addActionWithSprite(resource_path("media/6.png"),  lambda: setskippednotes(6))
		menu.addActionWithSprite(resource_path("media/7.png"),  lambda: setskippednotes(7))
		menu.addActionWithSprite(resource_path("media/8.png"),  lambda: setskippednotes(8))
		menu.addActionWithSprite(resource_path("media/9.png"),  lambda: setskippednotes(9))
		menu.addActionWithSprite(resource_path("media/10.png"), lambda: setskippednotes(10))
		menu.exec(self.mapToGlobal(self.rect().bottomLeft()))
	
	def mouseReleaseEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton and self.isEnabled() and self.isDown():
			self.clickedToOff.emit()
			self.setDown(False)  # Reset the button state
			self.off_state = True
			self.hovered = False  # Set hovered to False to return to the initial state
			self.update()
		else:
			super().mouseReleaseEvent(event)

class VelocityButton(QPushButton):
	clickedToOff = Signal()  # Signal emitted when the button is clicked and should return to the off state
	
	def __init__(self, parent=None):
		super().__init__(parent)
		self.off_state = True
		self.hovered = False
		self.sprite_sheet = QPixmap()
	
	def setSpriteImage(self, sprite_path):
		self.sprite_sheet = QPixmap(sprite_path)
		self.update()
	
	def paintEvent(self, event: QPaintEvent):
		painter = QPainter(self)
		painter.drawPixmap(self.rect(), self.getSpriteForState())
	
	def getSpriteForState(self) -> QPixmap:
		sprite_height = 20
		sprite_index = 0
		if self.isDown():
			sprite_index += 2
		elif self.off_state and self.hovered:
			sprite_index += 4
		return self.sprite_sheet.copy(0, sprite_index * sprite_height, self.width(), sprite_height)
	
	def enterEvent(self, event):
		if self.isEnabled() and not self.isDown():
			self.hovered = True
			self.update()
	
	def leaveEvent(self, event):
		if self.isEnabled() and not self.isDown():
			self.hovered = False
			self.update()
	
	def mousePressEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton and self.isEnabled():
			self.show_menu()
		else:
			super().mousePressEvent(event)
	
	def show_menu(self):
		# Create and show the menu at the button's position
		menu = SpriteMenu(self)
		menu.addActionWithSprite(resource_path("media/1.png"),  lambda: setvelocitylayers(1))
		menu.addActionWithSprite(resource_path("media/2.png"),  lambda: setvelocitylayers(2))
		menu.addActionWithSprite(resource_path("media/3.png"),  lambda: setvelocitylayers(3))
		menu.addActionWithSprite(resource_path("media/4.png"),  lambda: setvelocitylayers(4))
		menu.addActionWithSprite(resource_path("media/5.png"),  lambda: setvelocitylayers(5))
		menu.addActionWithSprite(resource_path("media/6.png"),  lambda: setvelocitylayers(6))
		menu.addActionWithSprite(resource_path("media/7.png"),  lambda: setvelocitylayers(7))
		menu.addActionWithSprite(resource_path("media/8.png"),  lambda: setvelocitylayers(8))
		menu.addActionWithSprite(resource_path("media/9.png"),  lambda: setvelocitylayers(9))
		menu.addActionWithSprite(resource_path("media/10.png"), lambda: setvelocitylayers(10))
		menu.exec(self.mapToGlobal(self.rect().bottomLeft()))
	
	def mouseReleaseEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton and self.isEnabled() and self.isDown():
			self.clickedToOff.emit()
			self.setDown(False)  # Reset the button state
			self.off_state = True
			self.hovered = False  # Set hovered to False to return to the initial state
			self.update()
		else:
			super().mouseReleaseEvent(event)

class DirectionButton(QPushButton):
	clickedToOff = Signal()  # Signal emitted when the button is clicked and should return to the off state
	
	def __init__(self, parent=None):
		super().__init__(parent)
		self.off_state = True
		self.hovered = False
		self.sprite_sheet = QPixmap()
	
	def setSpriteImage(self, sprite_path):
		self.sprite_sheet = QPixmap(sprite_path)
		self.update()
	
	def paintEvent(self, event: QPaintEvent):
		painter = QPainter(self)
		painter.drawPixmap(self.rect(), self.getSpriteForState())
	
	def getSpriteForState(self) -> QPixmap:
		sprite_height = 20
		sprite_index = 0
		if self.isDown():
			sprite_index += 2
		elif self.off_state and self.hovered:
			sprite_index += 4
		return self.sprite_sheet.copy(0, sprite_index * sprite_height, self.width(), sprite_height)
	
	def enterEvent(self, event):
		if self.isEnabled() and not self.isDown():
			self.hovered = True
			self.update()
	
	def leaveEvent(self, event):
		if self.isEnabled() and not self.isDown():
			self.hovered = False
			self.update()
	
	def mousePressEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton and self.isEnabled():
			self.show_menu()
		else:
			super().mousePressEvent(event)
	
	def show_menu(self):
		# Create and show the menu at the button's position
		menu = SpriteMenu(self)
		menu.addActionWithSprite(resource_path("media/ascending.png"),  lambda: setvelocitydirection(True))
		menu.addActionWithSprite(resource_path("media/descending.png"),  lambda: setvelocitydirection(False))
		menu.exec(self.mapToGlobal(self.rect().bottomLeft()))
	
	def mouseReleaseEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton and self.isEnabled() and self.isDown():
			self.clickedToOff.emit()
			self.setDown(False)  # Reset the button state
			self.off_state = True
			self.hovered = False  # Set hovered to False to return to the initial state
			self.update()
		else:
			super().mouseReleaseEvent(event)



class RoundRobinsButton(QPushButton):
	clickedToOff = Signal()  # Signal emitted when the button is clicked and should return to the off state
	
	def __init__(self, parent=None):
		super().__init__(parent)
		self.off_state = True
		self.hovered = False
		self.sprite_sheet = QPixmap()
	
	def setSpriteImage(self, sprite_path):
		self.sprite_sheet = QPixmap(sprite_path)
		self.update()
	
	def paintEvent(self, event: QPaintEvent):
		painter = QPainter(self)
		painter.drawPixmap(self.rect(), self.getSpriteForState())
	
	def getSpriteForState(self) -> QPixmap:
		sprite_height = 20
		sprite_index = 0
		if self.isDown():
			sprite_index += 2
		elif self.off_state and self.hovered:
			sprite_index += 4
		return self.sprite_sheet.copy(0, sprite_index * sprite_height, self.width(), sprite_height)
	
	def enterEvent(self, event):
		if self.isEnabled() and not self.isDown():
			self.hovered = True
			self.update()
	
	def leaveEvent(self, event):
		if self.isEnabled() and not self.isDown():
			self.hovered = False
			self.update()
	
	def mousePressEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton and self.isEnabled():
			self.show_menu()
		else:
			super().mousePressEvent(event)
	
	def show_menu(self):
		# Create and show the menu at the button's position
		menu = SpriteMenu(self)
		menu.addActionWithSprite(resource_path("media/1.png"),  lambda: setroundrobins(1))
		menu.addActionWithSprite(resource_path("media/2.png"),  lambda: setroundrobins(2))
		menu.addActionWithSprite(resource_path("media/3.png"),  lambda: setroundrobins(3))
		menu.addActionWithSprite(resource_path("media/4.png"),  lambda: setroundrobins(4))
		menu.addActionWithSprite(resource_path("media/5.png"),  lambda: setroundrobins(5))
		menu.addActionWithSprite(resource_path("media/6.png"),  lambda: setroundrobins(6))
		menu.addActionWithSprite(resource_path("media/7.png"),  lambda: setroundrobins(7))
		menu.addActionWithSprite(resource_path("media/8.png"),  lambda: setroundrobins(8))
		menu.addActionWithSprite(resource_path("media/9.png"),  lambda: setroundrobins(9))
		menu.addActionWithSprite(resource_path("media/10.png"), lambda: setroundrobins(10))
		menu.exec(self.mapToGlobal(self.rect().bottomLeft()))
	
	def mouseReleaseEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton and self.isEnabled() and self.isDown():
			self.clickedToOff.emit()
			self.setDown(False)  # Reset the button state
			self.off_state = True
			self.hovered = False  # Set hovered to False to return to the initial state
			self.update()
		else:
			super().mouseReleaseEvent(event)

class SignalTracksButton(QPushButton):
	clickedToOff = Signal()  # Signal emitted when the button is clicked and should return to the off state
	
	def __init__(self, parent=None):
		super().__init__(parent)
		self.off_state = True
		self.hovered = False
		self.sprite_sheet = QPixmap()
	
	def setSpriteImage(self, sprite_path):
		self.sprite_sheet = QPixmap(sprite_path)
		self.update()
	
	def paintEvent(self, event: QPaintEvent):
		painter = QPainter(self)
		painter.drawPixmap(self.rect(), self.getSpriteForState())
	
	def getSpriteForState(self) -> QPixmap:
		sprite_height = 20
		sprite_index = 0
		if self.isDown():
			sprite_index += 2
		elif self.off_state and self.hovered:
			sprite_index += 4
		return self.sprite_sheet.copy(0, sprite_index * sprite_height, self.width(), sprite_height)
	
	def enterEvent(self, event):
		if self.isEnabled() and not self.isDown():
			self.hovered = True
			self.update()
	
	def leaveEvent(self, event):
		if self.isEnabled() and not self.isDown():
			self.hovered = False
			self.update()
	
	def mousePressEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton and self.isEnabled():
			self.show_menu()
		else:
			super().mousePressEvent(event)
	
	def show_menu(self):
		# Create and show the menu at the button's position
		menu = SpriteMenu(self)
		menu.addActionWithSprite(resource_path("media/1.png"),  lambda: setsignaltracks(1))
		menu.addActionWithSprite(resource_path("media/2.png"),  lambda: setsignaltracks(2))
		menu.addActionWithSprite(resource_path("media/3.png"),  lambda: setsignaltracks(3))
		menu.addActionWithSprite(resource_path("media/4.png"),  lambda: setsignaltracks(4))
		menu.addActionWithSprite(resource_path("media/5.png"),  lambda: setsignaltracks(5))
		menu.addActionWithSprite(resource_path("media/6.png"),  lambda: setsignaltracks(6))
		menu.addActionWithSprite(resource_path("media/7.png"),  lambda: setsignaltracks(7))
		menu.addActionWithSprite(resource_path("media/8.png"),  lambda: setsignaltracks(8))
		menu.addActionWithSprite(resource_path("media/9.png"),  lambda: setsignaltracks(9))
		menu.addActionWithSprite(resource_path("media/10.png"), lambda: setsignaltracks(10))
		menu.exec(self.mapToGlobal(self.rect().bottomLeft()))
	
	def mouseReleaseEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton and self.isEnabled() and self.isDown():
			self.clickedToOff.emit()
			self.setDown(False)  # Reset the button state
			self.off_state = True
			self.hovered = False  # Set hovered to False to return to the initial state
			self.update()
		else:
			super().mouseReleaseEvent(event)


class SpriteMenu(QMenu):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setFixedWidth(40)
	
	def addActionWithSprite(self, sprite, action_slot):
		action = self.addAction("")
		action.setIcon(QIcon(sprite))
		action.triggered.connect(action_slot)
	
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHints(QPainter.RenderHint.Antialiasing)
	
		for action in self.actions():
			rect = self.actionGeometry(action)
	
			pixmap = action.icon().pixmap(40, 20)
			painter.drawPixmap(rect.x(), rect.y(), pixmap)

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
	
		self.setWindowTitle("samplesidekick")
		self.setGeometry(0, 0, 960, 540)
	
		self.intro_video_path = resource_path("media/intro.mp4")
		self.day_video_path = resource_path("media/day.mp4")
		self.night_video_path = resource_path("media/night.mp4")
	
		self.video_window = VideoWindow(self.intro_video_path, self.day_video_path, self.night_video_path)
		self.setCentralWidget(self.video_window)
	
		# Set the window flags to disable resizing
		self.setFixedSize(self.size())
	
		self.video_window.startingnote_button.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
		self.video_window.startingnote_button.clicked.connect(self.context_menu_requested)
	
		# Center the window on the screen
		self.center()
	
	def center(self):
		# Get the screen geometry
		screen = QApplication.primaryScreen().geometry()
	
		# Calculate the center point
		x = (screen.width() - self.width()) // 2
		y = (screen.height() - self.height()) // 2
	
		# Move the window to the center
		self.move(x, y)
	
	def context_menu_requested(self):
		self.menu.exec(self.video_window.startingnote_button.mapToGlobal(self.video_window.startingnote_button.pos()))
		
# Animated progress bar

class AnimatedSprite:
	def __init__(self, parent, darkness):
		self.parent = parent
		self.sprite_height = 35
		self.total_frames = 95
		self.current_frame = 0
		
		if darkness:
			spritesheet_path = resource_path("media/progressnight.png")
		else:
			spritesheet_path = resource_path("media/progresslight.png")
			
		self.label = QLabel(parent)
		self.label.setGeometry(0, 0, 765, self.sprite_height)
		
		self.spritesheet = QPixmap(spritesheet_path)
		
		self.timer = QTimer(parent)
		self.timer.timeout.connect(self.update_frame)
	
	def start_animation(self, darkness):
		if darkness:
			spritesheet_path = resource_path("media/progressnight.png")
		else:
			spritesheet_path = resource_path("media/progresslight.png")
			
		self.spritesheet = QPixmap(spritesheet_path)  # Update the spritesheet path based on current darkness value
		
		self.current_frame = 0
		self.timer.start(30)
	
	def update_frame(self):
		if self.current_frame < self.total_frames:
			y_offset = self.current_frame * self.sprite_height
			self.label.setPixmap(self.spritesheet.copy(0, y_offset, 765, self.sprite_height))
			self.current_frame += 1
		else:
			self.label.clear()
			self.timer.stop()
	
# Spawn the actual instance of the app and its window

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	
	def setstartingnote(n):
		global startingnote
		startingnote = n
		window.video_window.startingnote_button.setSpriteImage(resource_path("media/"+str(startingnote)+".png"))
		
	def setstartingnumber(n):
		global startingnumber
		startingnumber = n
		window.video_window.startingnumber_button.setSpriteImage(resource_path("media/"+str(startingnumber)+".png"))
	
	def setskippednotes(n):
		global skippednotes
		skippednotes = n
		window.video_window.skippednotes_button.setSpriteImage(resource_path("media/"+str(skippednotes)+".png"))
	
	def setvelocitylayers(n):
		global velocitylayers
		velocitylayers = n
		window.video_window.velocitylayers_button.setSpriteImage(resource_path("media/"+str(velocitylayers)+".png"))
		
	def setvelocitydirection(n):
		global velocitydirection
		velocitydirection = n
		if n == True:
			window.video_window.velocitydirection_button.setSpriteImage(resource_path("media/ascending.png"))
		else:
			window.video_window.velocitydirection_button.setSpriteImage(resource_path("media/descending.png"))
		
	def setroundrobins(n):
		global roundrobins
		roundrobins = n
		window.video_window.roundrobins_button.setSpriteImage(resource_path("media/"+str(roundrobins)+".png"))
		
	def setsignaltracks(n):
		global signaltracks
		signaltracks = n
		window.video_window.signaltracks_button.setSpriteImage(resource_path("media/"+str(signaltracks)+".png"))
	
	def samplerename(signaltracks, startingnote, startingnumber, skippednotes, velocitylayers, roundrobins, chromaticscale, velocitydivisions, roundrobindict, signaltracksdict, original_directory, new_directory, velocitydirection):
		
		if original_directory == "":
			original_error_dialog = ImageDialog(resource_path("media/errorsampledirectory.png"))
			original_error_dialog.exec()
		
		elif new_directory == "":
			new_directory_error_dialog = ImageDialog(resource_path("media/erroroutputdirectory.png"))
			new_directory_error_dialog.exec()

		else:
				
			window.video_window.playprogress()
			
			files = os.listdir(original_directory)
			files = [filename for filename in files if filename.split('.')[0].isdigit()]
			files.sort(key=lambda x: int(x.split('.')[0])) # sort by number, not by name
			
			starting_note_index = chromaticscale.index(f'{startingnote}{startingnumber}')
	
			note_names = chromaticscale[starting_note_index::skippednotes+1]
			round_robin_names = roundrobindict[roundrobins]
			track_names = signaltracksdict[signaltracks]
			
			if velocitydirection == True:
				velocity_names = velocitydivisions[velocitylayers]
			else:
				velocity_names = velocitydivisionsdescending[velocitylayers]
	
			product_names = product(note_names, velocity_names, round_robin_names, track_names)
	
			for file, (note_name, velocity_name, round_robin_name, track_name) in zip(files, product_names):

				# Build the new name with the appropriate note, velocity layer, and round robin
				final_name = ' '.join((track_name.strip(), note_name.strip(), velocity_name.strip(), round_robin_name.strip()))

				# Build the full paths for the old and new names
				old_path = os.path.join(original_directory, file)
				new_path = os.path.join(new_directory, final_name.strip()+'.'+file.split('.')[-1])
				shutil.copy2(old_path, new_path)

										
	sys.exit(app.exec())