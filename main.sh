# Kill opened excel sheets
filename='pid.txt'
n=1
while read line; do
# reading each line
echo "Line No. $n : $line"
kill $line
n=$((n+1))
done < $filename
rm pid.txt

# run the script
python main.py

# Open excel sheets
"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE" Option.xlsx & stk=$!
"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE" Stocks.xlsx & opt=$!
echo "pid is "
echo -e $stk >> pid.txt
echo -e $opt >> pid.txt