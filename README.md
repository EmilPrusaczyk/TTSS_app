# TTSS_app
Aplikacja do wyświetlania czasów odjazdów tramwajów z [TTSS API](http://ttss.krakow.pl/).

# Wymagane biblioteki
Program używa bibliotek **Beautiful Soup 4** oraz **Requests** do pobierania danych z publicznych API MPK Kraków.
```
pip install bs4
pip install requests
```

# Używanie programu
Program uruchamiamy poleceniem `main`.

Aplikacja przyjmuje od jednego do trzech argumentów:
```
main nr_linii nazwa_przystanku kierunek
```
Argument `nr_linii` musi być liczbą, a `kierunek`, jeśli podany, musi znajdować się na końcu.

Możliwe uruchomienia programu to:

* `main nr_linii` wyświetli przystanki znajdujące się na podanej linii tramwajowej.
* `main nazwa_przystanku` wyświetli informacje o odjazdach z danego przystanku.
* `main nr_linii nazwa_przystanku` wyświetli odjazdy tramwajów danej linii z danego przystanku.
* `main nazwa_przystanku kierunek` wyświetli odjazdy tramwajów z danego przystanku w wybranym kierunku.
* `main nr_linii nazwa_przystanku kierunek` wyświetli odjazdy tramwajów danej linii z danego przystanku w wybranym kierunku.

### Przykład
```
> main "kampus uj"

Przystanek Kampus UJ
Linie 11, 18, 52

Właśnie odjechały:
22:14 [18] Czerwone Maki P+R
22:11 [18] Krowodrza Górka

Obecny rozkład:
22:20 [11] Czerwone Maki P+R
22:23 [52] Os.Piastów
22:23 [52] Czerwone Maki P+R
22:25 [11] Mały Płaszów
22:29 [18] Czerwone Maki P+R
22:31 [18] Krowodrza Górka
22:35 [11] Czerwone Maki P+R
22:38 [52] Os.Piastów
```

Wprowadzanie danych możliwe jest z drobnymi błędami. Program pozwoli wybrać poprawne nazwy przystanków bazując na [odległości Levenshteina](https://pl.wikipedia.org/wiki/Odleg%C5%82o%C5%9B%C4%87_Levenshteina).

```
> main "ruczaaaaj" 52
Czy chodziło Ci o:
1) Ruczaj
2) Reymana
3) Kurdwanów
4) Borsucza
5) Słomiana
0) WYJDŹ
Wybór: 1
Przystanek Ruczaj
Linie 11, 18, 52

Właśnie odjechały:

Obecny rozkład:
22:39 [52] Os.Piastów
22:37 [52] Czerwone Maki P+R
22:52 [52] Czerwone Maki P+R
22:54 [52] Os.Piastów
```
