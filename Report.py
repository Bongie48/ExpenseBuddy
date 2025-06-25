import csv
from collections import defaultdict

def Report():
    TotalCost = 0.0
    MonthlyCost = defaultdict(float)  # Dictionary to hold monthly costs
    YearlyCost = defaultdict(float)    # Dictionary to hold yearly costs
    
    print("Expense Report\n================\n")
    
    # Open the CSV file
    with open('ExpenseRecord.csv', mode='r', newline='') as file:
        _reader = csv.reader(file)
        next(_reader)  # Skip header if there is one
        for record in _reader:
            # Assuming the record format is [Date, Amount]
            date = record[0]
            amount = float(record[1])
            TotalCost += amount
            
            # Split date (assuming it's in 'YYYY-MM-DD' format)
            year, month, day = map(int, date.split('/'))
            MonthlyCost[(year, month)] += amount
            YearlyCost[year] += amount
            
    print("===============================================================================\n")
    
    print("Monthly Costs Per Year:")
    for (year, month), cost in MonthlyCost.items():
        print(f"{year}-{month:02}: R {cost:.2f}")
    
    print("\nYearly Costs:")
    for year, cost in YearlyCost.items():
        print(f"{year}: R {cost:.2f}")
    
    print("\nOverall Cost:\t\tR {total:.2f}".format(total=TotalCost))
        