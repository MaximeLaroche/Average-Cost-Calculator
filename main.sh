# Kill opened excel sheets
filename='pid.txt'
n=1
while read line; do
# reading each line
kill $line
n=$((n+1))
done < $filename
rm $filename

# Update and install program
git pull
python -m pip install -r requirements.txt

###### Disnat
echo "Exécution de disnat"
python disnat.py
echo "Terminé l'exécution de disnat"
# Open excel sheets
"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE" DisnatOptions.xlsx & dsStk=$!
"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE" DisnatStocks.xlsx & dsOpt=$!
echo -e $dsStk >> $filename
echo -e $dsOpt >> $filename


echo "Exécution de questrade"
python questrade.py
echo "Terminé l'exécution de questrade"
"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE" QuestradeOptions.xlsx & qsStk=$!
"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE" QuestradeStocks.xlsx & qsOpt=$!
echo -e $qsStk >> $filename
echo -e $qsOpt >> $filename