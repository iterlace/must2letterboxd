# Must to Letterboxd Exporter

## Python

### Version
Since dataclasses are used, **the lowest version supported is Python 3.7**.  
You can download the newest release at https://www.python.org/downloads/

### Packages
Before script execution, you need to install `requests` library:
```bash
$ python3 install requests
```

## Usage

### 1. Export to .csv
Just provide a Must username. The rest is ours.

<img src="docs/media/username.png" width="320" alt="Settings Screenshot"/>

```bash
$ python3 main.py

Enter your Must username: iterlace

Exported Want list to /tmp/must2letterboxd/want.csv
Exported Watched list to /tmp/must2letterboxd/want.csv
```

### 2. Import .csv to Letterbox
Now you can upload:
 - **watched.csv** using a [direct link](https://letterboxd.com/import/)
 - **want.csv** to the [watchlist](https://letterboxd.com/iterlace/watchlist/)
