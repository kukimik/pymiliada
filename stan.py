#!/usr/bin/python
# -*- coding: utf-8 -*-

BLEDNA_ODPOWIEDZ=0
POPRAWNA_ODPOWIEDZ=1
NOWA_RUNDA=2

class Stan:
  def __init__(self):
    self.ktora_runda=0
    self.punkty_biezace=0
    self.liczniki_bledow=[0,0]
    self.liczniki_punktow=[0,0]
    self.widoczne_odpowiedzi=[]
    self.wydarzenie=None

  def poprawna_odpowiedz(self,numer_odpowiedzi,liczba_punktow):
    if (numer_odpowiedzi not in self.widoczne_odpowiedzi):
      self.widoczne_odpowiedzi.append(numer_odpowiedzi)
      self.punkty_biezace+=liczba_punktow
      self.wydarzenie=POPRAWNA_ODPOWIEDZ

  def bledna_odpowiedz(self,nr_druzyny):
    self.liczniki_bledow[nr_druzyny]+=1
    self.wydarzenie=BLEDNA_ODPOWIEDZ

  def dodaj_punkty(self,nr_druzyny):
    self.liczniki_punktow[nr_druzyny]+=self.punkty_biezace

  def zabierz_punkty(self,nr_druzyny):
    self.liczniki_punktow[nr_druzyny]-=self.punkty_biezace

  def kolejna_runda(self):
    self.nowa_runda(self.ktora_runda+1)

  def poprzednia_runda(self):
    self.nowa_runda(self.ktora_runda-1)

  def nowa_runda(self,numer_rundy):
    self.czy_final=False
    self.ktora_runda=numer_rundy
    self.punkty_biezace=0
    self.liczniki_bledow=[0,0]
    self.widoczne_odpowiedzi=[]
    self.wydarzenie=NOWA_RUNDA

stan=Stan()