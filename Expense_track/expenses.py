import datetime
import calendar
import os
import pandas as pd
import matplotlib.pyplot as plt

class Expense:
    def __init__(self, name, amt, cat):
        self.name = name
        self.amount = amt
        self.category = cat

    def __repr__(self):
        return f"{self.name},{self.amount:.2f},{self.category}"

def check_Expense():
    print('💸 Enter new expense:')
    expense_name = input('Where did you spend money? ➜ ')
    expense_amount = float(input('How much did you spend? (Rs) ➜ '))
    categories = ['Food', 'Travel', 'Shopping', 'Work', 'Misc', 'Fun']

    print('\nSelect a category:')
    for i, cat in enumerate(categories):
        print(f'{i+1}. {cat}')

    while True:
        try:
            cat_index = int(input(f'Select category [1-{len(categories)}]: ')) - 1
            if 0 <= cat_index < len(categories):
                selected_category = categories[cat_index]
                today = datetime.date.today()
                return Expense(expense_name, expense_amount, selected_category), today
            else:
                print("❌ Invalid index. Try again.")
        except ValueError:
            print("❌ Please enter a valid number.")

def save_expense(expense_obj, date, filepath="expense.csv"):
    new_row = f"{expense_obj.name},{expense_obj.amount},{expense_obj.category},{date}\n"
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(new_row)
    print("✅ Expense saved!")

def summarize_expenses(filepath="expense.csv", budget=600000):
    if not os.path.exists(filepath):
        print("⚠️ No expenses recorded yet.")
        return

    print("\n📊 SIMPLE EXPENSE SUMMARY:\n")

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total_spent = 0
    for line in lines:
        try:
            name, amount, category, date = line.strip().split(',')
            amount = float(amount)
            total_spent += amount
            print(f"🧾 {name} → Rs. {amount:.2f}")
        except ValueError:
            continue

    print("\n💰 Total Spent:", f"Rs. {total_spent:.2f}")
    print("🎯 Budget:", f"Rs. {budget:.2f}")
    remaining = budget - total_spent
    print("💼 Remaining:", f"Rs. {remaining:.2f}")

    # Budget Alert
    spend_ratio = total_spent / budget
    if spend_ratio > 0.9:
        print("🚨 ALERT: You’ve crossed 90% of your budget!")
    elif spend_ratio > 0.8:
        print("⚠️ Warning: You’ve used over 80% of your budget.")
    elif spend_ratio > 0.5:
        print("🔔 Notice: You’ve spent more than 50% of your budget.")

def filter_expenses(filepath="expense.csv"):
    if not os.path.exists(filepath):
        print("⚠️ No data found.")
        return

    df = pd.read_csv(filepath, names=["Name", "Amount", "Category", "Date"])

    print("\n📋 Filter Options:")
    print("1. View by Category")
    print("2. View by Date")
    choice = input("Select option: ")

    if choice == '1':
        cat = input("Enter category (e.g. Food, Travel): ").capitalize()
        filtered = df[df["Category"] == cat]
    elif choice == '2':
        date = input("Enter date (YYYY-MM-DD): ")
        filtered = df[df["Date"] == date]
    else:
        print("❌ Invalid input.")
        return

    if filtered.empty:
        print("😕 No matching records found.")
    else:
        print("\n📄 Matching Expenses:")
        print(filtered.to_string(index=False))

def show_chart(filepath="expense.csv"):
    if not os.path.exists(filepath):
        print("⚠️ No data found.")
        return

    df = pd.read_csv(filepath, names=["Name", "Amount", "Category", "Date"])
    summary = df.groupby("Category")["Amount"].sum()

    if summary.empty:
        print("😕 No expenses to chart.")
        return

    plt.figure(figsize=(6,6))
    plt.pie(summary, labels=summary.index, autopct="%1.1f%%", startangle=140)
    plt.title("Category-wise Expense Distribution")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()

def delete_expense(filepath="expense.csv"):
    if not os.path.exists(filepath):
        print("⚠️ No data found.")
        return

    name = input("Enter the expense name to delete: ")
    amt = input("Enter the amount: ")

    with open(filepath, "r", encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    deleted = False

    for line in lines:
        if f"{name},{amt}" in line:
            deleted = True
            continue
        new_lines.append(line)

    if deleted:
        with open(filepath, "w", encoding='utf-8') as f:
            f.writelines(new_lines)
        print("✅ Expense deleted.")
    else:
        print("❌ No matching expense found.")

def menu():
    budget = 600000
    filepath = "expense.csv"

    while True:
        print("\n📌 MENU:")
        print("1. ➕ Add Expense")
        print("2. 📈 View Summary")
        print("3. 📋 View by Category/Date")
        print("4. 📊 Show Chart")
        print("5. ❌ Delete Expense")
        print("6. 🔚 Exit")

        choice = input("Enter choice (1-6): ")

        if choice == '1':
            exp, dt = check_Expense()
            save_expense(exp, dt, filepath)
        elif choice == '2':
            summarize_expenses(filepath, budget)
        elif choice == '3':
            filter_expenses(filepath)
        elif choice == '4':
            show_chart(filepath)
        elif choice == '5':
            delete_expense(filepath)
        elif choice == '6':
            print("👋 Exiting. Good luck with your budget!")
            break
        else:
            print("❌ Invalid input. Please select between 1 to 6.")

menu()
