# Update and install program
git pull
python -m pip install -r requirements.txt

###### Disnat
echo "Exécution de disnat"
python disnat.py
echo "Terminé l'exécution de disnat"


##### Questrade
echo "Exécution de questrade"
python questrade.py
echo "Terminé l'exécution de questrade"
