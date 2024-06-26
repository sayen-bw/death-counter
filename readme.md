# Description
A counter displaying deaths/countings!
You can freely drag it around and place it on your screen wherever you like.

## Controlling the application
The following keys control the app. Other keys wont be logged or recognized!
- F7: Save current position of the window for next time
- F8: Increment death by 1
- F9: Close application and save deaths to file

## Execute the application
You can execute the app via the .exe in the release bundle.
Manually you can create a venv and install the requirements:

### Manually Linux
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 death_counter.pyw
```
### Manually Windows
```
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python death_counter.pyw
```