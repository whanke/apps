"""Vokabeltrainer von Wilm Hanke (2130964)
Stand: 13.07.2015"""

from collections import *
from random import *
from math import *
import os
import codecs
import sys
import datetime

def spielmodus():
    print('Spielmodus?\n1 = Zielworte lernen/eingeben, Fremdworte werden abgefragt')
    print('2 = Fremdworte lernen/eingeben, Zielworte erden abgefragt\n3 = Vokabelkarte hinzufügen')
    u_wahl = input('Eingabe: ')

    if u_wahl == str(1):
        return ext_dict() 
    elif u_wahl == str(2):
        return invert_dict()
    elif u_wahl == str(3):
        hinzu()
        return spielmodus()         
    else:
        print('Bitte eine gültige Wahl')
        return spielmodus()

def karte(wort,dic): # übertragung von key und value
    for k,v in dic.items():
        if k == wort:
            return k,v
    
def zufall_v(dic): 
    fworte=list(dic.keys())
    zufall_index = randint(0,len(fworte)-1)
    wort = fworte[zufall_index]
    return wort

def invert_dict():
    invert_d = {v: k for k, v in ext_dict().items()}
    return invert_d

def fremdwort(dic):
    fworte=list(dic.keys())
    zufall_index = randint(0,len(fworte)-1)
    wort = fworte[zufall_index]
    return wort

"""def, die eine externe datei als dict einliest
und die Datei nach bestimmten Kriterien einliest und
als externes dict zurückgibt"""
def ext_dict(): 
    datei = pfad()
    datei.seek(0)
    ext_dict = {}
    for line in datei.readlines():
        key=''
        value=''
        for c in line:
            key += c
            if c == "=":
                break
        if key.startswith("\ufeff"): # Korrektur, wenn BOM vorhanden
            key = key.replace('\ufeff', '')
        for c in line[line.find("=")+1:]:
            value += c
        value = value.replace('\n','') # Korrektur, da jede Zeile/value mit \n endet -> es wäre immer: eingabe != value
        ext_dict[key[0:-2]] = value[1:]
    return ext_dict

def pfad():
    while True:
        try:
            pfad = input('Pfad der externen Datei: ')
            datei = open(pfad,'r+',encoding="utf-8") 
            return datei
        except IOError:
            print('Datei existiert nicht.')


def hinzu(): #neue vokabelkarten in dict einpflegen
    print('Fügen Sie eine Vokabelkarte hinzu:\n')
    u_fremdwort = input('Fremdwort: ')
    u_zielwort = input('Zielwort: ')
    pfad = input('Pfad der externen Datei: ')
    p = pfad
    if os.path.isfile("./{0}.txt" .format(p)):
        with open(p,'a+') as f: f.write('\n')
        with open(p,'a+',encoding="utf-8") as f: f.write(u_fremdwort)
        with open(p,'a+') as f: f.write(" = ")
        with open(p,'a+',encoding="utf-8") as f: f.write(u_zielwort)
        print('Vokabelkarte hinzugefügt: ',u_fremdwort,' = ',u_zielwort)
        return True
    else:
        with open(p,'w+') as f: f.write('\n')
        with open(p,'a+',encoding="utf-8") as f: f.write(u_fremdwort)
        with open(p,'a+') as f: f.write(" = ")
        with open(p,'a+',encoding="utf-8") as f: f.write(u_zielwort)
        print('Vokabelkarte hinzugefügt: ',u_fremdwort,' = ',u_zielwort)

def user(username): # prüft/erstellt user (inklusive dict-box 1-3)
    fmt = '%d.%m.%Y um %H:%M:%S'
    if os.path.isfile("./{0}.txt" .format(username)):
        print('User erkannt.')
        DateiDatum = ''
        old_points=''
        level=''
        with open("./{0}.txt" .format(username),'r+',encoding="utf-8") as datei:
            for line in datei.readlines():
                if line.startswith('level'):
                    for c in line[line.find('=')+1:]:
                        level += c 
                if line.startswith('punkte'):
                    for c in line[line.find('=')+1:]:
                        old_points += c 
                if line.startswith('letzter_login'):
                    for c in line[line.find('=')+1:]:
                        DateiDatum += c
                        if c == '.':
                            break
                pass
        Alt_DateiDatum = datetime.datetime.strptime(DateiDatum[:-1], '%Y-%m-%d %H:%M:%S')
        Neu_DateiDatum = datetime.datetime.now()
        print('Letzter Login: {0}\n' .format(Alt_DateiDatum.strftime(fmt)))    
        datei.close()
        if Neu_DateiDatum - Alt_DateiDatum > datetime.timedelta(1):
            print('+3 Punkte für Besuch innerhalb eines Tages!'), calc_pts(3,username)
        elif Neu_DateiDatum - Alt_DateiDatum > datetime.timedelta(2):
            print('+2 Punkte für Besuch innerhalb zwei Tage!'), calc_pts(2,username)
        else:
            print('+1 Punkt für "Nichtaufgegeben und Wiedergekommen"!'), calc_pts(1,username)
        #### datei "./{0}.txt" .format(username) update: ####
        with open("./{0}.txt" .format(username),'w',encoding="utf-8") as datei: 
            datei.write('level={0}' .format(level)) 
            datei.write('punkte={0}' .format(old_points))
            datei.write('letzter_login={0}' .format(Neu_DateiDatum))
            datei.close()
        return True
    else:
        zeit = datetime.datetime.now()
        with open("./{0}.txt" .format(username),'w+',encoding="utf-8") as datei:
            datei.write('level=0\n')
            datei.write('punkte=0\n')
            datei.write('letzter_login={0}' .format(zeit))
        open("./{0}-dic-1.txt" .format(username),'w+').close()
        open("./{0}-dic-2.txt" .format(username),'w+').close()
        open("./{0}-dic-3.txt" .format(username),'w+').close()
        print('User erstellt.')
        return False

def calc_pts(punkte,username):
    old_points=''
    neue_punkte = int(0)
    DateiDatum = ''
    with open("./{0}.txt" .format(username),'r+',encoding="utf-8") as datei:
        for line in datei.readlines():
            if line.startswith('punkte'):
                for c in line[line.find('=')+1:]:
                    old_points += c          
                if old_points == '':
                    old_points = '0'
                    pass
                neue_punkte = int(old_points) + int(punkte)
            if line.startswith('letzter_login'):
                    for c in line[line.find('=')+1:]:
                        DateiDatum += c
                        if c == '.':
                            break
            pass            
        datei.close()
    if neue_punkte <= int(0):
        neue_punkte = int(1)
    level = int(sqrt(int(neue_punkte))) # Levelranking
    with open("./{0}.txt" .format(username),'w',encoding="utf-8") as datei: 
        datei.write('level={0}\n' .format(level)) 
        datei.write('punkte={0}\n' .format(neue_punkte))
        datei.write('letzter_login={0}' .format(DateiDatum))
        if punkte == 1:
            print('Es wurde {0} Punkt berechnet!' .format(punkte))
        else:
            print('Es wurden {0} Punkte berechnet!' .format(punkte))
            print('Status: Level {0} mit {1} Punkten.' .format(level,neue_punkte))
    datei.close()
    return True

def vokabel_in_box_check(username,boxstage,key,value):
    open("./{0}-dic-{1}.txt" .format(username, boxstage),'r+', encoding='utf-8').seek(0)
    for line in open("./{0}-dic-{1}.txt" .format(username, boxstage),'r+', encoding='utf-8').readlines():
        if line.rstrip() == key + " = " + value: 
            print('Vokabelkarte bereits in Box {0}' .format(boxstage))
            return True
        else:
            return False
        
def schreibe_vokabel_in_box(username,boxstage,key,value):
    with open("./{0}-dic-{1}.txt" .format(username,boxstage),'a+', encoding='utf8') as f:
        f.write(key)
        f.write(" = ")
        f.write(value)
        f.write('\n')
    print("Vokabelkarte in Box {0} eingetragen." .format(boxstage))
    return True

def check_beschriebene_karte(key,value): # prüfen, ob key und value keine leeren strings als wert haben    
    if key != '' and value != '':
        return True
    else:
        return False

def del_vokabelkarte(username,boxstage,key,value):
    datei = open("./{0}-dic-{1}.txt" .format(username, boxstage),"r+", encoding="utf-8")
    d = datei.readlines()
    datei.seek(0)
    for i in d:
        if i != key + " = " + value+ "\n":
            datei.write(i)
    datei.truncate()
    datei.close()
    return True

def level_check(username):
    level=''
    with open("./{0}.txt" .format(username),'r+',encoding="utf-8") as datei:
        for line in datei.readlines():
            if line.startswith('level'):
                for c in line[line.find('=')+1:]:
                    level += c
    return level

def aufdecken(username):
    s= int(level_check(username))/7
    if str(s).endswith('.0'):
        return True
    else:
        return False

#############################    
"""Programmausführung"""
#############################

username = input('Wie lautet Ihr Name? ')
user(username)
d = spielmodus()
choice = True
while choice:
    print("\n\nWas bedeutet:")
    zufall_vokabel=zufall_v(d)
    print('\n',zufall_vokabel,'\n')
    #print(d[zufall_vokabel]) ##### CHEAT!
    if aufdecken(username) == True:
        if input('Belohnung erhalten! "ja" für Annehmen: ') == 'ja':
            print(zufall_vokabel,' bedeutet: ',d[zufall_vokabel]),calc_pts(-1,username)
        pass
    pass
    eingabe=input('Ihr Tipp: ') 
    key = karte(zufall_vokabel,d)[0]
    value = karte(zufall_vokabel,d)[1]
    if check_beschriebene_karte(key,value):
        if eingabe == value:
            print('\nRichtig!\n')
            print(key,"=",value)
            """Prüfung, ob Vokabel in Box n, wenn ja, dann Vokabel in Box n+1"""
            if vokabel_in_box_check(username,1,key,value):
                del_vokabelkarte(username,1,key,value), schreibe_vokabel_in_box(username,2,key,value), calc_pts(7,username)
            elif vokabel_in_box_check(username,2,key,value):
                del_vokabelkarte(username,2,key,value), schreibe_vokabel_in_box(username,3,key,value), calc_pts(10,username)
            elif vokabel_in_box_check(username,3,key,value):
                print('\nVokabel in Box 3!\nVokabel in Endkarte! :)'), calc_pts(10,username)
            else:
                schreibe_vokabel_in_box(username,1,key,value), calc_pts(5,username)  
        else:
            print('\nLeider falsch!\nRichtig ist:\n',value,'\nVokabelkarte:\n',key,"=",value), calc_pts(-5,username)
    else:
        print('Leere Vokabelkarte gefunden')
    if input('\nFür Beenden = "ende" eingeben: ') == 'ende':
        choice = False
sys.exit("Vokabeltrainer beendet.")
