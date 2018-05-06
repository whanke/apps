""" NATO alphabet learning app
Author: Wilm Hanke
Date: Mai 2018
"""

# NATO alphabet


# source: http://www.die-marine.de/_deutsch/sonstiges/alpha_e.html

import random

nato = dict()
nato['A'] = 'ALFA'
nato['B'] = 'BRAVO'
nato['C'] = 'CHARLIE'
nato['D'] = 'DELTA'
nato['E'] = 'ECHO'
nato['F'] = 'FOXTROT'
nato['G'] = 'GOLF'
nato['H'] = 'HOTEL'
nato['I'] = 'INDIA'
nato['J'] = 'JULIETT'
nato['K'] = 'KILO'
nato['L'] = 'LIMA'
nato['M'] = 'MIKE'
nato['N'] = 'NOVEMBER'
nato['O'] = 'OSCAR'
nato['P'] = 'PAPA'
nato['Q'] = 'QUEBEC'
nato['R'] = 'ROMEO'
nato['S'] = 'SIERRA'
nato['T'] = 'TANGO'
nato['U'] = 'UNIFORM'
nato['V'] = 'VICTOR'
nato['W'] = 'WHISKEY'
nato['X'] = 'XRAY'
nato['Y'] = 'YANKEE'
nato['Z'] = 'ZULU'
# nato[''] = ''


def game_guess_word():
    first_input = input('Deine Eingabe: ')
    while user_input != 'exit':
        suggestion = random.choice(list(nato.keys()))
        print('Welcher Name gehört zu: ', suggestion)
        user_input = input('Deine Eingabe: ')
        # user_input
        if user_input == nato[suggestion]:
            print('Richtig! :)\n')
        else:
            print('### Falsch! :( ###')
            print('Korrekt wäre: {}\n'.format(nato[suggestion]))
        print("Zum Beenden 'exit' eintippen.\n")


game_guess_word()
