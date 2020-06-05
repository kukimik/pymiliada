#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame, sys, yaml
from pygame.locals import *
from os.path import normpath

PLIK_KONFIGURACYJNY = "config.yml"

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

    self.rozmiar_ekranu=tuple(dane_z_yaml['rozmiar_ekranu'])

    #obrazy
    sekcja=dane_z_yaml['obrazy']
    (self.img_ekran_powitalny,
     self.img_tlo,
     self.blad_maly,
     self.blad_duzy,
     self.aktywna_druzyna,
    ) = (pygame.image.load(normpath(sekcja['ekran_powitalny'])),
         pygame.image.load(normpath(sekcja['tlo'])),
         pygame.image.load(normpath(sekcja['blad_maly'])),
         pygame.image.load(normpath(sekcja['blad_duzy'])),
         pygame.image.load(normpath(sekcja['aktywna_druzyna'])),
        )

    #dźwięki
    #Traktujemy je jako muzykę, nie dźwięki, gdyż Sound.play() kończy się Segmentation fault. Nie wiem dlaczego.
    sekcja=dane_z_yaml['dzwieki']
    (self.snd_bledna_odpowiedz,
     self.snd_poprawna_odpowiedz,
     self.snd_koniec_rundy,
     self.snd_nowa_runda,
    ) = (normpath(sekcja['bledna_odpowiedz']),#pygame.mixer.Sound(normpath(sekcja['bledna_odpowiedz'])),
         normpath(sekcja['poprawna_odpowiedz']),#pygame.mixer.Sound(normpath(sekcja['poprawna_odpowiedz'])),
         normpath(sekcja['koniec_rundy']),
         normpath(sekcja['nowa_runda']),
        )

    #muzyka
    sekcja=dane_z_yaml['muzyka']
    self.mus_muzyka_na_start=normpath(sekcja['muzyka_na_start'])

    #czcionki
    sekcja=dane_z_yaml['czcionki']
    (self.fnt_podstawowa,
     self.fnt_punkty_druzyn,
    ) = (pygame.freetype.Font(normpath(sekcja['podstawowa']['plik']),sekcja['podstawowa']['rozmiar']),
         pygame.freetype.Font(normpath(sekcja['punkty_druzyn']['plik']),sekcja['punkty_druzyn']['rozmiar']),
        )

    (self.fnt_podstawowa.fgcolor,
     self.fnt_punkty_druzyn.fgcolor,
    ) = (tuple(sekcja['podstawowa']['kolor']),
         tuple(sekcja['punkty_druzyn']['kolor']),
        )

    #współrzędne
    sekcja=dane_z_yaml['wspolrzedne']
    self.crd_bledy,self.crd_punkty_druzyn,self.crd_nazwy_druzyn,self.crd_aktywna_druzyna=[None,None],[None,None],[None,None],[None,None]

    (self.crd_odpowiedzi_lp,
     self.crd_odpowiedzi_haslo,
     self.crd_odpowiedzi_punkty,
     self.crd_odpowiedzi_odstep,
     self.crd_bledy[0],
     self.crd_bledy[1],
     self.crd_bledy_odstep,
     self.crd_punkty_druzyn[0],
     self.crd_punkty_druzyn[1],
     self.crd_punkty_suma_napis,
     self.crd_punkty_suma_punkty,
     self.crd_nazwy_druzyn[0],
     self.crd_nazwy_druzyn[1],
     self.crd_aktywna_druzyna[0],
     self.crd_aktywna_druzyna[1],
    ) = (tuple(sekcja['odpowiedzi']['lp']),
         tuple(sekcja['odpowiedzi']['haslo']),
         tuple(sekcja['odpowiedzi']['punkty']),
               sekcja['odpowiedzi']['odstep'],
         tuple(sekcja['bledy']['druzyna_0']),
         tuple(sekcja['bledy']['druzyna_1']),
               sekcja['bledy']['odstep'],
         tuple(sekcja['punkty']['druzyna_0']),
         tuple(sekcja['punkty']['druzyna_1']),
         tuple(sekcja['punkty']['suma_napis']),
         tuple(sekcja['punkty']['suma_punkty']),
         tuple(sekcja['nazwy_druzyn']['druzyna_0']),
         tuple(sekcja['nazwy_druzyn']['druzyna_1']),
         tuple(sekcja['aktywna_druzyna']['druzyna_0']),
         tuple(sekcja['aktywna_druzyna']['druzyna_1']),
        )

    #teksty
    sekcja=dane_z_yaml['teksty']
    (self.txt_suma,
     self.txt_ukryte_haslo,
     self.txt_ukryte_punkty,
    ) = (sekcja['suma'],
         sekcja['ukryte_punkty'],
         sekcja['ukryte_haslo'],
        )

    #rundy, nazwy drużyn i finał
    rundy_dane_z_yaml=czytaj_plik_yaml(sciezka=dane_z_yaml['pytania'])
    self.nazwy_druzyn=(rundy_dane_z_yaml['nazwy_druzyn']['druzyna_0'],
                       rundy_dane_z_yaml['nazwy_druzyn']['druzyna_1'])
    self.rundy=[ Runda(pytanie=runda['pytanie'], \
                       odpowiedzi=[ Odpowiedz(tresc=odpowiedz['odp'], punkty=odpowiedz['pkt']) \
                                    for odpowiedz in runda['odpowiedzi'] ] ) \
                 for runda in rundy_dane_z_yaml['rundy'] ]

def liczba_odpowiedzi(numer_rundy):
  return len(dane.rundy[numer_rundy].odpowiedzi)

def liczba_punktow(numer_rundy,numer_odpowiedzi):
  return dane.rundy[numer_rundy].odpowiedzi[numer_odpowiedzi].punkty

def stworz_ekran(rozmiar=None):
  if rozmiar is None:
    info = pygame.display.Info()
    return pygame.display.set_mode((info.current_w, info.current_h), FULLSCREEN)
  else:
    return pygame.display.set_mode(rozmiar)

def odswiez_ekran():
  ekran.blit(pygame.transform.smoothscale(wyswietlacz,pygame.display.get_surface().get_size()),(0,0))
  pygame.display.update()

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
dane = Dane(PLIK_KONFIGURACYJNY)
ekran = stworz_ekran(dane.rozmiar_ekranu)
wyswietlacz = pygame.Surface(dane.img_tlo.get_size())