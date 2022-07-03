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
    play_sound(40)

