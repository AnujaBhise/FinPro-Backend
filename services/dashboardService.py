# services/dashboardService.py

from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

from models.incomeModel import Income
from models.expenseModel import Expense

from schemas.commonSchema import ApiResponse


# =========================================================
# Generate Chart Data
# =========================================================
def generate_chart_data(expenses, incomes):

    monthly_data = {}

    month_names = [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ]

    # Process incomes
    for income in incomes:

        date = income.date

        month_key = month_names[date.month - 1]

        year = date.year

        key = f"{year}-{month_key}"

        if key not in monthly_data:

            monthly_data[key] = {
                "income": 0,
                "expense": 0,
                "balance": 0
            }

        monthly_data[key]["income"] += float(income.amount or 0)

    # Process expenses
    for expense in expenses:

        date = expense.date

        month_key = month_names[date.month - 1]

        year = date.year

        key = f"{year}-{month_key}"

        if key not in monthly_data:

            monthly_data[key] = {
                "income": 0,
                "expense": 0,
                "balance": 0
            }

        monthly_data[key]["expense"] += float(expense.amount or 0)

    # Calculate balance
    for key in monthly_data:

        monthly_data[key]["balance"] = (
            monthly_data[key]["income"] -
            monthly_data[key]["expense"]
        )

    # Last 4 months
    sorted_keys = sorted(monthly_data.keys())[-4:]

    chart_data = []

    for key in sorted_keys:

        year, month = key.split("-")

        chart_data.append({
            "month": month,
            "income": monthly_data[key]["income"],
            "expense": monthly_data[key]["expense"],
            "balance": monthly_data[key]["balance"]
        })

    return chart_data


# =========================================================
# Generate Insights
# =========================================================
def generate_insights(
    monthly_income,
    monthly_expense,
    savings,
    savings_rate,
    spend_by_category
):

    insights = []

    # Highest expense category
    highest_category = ("Other", 0)

    for category, amount in spend_by_category.items():

        if amount > highest_category[1]:

            highest_category = (category, amount)

    if highest_category[1] > 0:

        percentage = round(
            (highest_category[1] / monthly_expense) * 100
        )

        insights.append({
            "type": "spending_insight",
            "category": highest_category[0],
            "percentage": percentage,
            "amount": highest_category[1]
        })

    # Savings insight
    savings_percentage = (
        0
        if monthly_income == 0
        else round((savings / monthly_income) * 100)
    )

    insights.append({
        "type": "savings_trend",
        "savingsPercentage": savings_percentage,
        "savingsAmount": savings,
        "incomeAmount": monthly_income
    })

    # Goal tracking
    target_savings_rate = 25

    insights.append({
        "type": "monthly_goal",
        "currentRate": savings_rate,
        "targetRate": target_savings_rate,
        "difference": savings_rate - target_savings_rate,
        "onTrack": savings_rate >= target_savings_rate
    })

    return insights


# =========================================================
# Dashboard Overview
# =========================================================
def get_dashboard_overview(
    db: Session,
    user_id: int
):

    try:

        now = datetime.now()

        start_of_year = datetime(
            now.year,
            1,
            1
        )

        # Get incomes
        incomes = (
            db.query(Income)
            .filter(
                Income.user_id == user_id,
                Income.date >= start_of_year,
                Income.date <= now
            )
            .all()
        )

        # Get expenses
        expenses = (
            db.query(Expense)
            .filter(
                Expense.user_id == user_id,
                Expense.date >= start_of_year,
                Expense.date <= now
            )
            .all()
        )

        # Total income
        monthly_income = sum(
            float(income.amount or 0)
            for income in incomes
        )

        # Total expense
        monthly_expense = sum(
            float(expense.amount or 0)
            for expense in expenses
        )

        # Savings
        savings = monthly_income - monthly_expense

        # Savings rate
        savings_rate = (
            0
            if monthly_income == 0
            else round((savings / monthly_income) * 100)
        )

        # Recent transactions
        recent_transactions = []

        for income in incomes:

            recent_transactions.append({
                "id": income.id,
                "description": income.description,
                "amount": income.amount,
                "category": income.category,
                "date": str(income.date),
                "type": "income"
            })

        for expense in expenses:

            recent_transactions.append({
                "id": expense.id,
                "description": expense.description,
                "amount": expense.amount,
                "category": expense.category,
                "date": str(expense.date),
                "type": "expense"
            })

        recent_transactions = sorted(
            recent_transactions,
            key=lambda x: x["date"],
            reverse=True
        )

        # Expense by category
        spend_by_category = {}

        for expense in expenses:

            category = expense.category or "Other"

            spend_by_category[category] = (
                spend_by_category.get(category, 0) +
                float(expense.amount or 0)
            )

        # Expense distribution
        expense_distribution = []

        for category, amount in spend_by_category.items():

            expense_distribution.append({
                "category": category,
                "amount": amount,
                "percent": (
                    0
                    if monthly_expense == 0
                    else round((amount / monthly_expense) * 100)
                )
            })

        # Insights
        insights = generate_insights(
            monthly_income,
            monthly_expense,
            savings,
            savings_rate,
            spend_by_category
        )

        # Chart data
        chart_data = generate_chart_data(
            expenses,
            incomes
        )

        return ApiResponse(
            success=True,
            message="Dashboard fetched successfully",
            data={
                "monthlyIncome": monthly_income,
                "monthlyExpense": monthly_expense,
                "savings": savings,
                "savingsRate": savings_rate,
                "recentTransactions": recent_transactions,
                "expenseDistribution": expense_distribution,
                "insights": insights,
                "chartData": chart_data
            }
        )

    except Exception as error:

        print("Dashboard Error:", error)

        return ApiResponse(
            success=False,
            message="Dashboard fetch failed"
        )