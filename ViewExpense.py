import csv
def Viewing():
    print("Added Expense Record This Year")
    print("================================")
    with open('ExpenseRecord.csv', mode='r', newline='') as file:
        csv_reader=csv.reader(file)
        for row in csv_reader:
            print(row)