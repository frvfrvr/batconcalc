# BatConCalc

## battery-consume-calc

Laptop Battery Consumption Benchmark tool

![Battery-consume-calc](https://i.imgur.com/o1xgqq6.png)

You can use this tool to calculate the battery consumption of your laptop. This tool supports csv file logging.

## Installation

- Windows

- Linux

- macOS (Apple Silicon, Big Sur 11.0-)

## Roadmap

- [x] AFK (Away from Keyboard) detection  
- [x] Battery cycle count monitoring (macOS, Macbook)
- [x] Battery percentage logging
- [x] export to CSV support
- [ ] battery percentage visual graph on main window
  - [ ] hoverable data points (unlike the default Battery settings)

## Usage

When logging is enabled, the tool will log the following format every time battery percentage changes:\
     `[HH:MM:SS] - [BATTERY_PERCENTAGE] | [BATTERY_STATUS] [if AFK] [BATTERY CYCLE (Macbooks only)]`\
