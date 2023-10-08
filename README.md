# BatConCalc
## battery-consume-calc

Laptop Battery Consumption Benchmark tool

![Battery-consume-calc](https://i.imgur.com/d2H1aXQ.png)

You can use this tool to calculate the battery consumption of your laptop. This tool supports csv file logging.

## Installation

- Windows

- Linux

- macOS (Apple Silicon, Big Sur 11.0-)

## Roadmap

- [x] AFK (Away from Keyboard) / BTK (Back to Keyboard) button for logging
  - [x] Logging to file. Example:  
          09:14:31 80% - Battery charges 1% every 1 minute, 1 second  
          09:15:31 80% - Battery charges, user is away from keyboard  
          16:05:33 80% - Battery charges, user is back to keyboard  
          16:05:33 79% - Battery consumes 1% every 6 hours, 51 minutes, 2 seconds  
- [x] Battery cycle count monitoring (macOS, Macbook)
- [x] Add date on log file when battery percentage changes next day
- [x] Fix minor grammar issue when only hours and seconds are rendered
- [ ] export to CSV support
- [ ] battery percentage visual graph on main window
  - [ ] hoverable data points (unlike the default Battery settings)

## Build

Requires Python 3.8+ and Pyinstaller

     pip install pyinstaller
     pyinstaller --onefile --icon=icon.ico --clean --windowed --name=battery-consume-calc battery-consume-calc.py

## Usage

When logging is enabled, the tool will log the following format every time battery percentage changes:\
     `[HH:MM:SS] [Battery percentage] - [Battery percentage change] [Date if percentage changes next day] [Battery cycle count (for Macbook)]`
