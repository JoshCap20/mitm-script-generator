#!/bin/zsh
# MacOS/Linux startup script for mitmproxy setup
set -e

VENV_DIR=".venv"
REQUIREMENTS="requirements.txt"

if [ ! -d "$VENV_DIR" ]; then
    echo "No virtual environment found. Creating one at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created. Installing requirements..."
    source "$VENV_DIR/bin/activate"
    if [ -f "$REQUIREMENTS" ]; then
        pip install --upgrade pip
        pip install -r "$REQUIREMENTS"
    else
        echo "No requirements.txt found, skipping requirements installation."
    fi
else
    echo "Virtual environment already exists at $VENV_DIR. Skipping setup."
    source "$VENV_DIR/bin/activate"
fi

echo "Virtual environment activated"

if [ -z "$MITM_OPTION" ]; then
    echo "MITM_OPTION not set, defaulting to 'Secure'"
    export MITM_OPTION="Secure"
fi
echo "Using MITM_OPTION: $MITM_OPTION"
option=$MITM_OPTION

# Comment out if you want to skip tests
echo "Running request listener script tests to ensure functionality"
pytest util/test.py

echo "Generating request listener script"
python util/make.py $option

if ! command -v mitmproxy >/dev/null 2>&1; then
    echo "mitmproxy is not installed in the current environment. Please install it."
    exit 1
fi

echo "Running mitmproxy with blocker script"
mitmdump -s mitm_script.py --quiet