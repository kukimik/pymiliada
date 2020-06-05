# Pymiliada

Pymiliada - symulator popularnego teleturnieju, napisany (na kolanie) w Pythonie przy użyciu Pygame. Do wykorzystania przy prowadzeniu imprez.

## Klawisze

* `1` - `9` - wyświetl odpowiedź o odpowiednim numerze;
* `b` - błędna odpowiedź;
* `,` - pojedynek na początku rundy wygrała drużyna po lewej;
* `.` - pojedynek na początku rundy wygrała drużyna po prawej;
* `strzałka w prawo` - kolejna runda;
* `strzałka w lewo` - poprzednia runda;
* `Backspace` - cofnij ostatnią czynność;
* `Escape` - koniec gry.

## Typowy przebieg gry

Poniższy schemat powtarza się w każdej rundzie.

1. Rozpoczynamy od pojedynku. Prowadzący czyta pytanie. Która drużyna szybciej naciśnie przycisk, ta odpowiada.
2. Postępujemy odpowiednio od tego jaka odpowiedź padła:
   * jeśli padła najwyżej punktowana odpowiedź (o numerze `1`), to naciskamy `1` aby ją wyświetlić, a następnie `,` lub `.`, żeby wskazać która drużyna jej udzieliła;
   * jeśli odpowiedź była błędna, to naciskamy `b` i odpowiada drużyna przeciwna;
   * jeśli padła odpowiedź o numerze `2` do `9`, to naciskamy klawisz odpowiadający numerowi odpowiedzi i następnie odpowiada drużyna przeciwna.

  Jeśli druga drużyna udzieliła lepszej odpowiedzi niż pierwsza, to wskazujemy ją przy użyciu klawisza `,` lub `.`. Jeśli obie drużyny odpowiedziały błędnie, to odpowiadają na przemian do momentu aż (zgodnie z regułami znanymi z teleturnieju) któraś z nich zostanie wybrana przy uzyciu `,` lub `.`.

3. Wybrana drużyna odpowiada. Jeśli udzieli poprawnej odpowiedzi, to używamy odpowiedniego klawisza `1` - `9`. Jeśli błędnej, to `b`.
4. Jeśli wszystkie poprawne odpowiedzi zostaną udzielone, to runda się kończy, a drużyna która odpowiadała dostaje punkty. Przechodzimy do kolejnej rundy przy użyciu `strzałki w prawo`.
5. Jeśli drużyna udzieli trzech błędnych odpowiedzi, to odpowiada drużyna przeciwna.
   * Jeśli odpowie poprawnie to naciskamy odpowiedni klawisz `1` - `9` i drużyna ta wygrywa rundę (dostaje punkty).
   * Jeśli odpowie błędnie, to naciskamy `b`, drużyna ta przegrywa rundę (punkty dostaje drużyna, która odpowiadała jako pierwsza).
6. Jeśli runda skończyła się zanim udzielono wszystkich poprawnych odpowiedzi, to możemy pokazać pokazać odpowiedzi które nie zostały udzielone przy użyciu klawiszy `1` - `9`. Nie będą za nie naliczane punkty. Następnie przechodzimy do kolejnej rundy przy użyciu `strzałki w prawo`.

Klawisze `strzałka w lewo` i `Backspace` można stosować w sytuacjach awaryjnych.

## Pliki konfiguracyjne

### config.yml

Plik zawiera konfigurowalne elementy gry inne niż pytania:

* rozdzielczości ekranu;
* ściezki na dysku do obrazów, dźwięków i czcionek;
* rozmiary i kolory czcionek (kolor w formacie [R,G,B]);
* ścieżkę do pliku z pytaniami;
* współrzędne elementów na ekranie;
* treść stałych elementów tekstowych.

Modyfikując ten plik oraz obrazki/dźwięki/czcionki można dostosować wygląd gry do własnych potrzeb.

### dane/pytania.yml

Plik zawiera dane, które należy dostosować przed każdą prowadzoną rozgrywką:

* nazwy drużyn;
* kolejne pytania, odpowiedzi i punkty przysługujące za danę odpowiedź;

## TODO

* mnożnik punktów w rundach ("W n-tej rundzie liczbę punktów mnożymy przez x.") i wyświetlacz z przemnożoną liczbą punktów nad tablicą z odpowiedziami;
* runda finałowa;
* klawisz pozwalający wyświetlić (np. na pasku u dołu ekranu) aktualne pytanie;
* konfigurowalne klawisze (?).