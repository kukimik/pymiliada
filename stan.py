#!/usr/bin/python
# -*- coding: utf-8 -*-

from konfiguracja import liczba_odpowiedzi, liczba_punktow
import copy

MAX_POZIOMY_UNDO=8000

BLEDNA_ODPOWIEDZ='bledna_odpowiedz'
POPRAWNA_ODPOWIEDZ='poprawna_odpowiedz'
NOWA_RUNDA='nowa_runda'

MAX_LICZBA_BLEDOW=3

class Stan:
  def __init__(self):
    self.ktora_runda=0
    self.punkty_biezace=0
    self.liczniki_bledow=[0,0]
    self.liczniki_punktow=[0,0]
    self.widoczne_odpowiedzi=[]
    self.biezaca_druzyna=None
    self.wydarzenie=None
    self.koniec_rundy=False

  def poprawna_odpowiedz(self,numer_odpowiedzi):
    if not (len(self.widoczne_odpowiedzi) > 0 and self.biezaca_druzyna is None):
      if numer_odpowiedzi < liczba_odpowiedzi(self.ktora_runda) and numer_odpowiedzi not in self.widoczne_odpowiedzi:
        self.zapisz_stan()
        self.widoczne_odpowiedzi.append(numer_odpowiedzi)
        self.wydarzenie=POPRAWNA_ODPOWIEDZ
        if not self.koniec_rundy:
          self.punkty_biezace+=liczba_punktow(self.ktora_runda,numer_odpowiedzi)
          if self.biezaca_druzyna is not None and len(self.widoczne_odpowiedzi) == liczba_odpowiedzi(self.ktora_runda):
            print('koniec rundy!')
            self.zakoncz_runde(self.biezaca_druzyna)

  def bledna_odpowiedz(self):
    if not self.koniec_rundy:
      if self.biezaca_druzyna is not None:
        przeciwna_druzyna={0:1,1:0,None:None}[self.biezaca_druzyna]
        self.zapisz_stan()
        if self.liczniki_bledow[przeciwna_druzyna] == MAX_LICZBA_BLEDOW:
          self.liczniki_bledow[self.biezaca_druzyna]=1
          self.zakoncz_runde(przeciwna_druzyna)
        elif self.liczniki_bledow[self.biezaca_druzyna] < MAX_LICZBA_BLEDOW:
          self.liczniki_bledow[self.biezaca_druzyna]+=1
          if self.liczniki_bledow[self.biezaca_druzyna] == MAX_LICZBA_BLEDOW:
            self.biezaca_druzyna=przeciwna_druzyna
      self.wydarzenie=BLEDNA_ODPOWIEDZ

  def zakoncz_runde(self,numer_druzyny_wygrywajacej):
    if not self.koniec_rundy:
      self.liczniki_punktow[numer_druzyny_wygrywajacej]+=self.punkty_biezace
      self.punkty_biezace=0
      self.koniec_rundy=True

  def ustaw_biezaca_druzyne(self,nr_druzyny):
    self.zapisz_stan()
    self.biezaca_druzyna=nr_druzyny

  def nowa_runda(self,numer_rundy):
    self.zapisz_stan()
    self.czy_final=False
    self.ktora_runda=numer_rundy
    self.punkty_biezace=0
    self.liczniki_bledow=[0,0]
    self.widoczne_odpowiedzi=[]
    self.biezaca_druzyna=None
    self.koniec_rundy=False
    self.wydarzenie=NOWA_RUNDA

  def kolejna_runda(self):
    self.nowa_runda(self.ktora_runda+1)

  def poprzednia_runda(self):
    self.nowa_runda(self.ktora_runda-1)

  def zapisz_stan(self):
    poprzednie_stany.append(copy.deepcopy(vars(stan)))
    if len(poprzednie_stany) > MAX_POZIOMY_UNDO:
      del poprzednie_stany[0]

  def przywroc_poprzedni_stan(self):
    if poprzednie_stany:
      opis_stanu=poprzednie_stany.pop()
      for n, v in opis_stanu.items():
        setattr(self, n, v)

stan=Stan()
poprzednie_stany=[]