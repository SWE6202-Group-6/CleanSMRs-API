# CleanSMRs-API

This is the code repository for the CleanSMRs API project.

## Setup

First, clone the repository, either through the GitHub client or the Git CLI:

```
git clone https://github.com/SWE6202-Group-6/CleanSMRs-API.git
```

Navigate into the directory and create your virtual environment:

```
cd CleanSMRs-API
python -m venv .venv
```

Prefer one of `env`, `venv` or `.venv` for your virtual environment name as these are already added to the `.gitignore` 
file. If you choose another name, please make sure to add it to a line in `.gitignore` to ensure it is not committed to 
the repository - they can be quite large on disk.

Activate the virtual environment.

Windows:

```
source .venv/Scripts/activate
```

Mac/Linux:

```
source .venv/bin/activate
```

To install required packages for the first time, execute the following:

```
python -m pip install -r requirements.txt
```

Whenever you add a new dependency with Pip, make sure it also gets added to the `requirements.txt` file:

```
python -m pip freeze > requirements.txt
```

For any application settings, you'll need to make a copy of `.env.example` as `.env` and add things such as database 
details, any secrets etc. to it:

```
cp .env.example .env
```

## Contributing

Visual Studio Code is the recommended editor. The following extensions are useful:

- autoDocstring (njpwerner.autodocstring)
- Black Formatter (ms-python.black-formatter)
- isort (ms-python.isort)
- Python (ms-python.python)
- Python Test Explorer for Visual Studio Code (littlefoxteam.vscode-python-test-adapter)

The following are the recommended settings to add to your user settings file in VS Code to configure the extension 
behaviour. You can access this by pressing Ctrl+Shift+P and typing 'settings', then selecting 'Preferences: Open User 
Settings (JSON)'.

```
"[python]":{
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.rulers": [80],
    "editor.codeActionsOnSave": {
        "source.organizeImports": "explicit",
    },
    "notebook.codeActionsOnSave": {
        "notebook.source.fixAll": "explicit"
    }
},
"black-formatter.args": ["--line-length", "80"],
"isort.args":["--profile", "black"],
"autoDocstring.docstringFormat": "google"
```

This will set up your editor to format your Python code according to the PEP8 guidelines every time you save the file,
as well as organising your imports. For docstrings, typing `"""` and hitting tab will expand it into a Google-style
docstring that you can then populate with details for the module/class/method.
