# Kill opened excel sheets
filename='pid.txt'
n=1
while read line; do
# reading each line
kill $line
n=$((n+1))
done < $filename
rm $filename

# run the script
python -m pip install pandas==1.4.2
python -m pip install openpyxl==3.0.9
python -m pip install yfinance==0.1.70
python main.py

# Open excel sheets
"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE" Option.xlsx & stk=$!
"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE" Stocks.xlsx & opt=$!
echo -e $stk >> $filename
echo -e $opt >> $filename