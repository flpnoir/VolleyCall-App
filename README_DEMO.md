README_DEMO.md
==============
This demo runs inside your existing repo "VolleyCall-App" without a database.
It uses in-memory data for the assessment video and presentation.

Folder layout to add inside your repo:
VolleyCall-App/
  app_demo.py
  requirements_demo.txt
  demo_prototype/
    templates/
    static/

How to install and run (Windows)
--------------------------------
1) Open VS Code in the repo folder "VolleyCall-App".
2) Open Terminal.
3) Create and activate a fresh venv:
   py -m venv .venv
   .venv\Scripts\activate
4) Install minimal deps:
   pip install -r requirements_demo.txt
5) Run the demo server:
   python app_demo.py
6) Open http://127.0.0.1:5000

How to install and run (macOS or Linux)
---------------------------------------
1) Open VS Code in the repo folder "VolleyCall-App".
2) Open Terminal.
3) Create and activate a fresh venv:
   python3 -m venv .venv
   source .venv/bin/activate
4) Install minimal deps:
   pip install -r requirements_demo.txt
5) Run the demo server:
   python app_demo.py
6) Open http://127.0.0.1:5000

Test users
----------
- Organizer: ernesto@example.com / test
- Player: eleonora@example.com / test
- Player: john@example.com / test

Main pages
----------
- /
- /login
- /dashboard
- /matches/new
- /matches/<id>
