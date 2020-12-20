#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame, pygame.freetype, pygame.mixer, sys
from pygame.locals import *
from konfiguracja import dane, wyswietlacz, odswiez_ekran
from stan import stan

# TODO:
# - mnożnik punktów w rundach
# - runda finałowa
# - muzyka przed początkiem finału
# ? wyświetlać aktualne pytanie i numer rundy (opcjonalnie - opcja w config.yml? wyświetlane na klawisz?)
# ? przenieść do konfiguracji klawisze

KOLOR_CZARNY=(0,0,0)

KLAWISZE_ODPOWIEDZI=[K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9]
KLAWISZ_KONIEC_GRY=K_ESCAPE
KLAWISZ_NASTEPNA_RUNDA=K_RIGHT
KLAWISZ_POPRZEDNIA_RUNDA=K_LEFT
KLAWISZ_DRUZYNA_0=K_COMMA
KLAWISZ_DRUZYNA_1=K_PERIOD
KLAWISZ_BLAD=K_b
KLAWISZ_COFNIJ_CZYNNOSC=K_BACKSPACE

def biezace_odpowiedzi():
  return dane.rundy[stan.ktora_runda].odpowiedzi

def pokaz_tekst(tresc,xy,czcionka=dane.fnt_podstawowa):
  czcionka.render_to(wyswietlacz, xy, tresc.upper())

def pokaz_punkty():
  # suma punktów w bieżącej rundzie
  pokaz_tekst(tresc=dane.txt_suma,xy=dane.crd_punkty_suma_napis)
  pokaz_tekst(tresc=str(stan.punkty_biezace),xy=dane.crd_punkty_suma_punkty)
  # suma punktów przemnożona przez mnożnik
  pokaz_tekst(tresc=str(stan.punkty_przemnozone()), xy=dane.crd_punkty_przemnozone, czcionka=dane.fnt_punkty_druzyn)
  # punkty drużyn
  for ktora_druzyna in [0,1]:
    pokaz_tekst(tresc=str(stan.liczniki_punktow[ktora_druzyna]),xy=dane.crd_punkty_druzyn[ktora_druzyna],czcionka=dane.fnt_punkty_druzyn)

def pokaz_druzyny():
  for ktora_druzyna in [0,1]:
    pokaz_tekst(tresc=dane.nazwy_druzyn[ktora_druzyna],xy=dane.crd_nazwy_druzyn[ktora_druzyna])

  if stan.biezaca_druzyna is not None:
    wyswietlacz.blit(dane.aktywna_druzyna,dane.crd_aktywna_druzyna[stan.biezaca_druzyna])

def pokaz_odpowiedzi():
  odpowiedzi=dane.rundy[stan.ktora_runda].odpowiedzi
  crd_lp=list(dane.crd_odpowiedzi_lp)
  crd_haslo=list(dane.crd_odpowiedzi_haslo)
  crd_punkty=list(dane.crd_odpowiedzi_punkty)
  for indeks,odpowiedz in enumerate(odpowiedzi):
    pokaz_tekst(tresc=str(indeks+1), xy=tuple(crd_lp))
    pokaz_tekst(tresc=odpowiedz.tresc if indeks in stan.widoczne_odpowiedzi else dane.txt_ukryte_punkty, xy=tuple(crd_haslo))
    pokaz_tekst(tresc=str(odpowiedz.punkty) if indeks in stan.widoczne_odpowiedzi else dane.txt_ukryte_haslo, xy=tuple(crd_punkty))
    crd_lp[1]+=dane.crd_odpowiedzi_odstep
    crd_haslo[1]+=dane.crd_odpowiedzi_odstep
    crd_punkty[1]+=dane.crd_odpowiedzi_odstep

def pokaz_bledy():
  for ktora_druzyna in [0,1]:
    czy_duzy_blad = stan.liczniki_bledow[(ktora_druzyna+1) % 2] == 3 # jeśli druga drużyna zrobiła 3 błędy, to nasza drużyna ma albo brak błędów, albo jeden wielki błąd
    polozenie=list(dane.crd_bledy[ktora_druzyna])
    if czy_duzy_blad:
      if stan.liczniki_bledow[ktora_druzyna] > 0:
        wyswietlacz.blit(dane.blad_duzy,tuple(polozenie))
    else:
      for i in range(stan.liczniki_bledow[ktora_druzyna]):
        wyswietlacz.blit(dane.blad_maly,tuple(polozenie))
        polozenie[1]+=dane.crd_bledy_odstep

def zagraj_dzwiek_wydarzenia():
  # traktujemy dźwięki jak muzykę, bo Sound.play() z nieznanej przyczyny wywala program (Segmentation fault)
  if stan.dzwieki_wydarzen:
    for snd in stan.dzwieki_wydarzen:
      pygame.mixer.music.load(getattr(dane, snd))
      pygame.mixer.music.play()
      while pygame.mixer.music.get_busy():
        pygame.time.wait(50)
    stan.dzwieki_wydarzen=[]

def wyswietl_stan():
  wyswietlacz.fill(KOLOR_CZARNY)
  wyswietlacz.blit(dane.img_tlo,(0,0))
  pokaz_odpowiedzi()
  pokaz_punkty()
  pokaz_druzyny()
  pokaz_bledy()
  odswiez_ekran()
  zagraj_dzwiek_wydarzenia()

def ekran_powitalny():
  czy_petla = True
  pygame.mixer.music.load(dane.mus_muzyka_na_start)
  wyswietlacz.blit(dane.img_ekran_powitalny, (0,0) )
  odswiez_ekran()
  pygame.mixer.music.play()
  while czy_petla:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        czy_petla = False
  pygame.mixer.music.stop()

def rundy_zwykle():
  wyswietl_stan()

  czy_petla = True
  while czy_petla:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key ==  KLAWISZ_KONIEC_GRY:
          koniec()
        elif event.key == KLAWISZ_DRUZYNA_0:
          if stan.biezaca_druzyna is None:
            stan.ustaw_biezaca_druzyne(0)
        elif event.key == KLAWISZ_DRUZYNA_1:
          if stan.biezaca_druzyna is None:
            stan.ustaw_biezaca_druzyne(1)
        elif event.key in KLAWISZE_ODPOWIEDZI:
          numer_odpowiedzi = KLAWISZE_ODPOWIEDZI.index(event.key)
          stan.poprawna_odpowiedz(numer_odpowiedzi)
        elif event.key == KLAWISZ_BLAD:
          stan.bledna_odpowiedz()
        elif event.key == KLAWISZ_NASTEPNA_RUNDA:
          if stan.ktora_runda < len(dane.rundy) - 1:
            stan.kolejna_runda()
        elif event.key == KLAWISZ_POPRZEDNIA_RUNDA:
          if stan.ktora_runda > 0:
            stan.poprzednia_runda()
        elif event.key == KLAWISZ_COFNIJ_CZYNNOSC:
          stan.przywroc_poprzedni_stan()
        wyswietl_stan()

def koniec():
  pygame.quit()
  sys.exit()

def main():
  ekran_powitalny()
  rundy_zwykle()
  koniec()

if __name__ == '__main__':
  main()