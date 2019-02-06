# TTSS_app
Aplikacja do wyświetlania czasów odjazdów tramwajów z [TTSS api](http://ttss.krakow.pl/).

# Wymagane biblioteki
```
pip install bs4
pip install requests
```

# Używanie programu
Program uruchamiamy poleceniem `main`.

Aplikacja przyjmuje od jednego do trzech argumentów.
Możliwe uruchomienia programu to:

* `main nr_linii` wyświetli przystanki znajdujące się na podanej linii tramwajowej.
* `main nazwa_przystanku` wyświetli informacje o odjazdach z danego przystanku.
