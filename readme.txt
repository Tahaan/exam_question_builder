  1. Installation:
 ------------------

Set up a V-env with required modules installed
LINUX:
   python -m venv env
   pip install -r requirements.txt

WINDOWS:
   pip install virtualenv
   mkvirtualenv env
   \env\Scripts\activate.bat
   pip install -r requirements.txt

  2. Usage:
 -----------

Run the app within the virtual-env
LINUX:
   . env/bin/activate
   python main.py


WINDOWS:
   virtualenv env
   \env\Scripts\activate.bat
   python main.py
