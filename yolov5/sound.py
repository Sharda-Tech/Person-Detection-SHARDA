import pygame
import time
pygame.mixer.init()
speaker_volume  = 1
pygame.mixer.music.set_volume(speaker_volume)
sound = pygame.mixer.music.load('./alarm.wav')


def play_sound(duration):
    mixer.music.play()
    time.sleep(duration)

if __name__ == 'main':
    play_sound(2)

