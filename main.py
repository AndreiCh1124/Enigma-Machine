import pygame

from keyboard import Keyboard
from plugboard import Plugboard
from rotor import Rotor
from reflector import Reflector
from enigma import Enigma
from draw import draw

# setup pygame
pygame.init()
pygame.font.init()
pygame.display.set_caption("Enigma machine")

# init fonts
MONO = pygame.font.SysFont("FreeMono", 25)
BOLD = pygame.font.SysFont("FreeMono", 25, bold=True)

# global vars
WIDTH = 1600
HEIGHT = 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
MARGINS = {"top":200, "bottom":200, "left":100, "right":100}
GAP = 75
INPUT = ""
OUTPUT = ""
PATH = []

# historical configuration of the rotors and reflectors if the M3 Enigma
I = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
II = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
III = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V")
IV = Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J")
V = Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", "Z")
A = Reflector("EJMZALYXVBWFCRQUONTSPIKHGD")
B = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
C = Reflector("FVPJIAOYEDRZXWGCTKUQSBNMHL")

# keyboard and plugboard configuration
KB = Keyboard()
PB = Plugboard(["AB", "CD", "EF"])

# initialize enigma machine
eng = Enigma(B, I, II, III, PB, KB)

# set the rings
eng.set_rings((1, 1, 1))

# set the key
eng.set_key("CAT")


animating = True
while animating:
    # background
    SCREEN.fill('#333333')

    # render input
    text = BOLD.render(INPUT, True, "white")
    textbox = text.get_rect(center = (WIDTH/2, MARGINS["top"]/3))
    SCREEN.blit(text, textbox)


    # render input
    text = MONO.render(OUTPUT, True, "white")
    textbox = text.get_rect(center = (WIDTH/2, MARGINS["top"]/3+30))
    SCREEN.blit(text, textbox)

    # draw Enigma machine
    draw(eng, PATH, SCREEN, WIDTH, HEIGHT, MARGINS, GAP, BOLD)    

    pygame.display.flip()

    # track user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            animating = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                eng.r1.rotate()
            elif event.key == pygame.K_SPACE:
                INPUT += " "
                OUTPUT += " "
            else:
                key = event.unicode
                if key in "abcdefghijklmnopqrstuvwxyz":
                    letter = key.upper()
                    INPUT += letter
                    PATH, cipher = eng.encrypt(letter) 
                    OUTPUT += cipher