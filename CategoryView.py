import csv
def ViewByCategory():
    CategoryList=[]
    print("Total Price Per Category")
    print("=========================\n")
    with open('ExpenseRecord.csv', mode='r', newline='') as file:
        reader=csv.reader(file)
        for row in reader:
            CurrentCategory=row[0]
            PricePerCategory=0.0
            if(CurrentCategory not in CategoryList):
                for record in reader:
                    if record[0]==CurrentCategory:
                        PricePerCategory= record[1]
                CategoryList.append([CurrentCategory,PricePerCategory])
    for category in CategoryList:
        print(category[0]+"\t"+category[1])
