import requests
import argparse
from bs4 import BeautifulSoup

STOPS = None


def get_stops():
    '''Return a dictionary containing information about
    all tram stops from the TTSS api.'''
    global STOPS
    if STOPS:
        return STOPS

    url = 'http://www.ttss.krakow.pl/internetservice/geoserviceDispatcher/services/stopinfo/stops?left=-648000000&bottom=-324000000&right=648000000&top=324000000'
    r = requests.get(url).json()['stops']
    if not STOPS:
        STOPS = r
    return r


def get_stop_json(stop_name):
    '''Return a json from the api with info about the given stop.'''
    stops = get_stops()
    stopID = None
    for stop in stops:
        if stop['name'] == stop_name:
            stopID = stop['shortName']
            break
    return requests.get('http://www.ttss.krakow.pl/internetservice/services/passageInfo/stopPassages/stop?stop='+stopID).json()


def ldist(a, b):
    '''Calculate the Levenshtein distance between two strings.'''
    m = len(a)+1
    n = len(b)+1
    d = [[i]+[0]*(n-1) for i in range(m)]
    d[0] = list(range(n))
    for j in range(1, n):
        for i in range(1, m):
            d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1,
                          d[i-1][j-1] + char_diff(a[i-1], b[j-1]))
    return d[m-1][n-1]


def char_diff(a, b):
    '''Determine the difference between two chars, check for lazy spelling'''
    if a == b:
        return 0
    c = {'a': 'ą', 'e': 'ę', 'o': 'ó', 's': 'ś', 'l': 'ł',
         'z': 'żź', 'c': 'ć', 'n': 'ń', 'ź': 'zż', 'ż': 'zź'}
    if b in c.keys() and a in c[b] or a in c.keys() and b in c[a]:
        return 0.5
    return 1


def get_lines():
    '''Return a list of all tram line numbers'''
    r = requests.get('http://rozklady.mpk.krakow.pl/')
    soup = BeautifulSoup(r.content, features='html.parser')
    lines = soup.find_all('td', class_='linia_table_left')
    out = []
    lines_ = lines[0].find_all('a', class_='linia')
    out += [int(line.string) for line in lines_]
    lines_ = lines[1].find_all('a', class_='liniaN')
    out += [int(line.string) for line in lines_]
    lines_ = lines[2].find_all('a', class_='linia')
    out += [int(line.string) for line in lines_]
    return out


def print_line_info(n):
    '''Print stops for the specified line'''
    r = requests.get('http://www.ttss.krakow.pl/internetservice/services/lookup/autocomplete/json?query='+str(n)).json()
    routeID = r[1]['id']
    r = requests.get('http://www.ttss.krakow.pl/internetservice/services/routeInfo/routeStops?routeId='+str(routeID)).json()
    r = r['stops']
    stops = [stop['name'] for stop in r]
    print(f'Linia {n}')
    print(f'Przystanki na tej trasie:')
    print(', '.join(stops))


def normalize_name(s):
    return s.lower().replace('.', '')


def pick_stop(stop):
    '''Returns matching stop name or provides option for user input'''
    stops = [s['name'] for s in get_stops()]
    stops = map(lambda x: (x, ldist(stop, normalize_name(x))), stops)
    stops_ = sorted(stops, key=lambda x: x[1])
    stop = None
    if stops_[0][1] < 3:
        return stops_[0][0]
    elif stops_[0][1] > 10:
        print('Podany przystanek nie istnieje.')
        return None
    else:
        print('Czy chodziło Ci o przystanek:')
        for i, stop in enumerate(stops_[:5]):
            print(f'{i+1}) {stop[0]}')
        print('0) WYJDŹ')
        n = int(input('Wybór: '))
        print('')
        if n == 0:
            return None
        return stops_[n-1][0]


def pick_direction(stop, direction):
    '''Returns matching direction name or provides option for user input.
       Only choose from directions matching given stop.'''
    r = get_stop_json(stop)
    ds = sum((route['directions'] for route in r['routes']), [])
    if not ds:
        return None
    ds = list(set(ds))
    ds = map(lambda x: (x, ldist(direction, normalize_name(x))), ds)
    ds_ = sorted(ds, key=lambda x: x[1])
    direction = None
    if ds_[0][1] < 3:
        return ds_[0][0]
    elif ds_[0][1] > 10:
        print('Podany kierunek nie istnieje.')
        return None
    else:
        print('Czy chodziło Ci o kierunek:')
        for i, direction in enumerate(ds_[:5]):
            print(f'{i+1}) {direction[0]}')
        print('0) WYJDŹ')
        n = int(input('Wybór: '))
        print('')
        if n == 0:
            return None
        return ds_[n-1][0]


def print_stop_info(name, direction=None, line=None):
    '''Print departures from the given stop.
       If direction is given, only print lines going in that direction.
       If line is given, only print those lines.'''
    r = get_stop_json(name)
    print(f'Przystanek {name}')

    if line:
        r['actual'] = [t for t in r['actual'] if t['patternText'] == line]
        r['old'] = [t for t in r['old'] if t['patternText'] == line]
    if direction:
        r['actual'] = [t for t in r['actual'] if t['direction'] == direction]
        r['old'] = [t for t in r['old'] if t['direction'] == direction]
        r['routes'] = [t for t in r['routes'] if direction in t['directions']]
    if not line:
        print(f'Linie {", ".join(x["name"] for x in r["routes"])}')
    print('\nWłaśnie odjechały:')
    for t in r['old']:
        print(f"{t['plannedTime']} [{t['patternText']}] {t['direction']}")
    print('\nObecny rozkład:')
    for t in r['actual']:
        print(f"{t['plannedTime']} [{t['patternText']}] {t['direction']}")


def val_line(line):
    '''Check if a line exists'''
    line = int(line)
    lines = get_lines()
    if line not in lines:
        print('Linia o podanym numerze nie istnieje.')
        return False
    return True


def val_stop_line(stop, line):
    '''Check if a stop belongs to a line'''
    line = str(line)
    r = get_stop_json(stop)
    for route in r['routes']:
        if route['name'] == line:
            return True
    print('Przystanek nie obsługuje podanej linii.')
    return False


def val_stop_direction(stop, direction):
    '''Check if a stop belongs to a line going in the given direction'''
    r = get_stop_json(stop)
    for route in r['routes']:
        if direction in route['directions'].values():
            return True
    print('Przystanek nie obsługuje linii w podanym kierunku.')
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("c", nargs='+',
                        help='Search criteria, e.g. 52 "kampus uj"\
                              when direction is given, it must be last.')
    args = parser.parse_args()

    if len(args.c) == 1:
        arg = args.c[0]
        if arg.isdigit():
            arg = int(arg)
            # podano numer linii
            if val_line(arg):
                print_line_info(arg)
        else:
            # podano nazwę przystanku
            stop = pick_stop(arg)
            if stop:
                print_stop_info(stop)

    elif len(args.c) == 2:
        if args.c[0].isdigit() or args.c[1].isdigit():
            # linia, przystanek
            line, stop = args.c[0], args.c[1]
            if stop.isdigit():
                line, stop = stop, pick_stop(line)
            else:
                stop = pick_stop(stop)
            if val_line(line) and val_stop_line(stop, line):
                print_stop_info(stop, line=line)
        else:
            # przystanek, kierunek
            stop, direction = args.c[0], args.c[1]
            stop = pick_stop(stop)
            if stop:
                direction = pick_direction(stop, direction)
                if not direction:
                    print('')
                print_stop_info(stop, direction=direction)
    elif len(args.c) == 3:
        line, stop, direction = args.c[0], args.c[1], args.c[2]
        if stop.isdigit():
            line, stop = stop, line
        line = int(line)
        stop = pick_stop(stop)
        direction = pick_direction(stop, direction)
        print_stop_info(stop, direction=direction, line=line)
    else:
        print('Podano nieprawidłową liczbę argumentów.')
