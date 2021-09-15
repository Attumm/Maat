rm -rf venv
python3 -m venv venv
venv/bin/pip install --upgrade pip
venv/bin/pip install --upgrade wheel 
venv/bin/pip install -r requirements.txt

export SAVE=1

venv/bin/python run.py
