from pygame import mixer
sound = mixer.Sound('./alarm.wav')


def play_sound(duration):
    sound.play()
    time.sleep(duration)

if __name__ == 'main':
    play_sound(2)

