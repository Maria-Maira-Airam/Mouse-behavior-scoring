## Mouse-behavior-scoring
Python codes for scoring of mouse social/non-social behavior. Created for PhD thesis purposes.

## Behavioral Scoring Tools for Mouse Experiments

This repository contains three Python applications designed for manual scoring of mouse behaviors in different experimental settings. All tools provide real-time tracking of frequency and duration of key behaviors and are suitable for  home-cage monitoring, reciprocal social interaction (RSI), including social and non-social behavior.

The scripts were developed as part of a thesis project examining autism-related behavioral phenotypes in mice.

# Contents

OF_buttons_keys.py — Open Field / home-cage spontaneous behavior counter

RSI.py — Social interaction behavior counter

RSI_nonsocial.py — Non-social behavior counter

# Common Features

All three tools include:

- Graphical user interface built with tkinter

- Tracking of frequency and duration

- Button-based and keyboard-based scoring

- Real-time updates of displayed values

- Timestamped Save Results function (.csv or .xlsx)

- Reset functionality to start new trials



# 1 Home-Cage Behavior Counter
File: OF_buttons_keys.py

Moving	Q (Frequency Key)	A (Duration Key; hold)
Grooming	W	(Frequency Key) S (Duration Key; hold)
Rearing	P (Frequency Key)	L (Duration Key; hold)

💾 Output
Saved as .csv (Behavior, Frequency, Total Duration (s))

Notes
Uses only standard libraries (tkinter, csv, time, etc.).

# 2 Social Behavior Counter (RSI)
File: RSI.py

Sniffing	Y	
Following	X	
Mounting	M	
Push & Crawl	N	
Allogrooming	O	
Affiliative	P	

💾 Output
Saved as .xlsx (Event, Frequency, Total Duration (s))

Notes
- Uses the same key for duration (press and hold) and frequency (just press and release)
- Uses pynput for background keyboard listening
- Tracks durations continuously and updates the GUI every 100 ms

# 3 Non-Social Behavior Counter
File: RSI_nonsocial.py

Digging	Q (Frequency Key)	A (Duration Key; hold)
Grooming	W	(Frequency Key) S (Duration Key; hold)
Rearing	P (Frequency Key)	L (Duration Key; hold)
Social avoidance	O (Frequency Key)	Space (Duration Key; hold)

💾 Output
Saved as .csv (Behavior, Frequency, Total Duration (s))

Notes:
If Social avoidance frequency = 0 → exported as "NaN".



## Installation
Requirements
Python 3.8+

For RSI.py:
pip install openpyxl pynput

The other scripts use only Python standard libraries.

## Running the Applications

From the command line:
python OF_buttons_keys.py
python RSI.py
python RSI_nonsocial.py

A GUI window will open automatically.

Tip: The keyboard shortcuts work only while the window is focused.
