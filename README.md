## Simple times tables rockstars bot written in selenium

# Features

- Garage mode
- Studio mode
- You can choose the seconds / question (speed) you want to reach (eg. 2s/q)
- Simple error and crash detection with comprehensive logs

# How to use

Create a file called "secret.env". In it, add these lines with your own data:

USER=[Insert Username Here]

PASSWORD=[Insert Password Here]

POSTCODE=[Insert School Postcode Here]

(This information is necessary to allow the bot to log in to your account)

Then, run main.py in the virtual environment (or run start.bat, it does the same thing)

Then, change settings using console to your desire and select a mode to play. The program will automatically log in to your account, and begin playing.

# Todo:

- Allow selenium to begin from an already logged-in state (using cookies, probably)
- Add support for all modes
- Allow for variance (eg. answer a question with +-0.1s of speed to appear more human-like)
- Allow for intentional incorrect answers (eg. 1 in 5 chance to answer a question incorrectly)
- Add GUI
