This prototype keeps data in memory for the assessment2 video and presentation.

Folder layout
-------------
VolleyCall-App/
  app_demo.py
  requirements_demo.txt
  templates/
  static/
    css/stylesheet.css
    images/

How to install and run (Windows)
--------------------------------
1) Open VS Code in the repo folder “VolleyCall-App”.
2) Open Terminal.
3) Create and activate a fresh venv:
   python -m venv .venv
   .\.venv\Scripts\Activate
4) Install minimal deps:
   pip install -r requirements_demo.txt
5) Run the demo server:
   python app_demo.py
6) Open http://127.0.0.1:5000

How to install and run (macOS or Linux)
---------------------------------------
1) Open VS Code in the repo folder “VolleyCall-App”.
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
- organiser: ernesto@example.com / test
- player:    eleonora@example.com / test
- player:    john@example.com / test

Features in the demo
--------------------
- Login and registration with roles (organiser, player)
- Organiser creates a match: title, date, time, location, capacity, notes
- Match detail: RSVP, Paid / Unpaid badges, attendee chips
- Dashboards: 2×2 cards on desktop, responsive on mobile
- NZ short date format: dd/mm/yyyy h:mm am/pm
- UI: single stylesheet, glass slab over the background for contrast, centred branding, clear button hierarchy
- Login and registration with roles (organiser, player)

Routes
------
- /               index with upcoming matches
- /login          sign in
- /register       sign up
- /dashboard      player or organiser dashboard
- /matches/new    create a match
- /matches/<id>   match detail with RSVP
- / index with upcoming matches

Notes and limits
----------------
- In memory only. Data resets on server restart.
- For the assessment prototype. No email is sent yet.
- No organiser password gate in this demo. It can be added later if needed.
- Images and CSS live under static/. Templates under templates/.
