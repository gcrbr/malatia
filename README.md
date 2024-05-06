# Malatìa
![Interface](https://i.imgur.com/FtfGzuL.png)
![Map](https://i.imgur.com/H9J8M9f.png)

Tool to disappear at low cost and under mysterious circumstances.

This program deals with searching for low-cost trips on different carriers from a predetermined departure location to designated locations or otherwise offered by the carrier.

The results are viewable through an interface made with HTML, CSS and basic JavaScript. 

This simply displays the contents of the `data.json` file in a readable table format.

## Supported carriers
| Ryanair            | FlixBus            | Italo | Volotea | Wizz Air | Trenitalia | Itabus | easyJet |
|--------------------|--------------------|-------|---------|----------|------------|--------|------|
| ✓ | ✓ | ✓ |         |          | ✓ | ✓ | | |

Note: Some carriers such as _Itabus_, _Trenitalia_ and _Italo_, are only available in Italy.

## Installation
The only required dependencies are `dateutil` and `requests`, you can install them with the following command:
```bash
pip install python-dateutil requests
```

## Usage
To start the program:
```bash
python main.py
````

To run and view the interface you can use the parameter `-i` or `--interface`:
```bash
python main.py -i
````

You can see the other options by using the parameter `-h` or `--help`.

## Configuration
Within the `config.json` file it is possible to change:
- The starting city from which to search for trips
- The supported cities
- The price cap for the trips
- The time delay between searches (in seconds)

It is important to make sure that the city selected as the departure supports all the carriers used. 

In short - you need to verify that for the given city, all fields within `identifiers` are properly filled.

## Credits
[Svein Kåre Gunnarson](https://dionaea.com/) for the [DotMatrix](https://www.dafont.com/dot-matrix.font) font

## Technologies used
- LeafletJS: Map interface
- Yandex maps: Geocoding API