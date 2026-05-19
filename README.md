# EQX Doubles Finder — Python + Flask Edition 🐍

This is a Python rewrite of the EQX Doubles Finder web app. It connects to
the same Supabase backend as the original, but instead of calling Supabase
directly from JavaScript in the browser, a Python Flask server sits in the
middle and handles all database communication.

---

## What is Python?

Python is a **general-purpose programming language** created by Guido van Rossum
in 1991. It's designed to be readable — the syntax looks almost like plain English —
which makes it one of the most popular languages for beginners and experts alike.

**Python is interpreted.** This means there is no build step. You write a `.py` file,
type `python app.py` in the terminal, and the Python interpreter reads your file
**line by line, top to bottom**, executing each instruction immediately as it goes.

Compare this to **compiled languages** like Swift, Go, C, or Rust:

| | Interpreted (Python) | Compiled (Swift / Go / C) |
|---|---|---|
| **Run it by...** | `python app.py` | First compile: `swiftc app.swift -o app`, then run: `./app` |
| **Build step?** | ❌ None | ✅ Required |
| **Error discovery** | At runtime (as lines execute) | At compile time (before running) |
| **Speed** | Generally slower | Generally faster |
| **Dev cycle** | Fast — edit & run immediately | Slower — must recompile |

Python is used everywhere: web apps, data science, machine learning/AI, automation,
scripting, APIs, and more. The Python ecosystem has hundreds of thousands of
open-source packages on [PyPI](https://pypi.org).

---

## What is Flask?

Flask is a **micro web framework** for Python. "Micro" means it gives you the
minimum you need to build a web server without imposing opinions on how you
structure your app.

When you run `python app.py`, Flask:
1. Starts a web server listening on `localhost:5000`
2. Waits for HTTP requests from browsers
3. Matches each request's URL to a Python function (called a **route**)
4. Calls that function and sends its return value back to the browser

Flask uses **Jinja2** for HTML templates — Python variables and logic (loops,
conditionals) can be embedded directly in `.html` files using `{{ }}` and `{% %}` tags.

---

## How This Compares to the Original

### Original (plain HTML + JS)
```
Browser ──────────────────────────────────────────────► Supabase
          JS calls supabase-js directly from the browser
```

- The original `index.html` loads the Supabase JavaScript SDK
- All database queries happen in the user's browser
- The Supabase URL and anon key are visible in the HTML source

### Python Version (Flask in the middle)
```
Browser ──POST /api/doubles──► Flask (Python) ──RPC──► Supabase
        ◄─── JSON results ─────               ◄────────
```

- The browser's fetch() calls the **Flask server** at `/api/doubles`
- Flask receives the search parameters, calls Supabase via the Python SDK
- Flask sends the results back to the browser as JSON
- The Supabase key lives on the **server**, never exposed to the browser

The HTML itself is now rendered by Flask's **Jinja2 template engine** — the
club list and category dropdowns are generated server-side using `{% for %}` loops,
instead of being hardcoded in JavaScript.

---

## Project Structure

```
eqx-doubles-python/
├── app.py                 # The Flask app — routes, data, entry point
├── supabase_client.py     # Creates and exports the Supabase client
├── requirements.txt       # Python dependencies (pip install -r requirements.txt)
├── .env.example           # Template for your .env file (copy → .env)
├── .env                   # Your real secrets — DO NOT commit to git!
├── README.md              # This file
└── templates/
    └── index.html         # Jinja2 HTML template (rendered by Flask)
```

### File roles explained

**`app.py`** — The heart of the app. Defines:
- The CLUBS and CATEGORIES data as Python lists of dicts
- Route `GET /` → renders index.html with clubs & categories passed in
- Route `POST /api/doubles` → receives JSON search params, calls Supabase, returns JSON

**`supabase_client.py`** — A tiny module that creates one shared Supabase client.
Reads credentials from environment variables (or `.env`), with hardcoded fallbacks
so the app works out of the box.

**`requirements.txt`** — Lists the three pip packages needed: `flask`, `supabase`,
`python-dotenv`. Run `pip install -r requirements.txt` to install them all at once.

**`.env.example`** — A safe-to-commit template showing which environment variables
the app needs. Copy it to `.env` and fill in real values.

**`templates/index.html`** — The UI. Flask's Jinja2 engine fills in the clubs list
and category dropdowns at request time using `{% for club in clubs %}` loops.
All interactive behavior (fetching results, rendering cards, transit logic) is
JavaScript running in the browser, same as the original.

---

## How to Run

```bash
# 1. Navigate into the project folder
cd ~/Developer/eqx-doubles-python

# 2. (Recommended) Create a virtual environment so packages stay isolated
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Flask development server
python app.py

# 5. Open your browser
open http://localhost:5000
```

The app works immediately without a `.env` file because `supabase_client.py`
has the Supabase credentials hardcoded as fallback defaults. To override them,
copy `.env.example` to `.env` and fill in your values.

To stop the server, press **Ctrl-C** in the terminal.

---

## What "Interpreted" Means (in more detail)

When you type `python app.py`, here's what happens step by step:

1. **The Python interpreter starts** — this is a program (`/usr/bin/python3`)
   that knows how to read and execute Python code.

2. **It opens `app.py`** — just a text file.

3. **It reads line 1**: sees `from flask import Flask, render_template, ...`
   → goes and loads the Flask library into memory right now.

4. **It reads the next lines**: sees `CLUBS = [...]`
   → creates that list in memory right now.

5. **It reads `app = Flask(__name__)`**
   → calls the Flask constructor and stores the result right now.

6. **It reads `@app.route("/")`** then `def index():`
   → registers this function as the handler for GET / right now.

7. **It reads `if __name__ == "__main__": app.run(debug=True)`**
   → starts the web server right now.

The server is now running. No compilation, no binary, no build artifacts.
Your `.py` source file **is** the program. The interpreter is always there
translating it on the fly.

**Contrast with Swift:**
```bash
# Swift needs a compile step first:
swiftc app.swift -o app     # compile (can take seconds to minutes)
./app                        # then run the binary

# Python just runs:
python app.py                # interpreter reads + executes immediately
```

---

## Virtual Environments (venv)

A virtual environment is an isolated copy of Python + packages for your project.
This prevents different projects from fighting over incompatible package versions.

```bash
python3 -m venv .venv        # create a venv in a folder called .venv
source .venv/bin/activate    # activate it (your shell prompt changes)
pip install -r requirements.txt  # packages install INTO .venv, not globally
deactivate                   # exit the venv when done
```

The `.venv` folder should be added to `.gitignore` — it's large and can always
be recreated from `requirements.txt`.

---

## Learning Resources

- [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) — the best Flask beginner guide
- [Python.org Official Tutorial](https://docs.python.org/3/tutorial/) — from the source
- [Real Python](https://realpython.com) — practical articles and tutorials
- [Jinja2 Template Docs](https://jinja.palletsprojects.com/en/3.1.x/) — all the `{% %}` / `{{ }}` syntax
