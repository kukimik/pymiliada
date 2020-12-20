#!/usr/bin/python
# -*- coding: utf-8 -*-

from konfiguracja import liczba_odpowiedzi, liczba_punktow, mnoznik
import copy

MAX_POZIOMY_UNDO=8000

BLEDNA_ODPOWIEDZ='snd_bledna_odpowiedz'
POPRAWNA_ODPOWIEDZ='snd_poprawna_odpowiedz'
KONIEC_RUNDY='snd_koniec_rundy'
NOWA_RUNDA='snd_nowa_runda'

MAX_LICZBA_BLEDOW=3

class Stan:
  def __init__(self):
    self.ktora_runda=0
    self.punkty_biezace=0
    self.liczniki_bledow=[0,0]
    self.liczniki_punktow=[0,0]
    self.widoczne_odpowiedzi=[]
    self.biezaca_druzyna=None
    self.dzwieki_wydarzen=[]
    self.koniec_rundy=False

  def poprawna_odpowiedz(self,numer_odpowiedzi):
    if self.koniec_rundy \
        or self.biezaca_druzyna is not None \
        or (self.biezaca_druzyna is None and len(self.widoczne_odpowiedzi) < 2 and 0 not in self.widoczne_odpowiedzi):
      if numer_odpowiedzi < liczba_odpowiedzi(self.ktora_runda) and numer_odpowiedzi not in self.widoczne_odpowiedzi:
        self.zapisz_stan()
        self.widoczne_odpowiedzi.append(numer_odpowiedzi)
        self.dzwieki_wydarzen.append(POPRAWNA_ODPOWIEDZ)
        if not self.koniec_rundy:
          self.punkty_biezace+=liczba_punktow(self.ktora_runda,numer_odpowiedzi)
          if self.biezaca_druzyna is not None and \
              (len(self.widoczne_odpowiedzi) == liczba_odpowiedzi(self.ktora_runda) \
               or self.liczniki_bledow[{0:1,1:0}[self.biezaca_druzyna]] == MAX_LICZBA_BLEDOW):
            self.zakoncz_runde(self.biezaca_druzyna)

  def bledna_odpowiedz(self):
    if not self.koniec_rundy:
      if self.biezaca_druzyna is not None:
        przeciwna_druzyna={0:1,1:0,None:None}[self.biezaca_druzyna]
        self.zapisz_stan()
        self.dzwieki_wydarzen.append(BLEDNA_ODPOWIEDZ)
        if self.liczniki_bledow[przeciwna_druzyna] == MAX_LICZBA_BLEDOW:
          self.liczniki_bledow[self.biezaca_druzyna]=1
          self.zakoncz_runde(przeciwna_druzyna)
        elif self.liczniki_bledow[self.biezaca_druzyna] < MAX_LICZBA_BLEDOW:
          self.liczniki_bledow[self.biezaca_druzyna]+=1
          if self.liczniki_bledow[self.biezaca_druzyna] == MAX_LICZBA_BLEDOW:
            self.biezaca_druzyna=przeciwna_druzyna
      elif len(self.widoczne_odpowiedzi) < 2 and 0 not in self.widoczne_odpowiedzi:
        self.dzwieki_wydarzen.append(BLEDNA_ODPOWIEDZ)


  def zakoncz_runde(self,numer_druzyny_wygrywajacej):
    if not self.koniec_rundy:
      self.liczniki_punktow[numer_druzyny_wygrywajacej]+=self.punkty_przemnozone()
      self.punkty_biezace=0
      self.koniec_rundy=True
      self.biezaca_druzyna=None
      self.dzwieki_wydarzen.append(KONIEC_RUNDY)

  def ustaw_biezaca_druzyne(self,nr_druzyny):
    if not self.koniec_rundy and self.widoczne_odpowiedzi:
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
    self.dzwieki_wydarzen.append(NOWA_RUNDA)

  def kolejna_runda(self):
    self.nowa_runda(self.ktora_runda+1)

  def poprzednia_runda(self):
    self.nowa_runda(self.ktora_runda-1)

  def zapisz_stan(self):
    poprzednie_stany.append(copy.deepcopy(vars(stan)))
    poprzednie_stany[-1]['dzwieki_wydarzen']=[]
    if len(poprzednie_stany) > MAX_POZIOMY_UNDO:
      del poprzednie_stany[0]

  def przywroc_poprzedni_stan(self):
    if poprzednie_stany:
      opis_stanu=poprzednie_stany.pop()
      for n, v in opis_stanu.items():
        setattr(self, n, v)

  def punkty_przemnozone(self):
    return mnoznik(self.ktora_runda) * self.punkty_biezace

stan=Stan()
poprzednie_stany=[]