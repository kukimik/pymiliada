#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame, sys
from pygame.locals import *
from konfiguracja import dane, wyswietlacz
from stan import *

# TODO: przenieść do konfiguracji kolory, położenia, klawisze
BLACK=(0,0,0)
ORANGE=(255,200,0)

KLAWISZE_ODPOWIEDZI=[K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8]
KLAWISZ_KONIEC_GRY=K_q
#KLAWISZ_FINAL=K_0
#KLAWISZ_RUNDY=K_9
KLAWISZ_NASTEPNA_RUNDA=K_RIGHT
KLAWISZ_POPRZEDNIA_RUNDA=K_LEFT
KLAWISZ_BLAD_0=K_z
KLAWISZ_BLAD_0_COFNIJ=K_x
KLAWISZ_BLAD_1=K_n
KLAWISZ_BLAD_1_COFNIJ=K_m
KLAWISZ_PUNKTY_NALICZ_0=K_o
KLAWISZ_PUNKTY_ZABIERZ_0=K_k
KLAWISZ_PUNKTY_NALICZ_1=K_p
KLAWISZ_PUNKTY_ZABIERZ_1=K_l

#z/x  - dodanie/odjêcie b³êdu dru¿ynie po lewej
#n/m - dodanie/dojêcie b³êdu dru¿ynie po prawej
#o/k - dodanie sumy punktow do druzyny po lewej/ odjêcie
#p/l - dodanie sumy punktow do druzyny po prawej/ dojêcie
#9 i 0 - prze³¹czanie pomiêdzy etapami gry ( 9-powrot , 0 - nastêpny etap)

POLOZENIE_Y0=100
ODSTEP_Y=40
POLOZENIE_LP_X=100
POLOZENIE_HASLO_X=120
POLOZENIE_PUNKTY_X=900
POLOZENIE_SUMA_X=800
POLOZENIE_SUMA_Y=800
POLOZENIE_PUNKTY_DRUZYNA_0=(50,350)
POLOZENIE_PUNKTY_DRUZYNA_1=(1050,350)

def biezace_odpowiedzi():
  return dane.rundy[stan.ktora_runda].odpowiedzi

def pokaz_tekst(tresc,xy,czcionka=dane.fnt_podstawowa,kolor=ORANGE):
  text = czcionka.render(tresc.upper(),True,kolor)
  wyswietlacz.blit(text, xy)

def ekran_powitalny():
  czy_petla = True
  pygame.mixer.music.load(dane.mus_muzyka_na_start)
  wyswietlacz.blit(dane.img_ekran_powitalny, (0,0) )
  pygame.display.update()
  pygame.mixer.music.play()
  while czy_petla:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        czy_petla = False
  pygame.mixer.music.stop()

def wyswietl_stan():
  wyswietlacz.fill(BLACK)
  wyswietlacz.blit(dane.img_tlo,(0,0))
  odpowiedzi=dane.rundy[stan.ktora_runda].odpowiedzi
  # odpowiedzi
  for indeks,odpowiedz in enumerate(odpowiedzi):
    y=POLOZENIE_Y0+indeks*ODSTEP_Y
    pokaz_tekst(tresc=str(indeks+1), xy=(POLOZENIE_LP_X,y))
    pokaz_tekst(tresc=odpowiedz.tresc if indeks in stan.widoczne_odpowiedzi else '............................................', xy=(POLOZENIE_HASLO_X,y))
    pokaz_tekst(tresc=str(odpowiedz.punkty) if indeks in stan.widoczne_odpowiedzi else '--', xy=(POLOZENIE_PUNKTY_X,y))
  # suma punktów w bieżącej rundzie
  pokaz_tekst(tresc='SUMA',xy=(POLOZENIE_SUMA_X,POLOZENIE_SUMA_Y))
  pokaz_tekst(tresc=str(stan.punkty_biezace),xy=(POLOZENIE_PUNKTY_X,POLOZENIE_SUMA_Y))
  # punkty drużyn
  pokaz_tekst(tresc=str(stan.liczniki_punktow[0]),xy=POLOZENIE_PUNKTY_DRUZYNA_0,czcionka=dane.fnt_punkty_druzyn)
  pokaz_tekst(tresc=str(stan.liczniki_punktow[1]),xy=POLOZENIE_PUNKTY_DRUZYNA_1,czcionka=dane.fnt_punkty_druzyn)
  # błędy
  # TODO

  pygame.display.update()

def rundy_zwykle():
  wyswietl_stan()

  czy_petla = True
  while czy_petla:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key ==  KLAWISZ_KONIEC_GRY:
          koniec()
        elif event.key in KLAWISZE_ODPOWIEDZI:
          numer_odpowiedzi = KLAWISZE_ODPOWIEDZI.index(event.key)
          if numer_odpowiedzi < len(biezace_odpowiedzi()):
            stan.poprawna_odpowiedz(numer_odpowiedzi, biezace_odpowiedzi()[numer_odpowiedzi].punkty)
        elif event.key == KLAWISZ_NASTEPNA_RUNDA:
          if stan.ktora_runda < len(dane.rundy) - 1:
            stan.kolejna_runda()
        elif event.key == KLAWISZ_POPRZEDNIA_RUNDA:
          if stan.ktora_runda > 0:
            stan.poprzednia_runda()
        elif event.key == KLAWISZ_PUNKTY_NALICZ_0:
          stan.dodaj_punkty(0)
        elif event.key == KLAWISZ_PUNKTY_NALICZ_1:
          stan.dodaj_punkty(1)
        elif event.key == KLAWISZ_PUNKTY_ZABIERZ_0:
          stan.zabierz_punkty(0)
        elif event.key == KLAWISZ_PUNKTY_ZABIERZ_1:
          stan.zabierz_punkty(1)
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