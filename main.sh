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
python main.py

# Open excel sheets
"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE" Option.xlsx & stk=$!
"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE" Stocks.xlsx & opt=$!
echo -e $stk >> $filename
echo -e $opt >> $filename