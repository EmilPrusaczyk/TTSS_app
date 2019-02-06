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
