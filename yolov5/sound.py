import os
#os.environ["XDG_RUNTIME_DIR"]="/run/pi/1000"
#os.environ["PULSE_RUNTIME_PATH"]="/run/pi/1000/pulse/"
import pygame
import time
pygame.mixer.init()
speaker_volume  = 1
pygame.mixer.music.set_volume(speaker_volume)
pygame.mixer.music.load('/home/pi/Person-Detection/yolov5/siren.wav')


def play_sound(duration):
    pygame.mixer.music.play()
    time.sleep(duration)

if __name__ == "__main__":
    while(True):
        play_sound(40)

