#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame, pygame.freetype, sys
from pygame.locals import *
from konfiguracja import dane, wyswietlacz, odswiez_ekran
from stan import stan

# TODO:
# - dodać dźwięki
# - dodać X-y za błędy w formie obrazków
# - ładne tło i ustawienie współrzędnych obiektów
# - dodać oznaczenie, która drużyna jest aktywna (nazwy rodzin)
# - dodać aktualne pytanie i numer rundy (opcjonalnie - opcja w config.yml)
# - przenieść do konfiguracji kolory, położenia, klawisze
# - rozmiar ekranu w config.yml
# - runda finałowa


KOLOR_CZARNY=(0,0,0)
KOLOR_TEKSTU=(70,230,100)

KLAWISZE_ODPOWIEDZI=[K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9]
KLAWISZ_KONIEC_GRY=K_ESCAPE
KLAWISZ_NASTEPNA_RUNDA=K_RIGHT
KLAWISZ_POPRZEDNIA_RUNDA=K_LEFT
KLAWISZ_DRUZYNA_0=K_a
KLAWISZ_DRUZYNA_1=K_s
KLAWISZ_BLAD=K_b
KLAWISZ_COFNIJ_CZYNNOSC=K_z

POLOZENIE_Y0=100
ODSTEP_Y=70
POLOZENIE_LP_X=120
POLOZENIE_HASLO_X=160
POLOZENIE_PUNKTY_X=950

POLOZENIE_SUMA_X=800
POLOZENIE_SUMA_Y=900

POLOZENIE_PUNKTY_DRUZYNA_0=(50,700)
POLOZENIE_PUNKTY_DRUZYNA_1=(1050,700)
POLOZENIE_BLEDY_X_DRUZYNA_0=40
POLOZENIE_BLEDY_X_DRUZYNA_1=1070
POLOZENIE_BLEDY_Y=100
ODSTEP_BLEDY_Y=150

def biezace_odpowiedzi():
  return dane.rundy[stan.ktora_runda].odpowiedzi

def pokaz_tekst(tresc,xy,czcionka=dane.fnt_podstawowa,kolor=KOLOR_TEKSTU):
  czcionka.render_to(wyswietlacz, xy, tresc.upper(), kolor)

def pokaz_bledy(ktora_druzyna):
  czy_duzy_blad = stan.liczniki_bledow[(ktora_druzyna+1) % 2] == 3
  x={0:POLOZENIE_BLEDY_X_DRUZYNA_0,1:POLOZENIE_BLEDY_X_DRUZYNA_1}[ktora_druzyna]
  if czy_duzy_blad:
    if stan.liczniki_bledow[ktora_druzyna] > 0:
      pokaz_tekst('||',(x,POLOZENIE_BLEDY_Y+50),dane.fnt_blad)
      pokaz_tekst('X',(x+10,POLOZENIE_BLEDY_Y+50+70),dane.fnt_blad)
      pokaz_tekst('||',(x,POLOZENIE_BLEDY_Y+50+140),dane.fnt_blad)
  else:
    for i in range(stan.liczniki_bledow[ktora_druzyna]):
      pokaz_tekst('X',(x,POLOZENIE_BLEDY_Y+i*ODSTEP_BLEDY_Y),dane.fnt_blad)

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

def wyswietl_stan():
  wyswietlacz.fill(KOLOR_CZARNY)
  wyswietlacz.blit(dane.img_tlo,(0,0))
  odpowiedzi=dane.rundy[stan.ktora_runda].odpowiedzi
  # odpowiedzi
  for indeks,odpowiedz in enumerate(odpowiedzi):
    y=POLOZENIE_Y0+indeks*ODSTEP_Y
    pokaz_tekst(tresc=str(indeks+1), xy=(POLOZENIE_LP_X,y))
    pokaz_tekst(tresc=odpowiedz.tresc if indeks in stan.widoczne_odpowiedzi else '.................................', xy=(POLOZENIE_HASLO_X,y))
    pokaz_tekst(tresc=str(odpowiedz.punkty) if indeks in stan.widoczne_odpowiedzi else '--', xy=(POLOZENIE_PUNKTY_X,y))
  # suma punktów w bieżącej rundzie
  pokaz_tekst(tresc='SUMA',xy=(POLOZENIE_SUMA_X,POLOZENIE_SUMA_Y))
  pokaz_tekst(tresc=str(stan.punkty_biezace),xy=(POLOZENIE_PUNKTY_X,POLOZENIE_SUMA_Y))
  # punkty drużyn
  pokaz_tekst(tresc=str(stan.liczniki_punktow[0]),xy=POLOZENIE_PUNKTY_DRUZYNA_0,czcionka=dane.fnt_punkty_druzyn)
  pokaz_tekst(tresc=str(stan.liczniki_punktow[1]),xy=POLOZENIE_PUNKTY_DRUZYNA_1,czcionka=dane.fnt_punkty_druzyn)
  # błędy
  pokaz_bledy(ktora_druzyna=0)
  pokaz_bledy(ktora_druzyna=1)
  odswiez_ekran()

def rundy_zwykle():
  wyswietl_stan()

  czy_petla = True
  while czy_petla:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key ==  KLAWISZ_KONIEC_GRY:
          koniec()
        elif event.key == KLAWISZ_DRUZYNA_0:
          stan.ustaw_biezaca_druzyne(0)
        elif event.key == KLAWISZ_DRUZYNA_1:
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