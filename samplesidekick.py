"""This program is free software: you can redistribute it and/or modify
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

special thanks to: finn foley for giving me a reason to get this thing
finished already, moonriver for being so chill about me being super
obsessed with stuff like this, guy white for encouraging me to get
this onto github (and for maybe helping me solve the naming issue?
come on guy, you're our only hope in these trying times), zena and
drew for believing i was capable of doing stuff like this before i
ever did stuff like this, and you dear reader for reading this.
nobody ever reads this stuff.

ty, kady <3

"""

# We import all the libraries we need to rename files, have a flashy video GUI, play a fake progress bar video, etc

import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QMenu
from PyQt6.QtCore import QTimer, Qt, pyqtSignal, QUrl
from PyQt6.QtGui import QPixmap, QImage, QAction, QPainter, QPaintEvent, QIcon, QColor, QBrush
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
import cv2
import platform
import subprocess
import shutil
from itertools import cycle, islice

# Define all the little pieces of the final sample filenames

chromaticscale = ["C0", "C#0", "D0", "D#0", "E0", "F0", "F#0", "G0", "G#0", "A0", "A#0", "B0", "C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1", "G#1", "A1", "A#1", "B1", "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2", "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3", "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4", "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5", "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6", "C7", "C#7", "D7", "D#7", "E7", "F7", "F#7", "G7", "G#7", "A7", "A#7", "B7", "C8", "C#8", "D8", "D#8", "E8", "F8", "F#8", "G8", "G#8", "A8", "A#8", "B8", "C9", "C#9", "D9", "D#9", "E9", "F9", "F#9", "G9", "G#9", "A9", "A#9", "B9"]

velocitydivisions = {
10: [" 1 13 ", " 14 25 ", " 26 38 ", " 39 51 ", " 52 64 ", " 65 76 ", " 77 89 ", " 90 102 ", " 103 114 ", " 115 127 "],
9: [" 1 14 ", " 15 28 ", " 29 42 ", " 43 56 ", " 57 71 ", " 72 85 ", " 86 99 ", " 100 113 ", " 114 127 "],
8: [" 1 16 ", " 17 32 ", "33 48", "49 64", "65 79", "80 95", "96 111", "112 127"],
7: [" 1 18 ", " 19 36 ", " 37 54 ", " 55 73 ", " 74 91 ", " 92 109 ", " 110 127 "],
6: [" 1 21 ", " 22 42 ", " 43 64 ", " 65 85 ", " 86 106 ", " 107 127 "],
5: [" 1 25 ", " 26 51 ", " 52 76 ", " 77 102 ", " 103 127 "],
4: [" 1 32 ", " 33 64 ", " 65 95 ", " 96 127 "],
3: [" 1 42 ", " 43 85 ", " 86 127 "],
2: [" 1 64 ", " 65 127 "],
1: [""]
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

# Declare the options variables

startingnote = "C"
startingnumber = 3
skippednotes = 0
velocitylayers = 1
roundrobins = 1
startingnoteandnumber = startingnote + str(startingnumber)

# Define the way to draw the directory location text

class RightAlignedLabel(QLabel):
	def paintEvent(self, event):
		painter = QPainter(self)
		rect = self.contentsRect()
		elided_text = painter.fontMetrics().elidedText(self.text(), Qt.TextElideMode.ElideLeft, rect.width())
		painter.drawText(rect, Qt.AlignmentFlag.AlignRight, elided_text)

# Define the main window (This is where most of the application logic is including the renaming routine)

class VideoWindow(QMainWindow):
	def __init__(self, intro_video_path, day_video_path, night_video_path):
		super().__init__()

		# Create a label to display the video frames
		self.video_label = QLabel(self)
		self.video_label.setGeometry(0, 0, 960, 540)
		self.setCentralWidget(self.video_label)
		
		# Create a QLabel widget for the fake progress bar video display
		self.video_label2 = QLabel(self)
		self.video_label2.setGeometry(162, 142, 765, 35)  # Adjust the position and size
		
		# Create a QMediaPlayer instance
		self.media_player = QMediaPlayer()
		self.media_player.setVideoOutput(self.video_label2)

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
		self.target_directory_button.setGeometry(90, 464, 84, 20)
		self.target_directory_button.setFixedSize(84, 20)
		self.target_directory_button.setText("Select Target Directory")
		self.target_directory_button.setSpriteImage("media/selectsprite.png")
		self.target_directory_button.clickedToOff.connect(self.select_target_directory)
		self.target_directory_button.hide()

		self.destination_directory_button = SpriteButton(self)
		self.destination_directory_button.setGeometry(373, 464, 84, 20)
		self.destination_directory_button.setFixedSize(84, 20)
		self.destination_directory_button.setSpriteImage("media/selectsprite.png")
		self.destination_directory_button.setText("Select Destination Directory")
		self.destination_directory_button.clickedToOff.connect(self.select_destination_directory)
		self.destination_directory_button.hide()

		# Create the rename button
		self.rename_button = SpriteButton(self)
		self.rename_button.setGeometry(845, 185, 84, 20)
		self.rename_button.setFixedSize(84, 20)
		self.rename_button.setSpriteImage("media/startsprite.png")
		self.rename_button.setText("Rename")
		self.rename_button.clickedToOff.connect(self.samplerename)
		self.rename_button.hide()
		
		# Create the starting note button
		self.startingnote_button = NoteButton(self)
		self.startingnote_button.setGeometry(845, 292, 40, 20)
		self.startingnote_button.setFixedSize(40,20)
		self.startingnote_button.setSpriteImage("media/ddbutton.png")
		self.startingnote_button.setText("Starting Note")
		self.startingnote_button.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
		self.startingnote_button.hide()

		# Create the starting note number button
		self.startingnumber_button = NumberButton(self)
		self.startingnumber_button.setGeometry(895, 292, 40, 20)
		self.startingnumber_button.setFixedSize(40,20)
		self.startingnumber_button.setSpriteImage("media/ddbutton.png")
		self.startingnumber_button.setText("Starting Note Number")
		self.startingnumber_button.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
		self.startingnumber_button.hide()
		
		# Create the skipped notes button
		self.skippednotes_button = SkippedButton(self)
		self.skippednotes_button.setGeometry(845, 329, 40, 20)
		self.skippednotes_button.setFixedSize(40,20)
		self.skippednotes_button.setSpriteImage("media/ddbutton.png")
		self.skippednotes_button.setText("Skipped Notes")
		self.skippednotes_button.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
		self.skippednotes_button.hide()
		
		# Create the velocity layers button
		self.velocitylayers_button = VelocityButton(self)
		self.velocitylayers_button.setGeometry(845, 365, 40, 20)
		self.velocitylayers_button.setFixedSize(40,20)
		self.velocitylayers_button.setSpriteImage("media/ddbutton.png")
		self.velocitylayers_button.setText("Skipped Notes")
		self.velocitylayers_button.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
		self.velocitylayers_button.hide()

		# Create the round robins button
		self.roundrobins_button = RoundRobinsButton(self)
		self.roundrobins_button.setGeometry(845, 401, 40, 20)
		self.roundrobins_button.setFixedSize(40,20)
		self.roundrobins_button.setSpriteImage("media/ddbutton.png")
		self.roundrobins_button.setText("Skipped Notes")
		self.roundrobins_button.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
		self.roundrobins_button.hide()

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
			self.startingnote_button.show()
			self.startingnumber_button.show()
			self.skippednotes_button.show()
			self.velocitylayers_button.show()
			self.roundrobins_button.show()
		else:
			# Hide the buttons during the intro video playback
			self.target_directory.hide()
			self.destination_directory.hide()
			self.target_directory_button.hide()
			self.destination_directory_button.hide()
			self.rename_button.hide()
			self.startingnote_button.hide()
			self.startingnumber_button.hide()
			self.skippednotes_button.hide()
			self.velocitylayers_button.hide()
			self.roundrobins_button.hide()
	
	
	def handle_dark_mode_change(self):
		if self.transition_to_main:
			self.transition_to_main = False
			self.start_main_video()
	
	def select_target_directory(self):
		directory = QFileDialog.getExistingDirectory(self, "Select Target Directory")
		self.target_directory.setText(directory)
	
	def select_destination_directory(self):
		directory = QFileDialog.getExistingDirectory(self, "Select Destination Directory")
		self.destination_directory.setText(directory)
	
	def hide_buttons(self):
		self.target_directory_button.hide()
		self.destination_directory_button.hide()
		
	def play_video(self, video_path):
		self.media_player.setSource(QUrl.fromLocalFile(video_path))
		
		# Set the size and position of the video label
		width = 765
		height = 35
		self.video_label2.resize(width, height)
		self.video_label2.move(162, 142)  # Adjust the desired position
		
		# Adjust the stacking order of the video label
		self.video_label2.raise_()
		
		# Start the video playback
		self.media_player.play()

	# Run the rename function with the target and destination directories
	def samplerename(self):
			
		global startingnote
		global startingnumber
		notenumber = startingnumber
		global skippednotes
		global velocitylayers
		global roundrobins
		
		if self.is_dark_mode():
			video_path = "media/progressnight.mp4"
		else:
			video_path = "media/progresslight.mp4"
			
		self.play_video(video_path)
		
		# Path to the directory containing the files
		original_directory = self.target_directory.text()
		
		# Path to the directory where renamed files will be saved
		new_directory = self.destination_directory.text()
		
		if not os.path.exists(new_directory):
			os.makedirs(new_directory)
		
		files = os.listdir(original_directory)
		files.sort()
		
		starting_index = chromaticscale.index(startingnoteandnumber)
		
		# Handle first file
		first_file = files.pop(0)
		first_file_name, first_file_extension = os.path.splitext(first_file)
		for v in range(velocitylayers):
			for r in range(roundrobins):
				round_robin_name = roundrobindict[roundrobins][r]
				velocity_name = velocitydivisions[velocitylayers][v]
				final_name = startingnoteandnumber + velocity_name + round_robin_name + first_file_extension
				old_path = os.path.join(original_directory, first_file)
				new_path = os.path.join(new_directory, final_name)
				shutil.copy2(old_path, new_path)
		
		# Handle remaining files
		for v in range(velocitylayers):
			for r in range(roundrobins):
				round_robin_name = roundrobindict[roundrobins][r]
				velocity_name = velocitydivisions[velocitylayers][v]
				for file, note in zip(files, chromaticscale[starting_index::skippednotes+1]):
					filename, file_extension = os.path.splitext(file)
		
					# Build the new name with the appropriate note, velocity layer, and round robin
					final_name = note + velocity_name + round_robin_name + file_extension
		
					# Build the full paths for the old and new names
					old_path = os.path.join(original_directory, file)
					new_path = os.path.join(new_directory, final_name)
		
					# Copy the file to the new directory with the new name
					shutil.copy2(old_path, new_path)


# Define the sprite based buttons
		
class SpriteButton(QPushButton):
	clickedToOff = pyqtSignal()  # Signal emitted when the button is clicked and should return to the off state
		
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
	clickedToOff = pyqtSignal()  # Signal emitted when the button is clicked and should return to the off state
	
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
		menu.addActionWithSprite("media/c.png",  lambda: setstartingnote("C"))
		menu.addActionWithSprite("media/c#.png", lambda: setstartingnote("C#"))
		menu.addActionWithSprite("media/d.png",  lambda: setstartingnote("D"))
		menu.addActionWithSprite("media/d#.png", lambda: setstartingnote("D#"))
		menu.addActionWithSprite("media/e.png",  lambda: setstartingnote("E"))
		menu.addActionWithSprite("media/f.png",  lambda: setstartingnote("F"))
		menu.addActionWithSprite("media/f#.png", lambda: setstartingnote("F#"))
		menu.addActionWithSprite("media/g.png",  lambda: setstartingnote("G"))
		menu.addActionWithSprite("media/g#.png", lambda: setstartingnote("G#"))
		menu.addActionWithSprite("media/a.png",  lambda: setstartingnote("A"))
		menu.addActionWithSprite("media/a#.png", lambda: setstartingnote("A#"))
		menu.addActionWithSprite("media/b.png",  lambda: setstartingnote("B"))
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
	clickedToOff = pyqtSignal()  # Signal emitted when the button is clicked and should return to the off state
	
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
		menu.addActionWithSprite("media/0.png",  lambda: setstartingnumber(0))
		menu.addActionWithSprite("media/1.png",  lambda: setstartingnumber(1))
		menu.addActionWithSprite("media/2.png",  lambda: setstartingnumber(2))
		menu.addActionWithSprite("media/3.png",  lambda: setstartingnumber(3))
		menu.addActionWithSprite("media/4.png",  lambda: setstartingnumber(4))
		menu.addActionWithSprite("media/5.png",  lambda: setstartingnumber(5))
		menu.addActionWithSprite("media/6.png",  lambda: setstartingnumber(6))
		menu.addActionWithSprite("media/7.png",  lambda: setstartingnumber(7))
		menu.addActionWithSprite("media/8.png",  lambda: setstartingnumber(8))
		menu.addActionWithSprite("media/9.png",  lambda: setstartingnumber(9))
		menu.addActionWithSprite("media/10.png", lambda: setstartingnumber(10))
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
	clickedToOff = pyqtSignal()  # Signal emitted when the button is clicked and should return to the off state
	
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
		menu.addActionWithSprite("media/0.png",  lambda: setskippednotes(0))
		menu.addActionWithSprite("media/1.png",  lambda: setskippednotes(1))
		menu.addActionWithSprite("media/2.png",  lambda: setskippednotes(2))
		menu.addActionWithSprite("media/3.png",  lambda: setskippednotes(3))
		menu.addActionWithSprite("media/4.png",  lambda: setskippednotes(4))
		menu.addActionWithSprite("media/5.png",  lambda: setskippednotes(5))
		menu.addActionWithSprite("media/6.png",  lambda: setskippednotes(6))
		menu.addActionWithSprite("media/7.png",  lambda: setskippednotes(7))
		menu.addActionWithSprite("media/8.png",  lambda: setskippednotes(8))
		menu.addActionWithSprite("media/9.png",  lambda: setskippednotes(9))
		menu.addActionWithSprite("media/10.png", lambda: setskippednotes(10))
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
	clickedToOff = pyqtSignal()  # Signal emitted when the button is clicked and should return to the off state
	
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
		menu.addActionWithSprite("media/1.png",  lambda: setvelocitylayers(1))
		menu.addActionWithSprite("media/2.png",  lambda: setvelocitylayers(2))
		menu.addActionWithSprite("media/3.png",  lambda: setvelocitylayers(3))
		menu.addActionWithSprite("media/4.png",  lambda: setvelocitylayers(4))
		menu.addActionWithSprite("media/5.png",  lambda: setvelocitylayers(5))
		menu.addActionWithSprite("media/6.png",  lambda: setvelocitylayers(6))
		menu.addActionWithSprite("media/7.png",  lambda: setvelocitylayers(7))
		menu.addActionWithSprite("media/8.png",  lambda: setvelocitylayers(8))
		menu.addActionWithSprite("media/9.png",  lambda: setvelocitylayers(9))
		menu.addActionWithSprite("media/10.png", lambda: setvelocitylayers(10))
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
	clickedToOff = pyqtSignal()  # Signal emitted when the button is clicked and should return to the off state
	
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
		menu.addActionWithSprite("media/1.png",  lambda: setroundrobins(1))
		menu.addActionWithSprite("media/2.png",  lambda: setroundrobins(2))
		menu.addActionWithSprite("media/3.png",  lambda: setroundrobins(3))
		menu.addActionWithSprite("media/4.png",  lambda: setroundrobins(4))
		menu.addActionWithSprite("media/5.png",  lambda: setroundrobins(5))
		menu.addActionWithSprite("media/6.png",  lambda: setroundrobins(6))
		menu.addActionWithSprite("media/7.png",  lambda: setroundrobins(7))
		menu.addActionWithSprite("media/8.png",  lambda: setroundrobins(8))
		menu.addActionWithSprite("media/9.png",  lambda: setroundrobins(9))
		menu.addActionWithSprite("media/10.png", lambda: setroundrobins(10))
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
	
		self.intro_video_path = "media/intro.mp4"
		self.day_video_path = "media/day.mp4"
		self.night_video_path = "media/night.mp4"
	
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
		

# Spawn the actual instance of the app and its window

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	
	def setstartingnote(n):
		global startingnote
		startingnote = n
		window.video_window.startingnote_button.setSpriteImage("media/"+str(startingnote)+".png")
		
	def setstartingnumber(n):
		global startingnumber
		startingnumber = n
		window.video_window.startingnumber_button.setSpriteImage("media/"+str(startingnumber)+".png")
	
	def setskippednotes(n):
		global skippednotes
		skippednotes = n
		window.video_window.skippednotes_button.setSpriteImage("media/"+str(skippednotes)+".png")
	
	def setvelocitylayers(n):
		global velocitylayers
		velocitylayers = n
		window.video_window.velocitylayers_button.setSpriteImage("media/"+str(velocitylayers)+".png")
		
	def setroundrobins(n):
		global roundrobins
		roundrobins = n
		window.video_window.roundrobins_button.setSpriteImage("media/"+str(roundrobins)+".png")

	sys.exit(app.exec())