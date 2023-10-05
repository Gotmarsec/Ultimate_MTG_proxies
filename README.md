# Ultimate_MTG_proxies
Generate high-res Magic the Gathering proxy cards!

## Features

- **High resoultion card scans**
  This project uses high resolution card scans from the amazing [Scryfall](https://scryfall.com/) database.
  In case a low resolution artwork was picked, a waring is printed.

- **Intelligent corners**
  When outputting squared cards (in contrast to the original Magic the Gathering round corner card format), the color of each corner is adapted to the border of the card.
  In case of a borderless card, this drastically improves the looks of the proxies.

- **High customizeability**
  Choose to spezify lots of parameters, controlling every aspect of your proxies.

- **Ready to print pdf file**
  The proxies can directly be downloaded as printable pdf file.\
  Make sure to use a good printer and high quality paper for perfect results.

- **Progress indicator""
  Generating the proxies can take quite some time.
  The user is informed about every step taken.

## Installation

1. Clone this repository and submodules
```bash
git clone --recurse-submodules https://github.com/Gotmarsec/Ultimate_MTG_proxies.git
cd Ultimate_MTG_proxies
```

2. Create a Python [virtual environment](https://docs.python.org/3/library/venv.html) and activate it
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
python -m pip install -U Flask
python -m pip install Numpy
python -m pip install mtg-proxies-backend
```

## Usage
In the activate virtual environment, do
```bash
python magic_pdf_gen.py
```
The website is available under port 9093. \
![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) **Warning! Currently the server is only a standard flask developement server and is not save to be exposed to the public internet.**

## Acknowledgements
- [DiddiZ](https://github.com/DiddiZ) for his excellent local [version](https://github.com/DiddiZ/mtg-proxies) of the proxy generator, on which this project is based on.
- [Scryfall](https://scryfall.com/) for their [amazing API](https://scryfall.com/docs/api).
