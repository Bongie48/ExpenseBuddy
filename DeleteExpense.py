import csv
def DeleteExpense():
    print("\nNote: The record you want to delete must have a matching category and date!")
    RowsToKeep=[]
    DeleteCategory=input("Enter Category To Delete: ")
    DeleteDate=input("Enter Date Of Category To Delete: ")
    with open('ExpenseRecord.csv', mode='r', newline='') as file:
        csv_reader=csv.reader(file)
        for rows in csv_reader:
            if(rows[0]==DeleteCategory and rows[2]==DeleteDate):
                continue
            RowsToKeep.append(rows)

    with open ('ExpenseRecord.csv', mode='w', newline='') as file:
        csv_writer=csv_writer(file)
        csv_writer.writerow(RowsToKeep)


