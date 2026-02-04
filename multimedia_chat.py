#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 16:04:06 2025

@author: russ
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------






# ---- eof

from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys
from PyQt5.QtWidgets import QApplication


def play_sound(file_path, wait=True):
    """
    Play a sound file using QMediaPlayer.

    Args:
        file_path (str): Path to the sound file
        wait (bool): Whether to wait for the sound to finish playing
    """
    app = QApplication.instance() or QApplication(sys.argv)

    player = QMediaPlayer()
    player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
    player.play()

    if wait:
        # Simple wait loop to keep the application running while playing
        while player.state() == QMediaPlayer.PlayingState:
            app.processEvents()


def play_sound_with_callback(file_path, callback=None):
    """
    Play a sound file using QMediaPlayer and execute a callback when finished.

    Args:
        file_path (str): Path to the sound file
        callback (function): Function to call when sound finishes
    """
    app = QApplication.instance() or QApplication(sys.argv)

    player = QMediaPlayer()
    player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))

    if callback:
        player.stateChanged.connect(lambda state:
            callback() if state == QMediaPlayer.StoppedState else None)

    player.play()

    # Return the player object so it doesn't get garbage collected
    return player


def play_multiple_sounds(file_paths, interval=500):
    """
    Play multiple sound files in sequence with a specified interval between them.

    Args:
        file_paths (list): List of paths to sound files
        interval (int): Interval between sounds in milliseconds
    """
    app = QApplication.instance() or QApplication(sys.argv)

    player = QMediaPlayer()
    current_index = [0]  # Using list to allow modification in nested function

    def play_next():
        if current_index[0] < len(file_paths):
            player.setMedia(QMediaContent(QUrl.fromLocalFile(file_paths[current_index[0]])))
            player.play()
            current_index[0] += 1
            QTimer.singleShot(interval, play_next)

    play_next()
    return player


def beep(frequency=440, duration=500):
    """
    Creates and plays a beep sound using a generated WAV file.
    This is a workaround since QMediaPlayer doesn't generate tones directly.

    Args:
        frequency (int): Frequency in Hz
        duration (int): Duration in milliseconds

    Note: Requires numpy and wave modules
    """
    import numpy as np
    import wave
    import tempfile
    import os

    # Create a temporary WAV file
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    temp_file.close()

    # Generate sine wave data
    sample_rate = 44100
    t = np.linspace(0, duration/1000, int(sample_rate * duration/1000), False)
    tone = np.sin(frequency * t * 2 * np.pi)
    tone = (tone * 32767).astype(np.int16)

    # Write to WAV file
    with wave.open(temp_file.name, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(tone.tobytes())

    # Play the sound
    app = QApplication.instance() or QApplication(sys.argv)
    player = QMediaPlayer()
    player.setMedia(QMediaContent(QUrl.fromLocalFile(temp_file.name)))
    player.play()

    # Set up cleanup
    def cleanup():
        if player.state() == QMediaPlayer.StoppedState:
            try:
                os.unlink(temp_file.name)
            except:
                pass

    player.stateChanged.connect(cleanup)

    return player


class SoundPlayer:
    """
    A reusable class for playing sounds with QMediaPlayer.
    """
    def __init__(self):
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.player = QMediaPlayer()

    def play(self, file_path, volume=100):
        """Play a sound file with specified volume"""
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.player.setVolume(volume)
        self.player.play()

    def stop(self):
        """Stop the currently playing sound"""
        self.player.stop()

    def is_playing(self):
        """Check if sound is currently playing"""
        return self.player.state() == QMediaPlayer.PlayingState


# Basic usage - play a sound file
#play_sound( "/mnt/WIN_D/russ/0000/python00/python3/_projects/rsh/NickOfTime10.mp3" )

# # Play with callback when done
# def on_sound_finished():
#     print("Sound playback completed!")

# player = play_sound_with_callback("/path/to/mysound.mp3", on_sound_finished)

# # Play a sequence of sounds
# sound_files = [
#     "/path/to/sound1.mp3",
#     "/path/to/sound2.mp3",
#     "/path/to/sound3.mp3"
# ]
# player = play_multiple_sounds(sound_files, interval=1000)  # 1 second between sounds

# Play a beep tone
player = beep(440, 5000 )  # 440 Hz for 500 ms

# # Using the SoundPlayer class
# sound_player = SoundPlayer()
# sound_player.play("/path/to/mysound.mp3", volume=75)

# if sound_player.is_playing():
#     print("Sound is currently playing")

# # Later, when you want to stop playback
# sound_player.stop()