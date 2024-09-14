from expenses import Expense
import calendar
import datetime


def main():
    print(f"running")
    expense_file_path = "expenses.csv"
    budget = 5000
    
    # Get user input for expense.
    expense = get_user_expense()
    
    # Write expense to a file.
    save_expense_to_file(expense, expense_file_path)
    
    # Read file and summarize expenses.
    summarize_expenses(expense_file_path, budget)

def get_user_expense():
    print(f"getting user expense")
    expense_name = input("enter expense name: ")
    expense_amount = float(input("enter expense amount: "))
    
    expense_categories = ["food", "Home & Bills", "Work",
                          "Fun", "travel", "others"]
    
    while True:
        print("select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f" {i+1}. {category_name}" )
            
        value_range = (f"(1 - {len(expense_categories)})")
        selected_index = int(input(f"enter a category number {value_range}: ")) - 1
        
        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)
            return new_expense
        else:
            print("Invalid category, Try again please !")
            
        
def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"saving user expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")
    
def summarize_expenses(expense_file_path, budget):
    print(f"summarizing user expenses")
    expenses: list[Expense] = []
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expense = Expense(
                name=expense_name,
                amount=float(expense_amount),
                category=expense_category,
            )
            expenses.append(line_expense)
        
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount
    
    print("Expenses by Category: ")        
    for key, amount in amount_by_category.items():
        print(f" {key}: ${amount:.2f}")
        
    total_spent = sum([x.amount for x in expenses])
    print(f"Total spent ${total_spent:.2f} this month!")   
    
    remaining_budget =  budget - total_spent
    print(f"budget remaining ${remaining_budget:.2f}") 
    
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    reamining_days = days_in_month - now.day
    print("remaining days in the current month:", reamining_days)
    
    daily_budget = remaining_budget / reamining_days
    print(f"Budget Per Day: ${daily_budget:.2f}")
    
       
    
if __name__ == "__main__":
    main()