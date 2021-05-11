Dictionary App

Installation 
# create application directory
mkdir dictionary-app
cd dictionary-app

# Download app from github
git clone https://github.com/emrecirakoglu/dictionary_app_flask.git

# Create python virtual environment
python3 -m venv dictionary-app-venv
source dictionary-app-venv/bin/activate

# Install all dependencies
pip install requirements.txt

# Run application
python run.py