# battery-consume-calc

Laptop Battery Consumption Benchmark tool

[![Build Status](https://travis-ci.org/jkreps/battery-consume-calc.svg?branch=master)](https://travis-ci.org/jkreps/battery-consume-calc)
[![Coverage Status](https://coveralls.io/repos/jkreps/battery-consume-calc/badge.svg?branch=master)](https://coveralls.io/r/jkreps/battery-consume-calc?branch=master)
[![Code Climate](https://codeclimate.com/github/jkreps/battery-consume-calc/badges/gpa.svg)](https://codeclimate.com/github/jkreps/battery-consume-calc)
![GitHub stars](https://img.shields.io/github/stars/jkreps/battery-consume-calc.svg)
![GitHub forks](https://img.shields.io/github/forks/jkreps/battery-consume-calc.svg)

![](https://i.imgur.com/d2H1aXQ.png)

You can use this tool to calculate the battery consumption of your laptop. This tool supports text file logging.
## Installation

- Windows

- Linux

- macOS (Apple Silicon, Big Sur 11.0-)

## Roadmap

- Fixing time interval (issue - 11:03 AM and 12:57 PM will show "1 hour, 60 minutes")
    - testing

## Build

Requires Python 3.8+ and Pyinstaller

     pip install pyinstaller
     pyinstaller --onefile --icon=icon.ico --clean --windowed --name=battery-consume-calc battery-consume-calc.py

## Usage