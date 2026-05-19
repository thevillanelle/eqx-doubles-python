# =============================================================================
# supabase_client.py
# =============================================================================
#
# WHAT IS A MODULE?
# -----------------
# In Python, any .py file is called a "module." A module is just a reusable
# chunk of code you can share between files. Instead of copy-pasting the same
# code everywhere, you write it once in its own file and then `import` it
# wherever you need it.
#
# This module has one job: create a Supabase client and make it available
# to the rest of the app. Other files will do:
#
#     from supabase_client import supabase
#
# ...and they instantly have access to the client this file sets up.
#
# WHAT IS `import`?
# -----------------
# `import` tells Python: "go find this library/module and load it so I can
# use the things inside it." Python looks in:
#   1. The current directory (your project folder)
#   2. Built-in standard library modules (like `os`, `json`)
#   3. Third-party packages installed via `pip` (like `flask`, `supabase`)
#
# WHAT ARE ENVIRONMENT VARIABLES?
# --------------------------------
# Environment variables are key=value pairs that live *outside* your code,
# in the operating system's environment. They're used to store secrets
# (like API keys and passwords) so you never have to hardcode them in code
# that might get committed to GitHub.
#
# On macOS/Linux you can set one like this in the terminal:
#   export SUPABASE_URL="https://..."
#
# python-dotenv lets you put those same key=value pairs in a file called
# .env in your project folder, and it loads them automatically at startup.
# The .env file itself should NEVER be committed to git (add it to .gitignore).
#
# =============================================================================

# `os` is a built-in Python module (no install needed) that lets you talk
# to the operating system — read files, access environment variables, etc.
import os

# `dotenv` is a third-party library (installed via `pip install python-dotenv`).
# `load_dotenv()` reads the .env file in your project folder and stuffs each
# KEY=VALUE line into the process's environment variables so `os.getenv()`
# can find them.
from dotenv import load_dotenv

# `create_client` is a function from the `supabase` library. It takes a URL
# and an API key and returns a Supabase client object — a Python object with
# methods like .table(), .rpc(), .auth, etc.
from supabase import create_client, Client

# ---------------------------------------------------------------------------
# Load the .env file (if it exists). If there's no .env file, that's fine —
# load_dotenv() simply does nothing and we fall back to the hardcoded defaults
# below. This means the app works out of the box without any setup.
# ---------------------------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------------------------
# WHAT IS os.getenv()?
# ---------------------
# os.getenv("KEY", "default") reads an environment variable called KEY.
# If KEY isn't set in the environment (or .env file), it returns "default".
# The second argument is the fallback — here we hardcode the real Supabase
# credentials so the app works immediately, even without a .env file.
#
# In production you'd remove the hardcoded fallbacks and rely entirely on
# environment variables, so the secrets aren't in your source code.
# ---------------------------------------------------------------------------

# The URL of your Supabase project. Looks like https://<project-ref>.supabase.co
SUPABASE_URL: str = os.getenv(
    "SUPABASE_URL",
    "https://hprkoonlydcjqxrgjwtr.supabase.co"  # fallback default
)

# The "anon" (anonymous/public) key for your Supabase project.
# This key is safe to use in client-side code — Row Level Security policies
# on the database control what it can actually access.
SUPABASE_KEY: str = os.getenv(
    "SUPABASE_KEY",
    "sb_publishable_qHE_ZAyuekcsSDMpmK3a1w_fkWuo57M"  # fallback default
)

# ---------------------------------------------------------------------------
# Create the Supabase client.
#
# WHAT IS A VARIABLE?
# --------------------
# A variable is a name that points to a value stored in memory. Here `supabase`
# is a variable that holds the client object returned by create_client().
# The `: Client` part is a *type hint* — it's optional documentation telling
# other programmers (and tools like editors) what type of thing this variable
# holds. Python doesn't enforce type hints at runtime; they're just helpful notes.
# ---------------------------------------------------------------------------
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# That's it! Any other file in this project can now do:
#
#     from supabase_client import supabase
#
# ...and use `supabase.rpc(...)`, `supabase.table(...)`, etc.
