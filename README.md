# Docsie.io  

## Purpose of this repo is to        
   
* This is our static site. We write it wih ai. 
 
setup virtual environment if needed
pip install -r requirements.txt
sh start.sh

### To compile the site
python main.py


pybabel init -d locale -l it -i locale/messages.pot
pybabel compile -d locale -l it

