# battery-consume-calc

Laptop Battery Consumption Benchmark tool

[![Build Status](https://travis-ci.com/frvfrvr/battery-consume-calc.svg?branch=master)](https://travis-ci.com/frvfrvr/battery-consume-calc)
[![Coverage Status](https://coveralls.io/repos/frvfrvr/battery-consume-calc/badge.svg?branch=master)](https://coveralls.io/r/frvfrvr/battery-consume-calc?branch=master)
![GitHub stars](https://img.shields.io/github/stars/frvfrvr/battery-consume-calc.svg)
![GitHub forks](https://img.shields.io/github/forks/frvfrvr/battery-consume-calc.svg)

![Battery-consume-calc](https://i.imgur.com/d2H1aXQ.png)

You can use this tool to calculate the battery consumption of your laptop. This tool supports text file logging.

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

## Build

Requires Python 3.8+ and Pyinstaller

     pip install pyinstaller
     pyinstaller --onefile --icon=icon.ico --clean --windowed --name=battery-consume-calc battery-consume-calc.py

## Usage

When logging is enabled, the tool will log the following format every time battery percentage changes:\
     `[HH:MM:SS] [Battery percentage] - [Battery percentage change] [Date if percentage changes next day] [Battery cycle count (for Macbook)]`
