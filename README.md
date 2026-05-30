# BatConCalc

## battery-consume-calc

Laptop Battery Consumption Benchmark tool

![Battery-consume-calc](https://i.imgur.com/o1xgqq6.png)

You can use this tool to calculate the battery consumption of your laptop. This tool supports csv file logging.

## Installation

- Windows

- Linux

- macOS (Apple Silicon, Big Sur 11.0-)

Install via pip, requires Python 3.11+:
```bash
pip install batconcalc
```



## Roadmap

- [x] AFK (Away from Keyboard) detection  
- [x] Battery cycle count monitoring (macOS, Macbook)
- [x] Battery percentage logging
- [x] export to CSV support
- [ ] battery percentage visual graph on main window
  - [ ] hoverable data points (unlike the default Battery settings)
- [ ] terminal / no GUI support using curses
  - [ ] minimizable without tmux

## Usage

When logging is enabled, the tool will log the following format every time battery percentage changes:\
     `[HH:MM:SS] - [BATTERY_PERCENTAGE] | [BATTERY_STATUS] [if AFK] [BATTERY CYCLE (Macbooks only)]`\

You can add ``--help`` or ``-h`` to see the help menu.

```bash
~) batconcalc --help                                                                               ✔ │ playground Py │ at 11:14:43 
usage: batconcalc [-h] [--afk AFK] [--log LOG] [--version] [--foreground]

Laptop Battery Consumption Benchmark tool

options:
  -h, --help    show this help message and exit
  --afk AFK     AFK time in seconds
  --log LOG     Log file path (filetype: .csv)
  --version     show program's version number and exit
  --foreground  Run in foreground (do not detach from terminal)
```