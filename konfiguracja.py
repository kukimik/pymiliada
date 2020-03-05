#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame, sys, yaml
from pygame.locals import *
from os.path import normpath


PLIK_KONFIGURACYJNY = "config.yml"

IMG_SEKCJA='grafika'
IMG_EKRAN_POWITALNY='ekran_powitalny'
IMG_TLO='tlo'

SND_SEKCJA='dzwieki'
SND_BLEDNA_ODPOWIEDZ='bledna_odpowiedz'
SND_DOBRA_ODPOWIEDZ='dobra_odpowiedz'

MUS_SEKCJA='muzyka'
MUS_MUZYKA_NA_START='muzyka_na_start'

FNT_SEKCJA='czcionki'
FNT_OPT_PLIK='plik'
FNT_OPT_ROZMIAR='rozmiar'
FNT_PODSTAWOWA='podstawowa'
FNT_PUNKTY_DRUZYN='punkty_druzyn'
FNT_BLAD='blad'


PYTANIA_SEKCJA='pytania'

P_RUNDY='rundy'
P_FINAL='final'
P_PYTANIE='pytanie'
P_ODPOWIEDZI='odpowiedzi'
P_ODP='odp'
P_PKT='pkt'

def czytaj_plik_yaml(sciezka):
  plik = open(normpath(sciezka), 'r')
  zawartosc_pliku = plik.read()
  plik.close()
  return yaml.safe_load(zawartosc_pliku)

class Odpowiedz:
  def __init__(self,tresc,punkty):
    self.tresc=tresc
    self.punkty=punkty

class Runda:
  def __init__(self,pytanie,odpowiedzi):
    self.pytanie=pytanie
    self.odpowiedzi=odpowiedzi

class Dane:
  def __init__(self, plik_konfiguracyjny):

    dane_z_yaml = czytaj_plik_yaml(sciezka=plik_konfiguracyjny)

    img_sekcja=dane_z_yaml[IMG_SEKCJA]
    snd_sekcja=dane_z_yaml[SND_SEKCJA]
    mus_sekcja=dane_z_yaml[MUS_SEKCJA]
    fnt_sekcja=dane_z_yaml[FNT_SEKCJA]

    #obrazy
    self.img_ekran_powitalny=pygame.image.load(normpath(img_sekcja[IMG_EKRAN_POWITALNY]))
    self.img_tlo=pygame.image.load(normpath(img_sekcja[IMG_TLO]))

    #dźwięki
    self.snd_bledna_odpowiedz=pygame.mixer.Sound(normpath(snd_sekcja[SND_BLEDNA_ODPOWIEDZ]))
    self.snd_dobra_odpowiedz=pygame.mixer.Sound(normpath(snd_sekcja[SND_DOBRA_ODPOWIEDZ]))

    #muzyka
    self.mus_muzyka_na_start=normpath(mus_sekcja[MUS_MUZYKA_NA_START])

    #czcionki
    self.fnt_podstawowa=pygame.font.Font(normpath(fnt_sekcja[FNT_PODSTAWOWA][FNT_OPT_PLIK]),fnt_sekcja[FNT_PODSTAWOWA][FNT_OPT_ROZMIAR])
    self.fnt_punkty_druzyn=pygame.font.Font(normpath(fnt_sekcja[FNT_PUNKTY_DRUZYN][FNT_OPT_PLIK]),fnt_sekcja[FNT_PUNKTY_DRUZYN][FNT_OPT_ROZMIAR])
    self.fnt_blad=pygame.font.Font(normpath(fnt_sekcja[FNT_BLAD][FNT_OPT_PLIK]),fnt_sekcja[FNT_BLAD][FNT_OPT_ROZMIAR])

    #rundy i finał
    rundy_dane_z_yaml=czytaj_plik_yaml(sciezka=dane_z_yaml[PYTANIA_SEKCJA])
    self.rundy=[ Runda(pytanie=runda[P_PYTANIE],odpowiedzi=[ Odpowiedz(tresc=odpowiedz[P_ODP],punkty=odpowiedz[P_PKT]) for odpowiedz in runda[P_ODPOWIEDZI] ]) for runda in rundy_dane_z_yaml[P_RUNDY] ]

def liczba_odpowiedzi(numer_rundy):
  return len(dane.rundy[numer_rundy].odpowiedzi)

def liczba_punktow(numer_rundy,numer_odpowiedzi):
  return dane.rundy[numer_rundy].odpowiedzi[numer_odpowiedzi].punkty

def stworz_wyswietlacz():
  info = pygame.display.Info()
  #return pygame.display.set_mode((1024, 768), FULLSCREEN)
  return pygame.display.set_mode((info.current_w, info.current_h), FULLSCREEN)

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
dane = Dane(PLIK_KONFIGURACYJNY)
wyswietlacz = stworz_wyswietlacz()
