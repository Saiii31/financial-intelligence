import json
import csv
import sys
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import (
    Transaction,
    Asset,
    Liability,
    FinancialMetric,
    MonthlyTrend,
    Recommendation
)

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def load_financial_metrics(db: Session, summary: dict):
    """
    Load financial metrics from Person 1's summary into the database.
    """
    metric = FinancialMetric(
        income=summary["summary"]["income"],
        expenses=summary["summary"]["expenses"],
        savings=summary["summary"]["savings"],
        savings_rate=summary["summary"]["savings_rate"],
        total_assets=summary["summary"]["assets"],
        total_liabilities=summary["summary"]["liabilities"],
        net_worth=summary["summary"]["net_worth"],
        monthly_emi=summary["summary"]["monthly_emi"],
        debt_to_income=summary["summary"]["debt_to_income"] * 100,  # Convert to percentage
        health_score=summary["health_score_breakdown"]["overall_health_score"]
    )
    db.add(metric)
    db.commit()
    print(f"[OK] Loaded financial metrics")

def load_monthly_trends(db: Session, summary: dict):
    """
    Load monthly trends from Person 1's summary.
    We'll calculate actual monthly income/expenses from transactions data.
    """
    import pandas as pd
    
    # Load transactions from CSV to get actual monthly income/expenses
    try:
        transactions_df = pd.read_csv('data/transactions_clean.csv')
        
        # Convert date column
        transactions_df['date'] = pd.to_datetime(transactions_df['date'], errors='coerce')
        transactions_df = transactions_df[transactions_df['date'].notna()].copy()
        transactions_df['month'] = transactions_df['date'].dt.to_period('M').astype(str)
        
        # Calculate monthly income and expenses
        monthly_data = {}
        for month in transactions_df['month'].unique():
            month_df = transactions_df[transactions_df['month'] == month]
            income = float(month_df[month_df['type'].str.lower() == 'income']['amount'].sum())
            expenses = float(month_df[month_df['type'].str.lower() == 'expense']['amount'].sum())
            monthly_data[month] = {
                "income": income,
                "expenses": expenses,
                "savings": income - expenses
            }
        
        # Insert into database
        for month, data in sorted(monthly_data.items()):
            trend = MonthlyTrend(
                month=month,
                income=data["income"],
                expenses=data["expenses"],
                savings=data["savings"]
            )
            db.add(trend)
        
        db.commit()
        print(f"[OK] Loaded {len(monthly_data)} monthly trends from actual transaction data")
    except Exception as e:
        print(f"[WARNING] Could not load monthly trends from transactions: {e}")
        print(f"[INFO] Falling back to aggregated spending data...")
        
        # Fallback to original method
        monthly_spending = summary["spending_analysis"]["monthly_category_spending"]
        
        # Aggregate by month
        monthly_data = {}
        for item in monthly_spending:
            month = item["month"]
            if month not in monthly_data:
                monthly_data[month] = {"income": 0, "expenses": 0, "savings": 0}
            monthly_data[month]["expenses"] += item["spending"]
        
        # Estimate income and savings
        for month, data in monthly_data.items():
            avg_monthly_income = summary["summary"]["income"] / len(monthly_data)
            data["income"] = avg_monthly_income
            data["savings"] = data["income"] - data["expenses"]
        
        # Insert into database
        for month, data in sorted(monthly_data.items()):
            trend = MonthlyTrend(
                month=month,
                income=data["income"],
                expenses=data["expenses"],
                savings=data["savings"]
            )
            db.add(trend)
        
        db.commit()
        print(f"[OK] Loaded {len(monthly_data)} monthly trends (estimated)")

def load_recommendations(db: Session, summary: dict):
    """
    Load recommendations from Person 1's summary.
    """
    recommendations = summary["recommendations"]
    
    for i, rec in enumerate(recommendations):
        priority = "HIGH" if i == 0 else "MEDIUM" if i == 1 else "LOW"
        category = "General"
        
        # Try to categorize based on content
        if "savings" in rec.lower():
            category = "Savings"
        elif "debt" in rec.lower():
            category = "Debt"
        elif "spending" in rec.lower():
            category = "Spending"
        
        recommendation = Recommendation(
            recommendation=rec,
            priority=priority,
            category=category
        )
        db.add(recommendation)
    
    db.commit()
    print(f"[OK] Loaded {len(recommendations)} recommendations")

def load_transactions_from_csv(db: Session, csv_path: str):
    """
    Load transactions from Person 1's cleaned CSV file.
    Skip transactions marked as duplicates.
    """
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        skipped = 0
        for row in reader:
            # Skip duplicate transactions
            if row.get('is_duplicate', 'False').lower() == 'true':
                skipped += 1
                continue
            
            transaction = Transaction(
                txn_id=row.get('txn_id', f"TXN_{count}"),
                date=datetime.strptime(row['date'], '%Y-%m-%d').date() if row.get('date') else None,
                category=row.get('category_clean', row.get('category', 'Uncategorized')),
                description=row.get('description', ''),
                amount=float(row.get('amount', 0)),
                type=row.get('type', 'expense'),
                is_duplicate=row.get('is_duplicate', 'False').lower() == 'true',
                is_anomaly=row.get('is_anomaly', 'False').lower() == 'true'
            )
            db.add(transaction)
            count += 1
    
    db.commit()
    print(f"[OK] Loaded {count} transactions (skipped {skipped} duplicates)")

def load_assets_from_csv(db: Session, csv_path: str):
    """
    Load assets from Person 1's cleaned CSV file.
    """
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            asset = Asset(
                asset_id=row.get('asset_id', f"ASSET_{count}"),
                type=row.get('type', 'Other'),
                value=float(row.get('value', 0)),
                as_of_date=datetime.strptime(row['as_of_date'], '%Y-%m-%d').date() if row.get('as_of_date') else datetime.now().date()
            )
            db.add(asset)
            count += 1
    
    db.commit()
    print(f"[OK] Loaded {count} assets")

def load_liabilities_from_csv(db: Session, csv_path: str):
    """
    Load liabilities from Person 1's cleaned CSV file.
    """
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            liability = Liability(
                liability_id=row.get('liability_id', f"LIAB_{count}"),
                type=row.get('type', 'Other'),
                outstanding=float(row.get('outstanding', 0)),
                interest_rate=float(row.get('interest_rate', 0)),
                emi=float(row.get('emi', 0)),
                due_date=datetime.strptime(row['due_date'], '%Y-%m-%d').date() if row.get('due_date') else None
            )
            db.add(liability)
            count += 1
    
    db.commit()
    print(f"[OK] Loaded {count} liabilities")

def main():
    """
    Main function to load all Person 1 data into the database.
    """
    print("Starting data load from Person 1's analytics...")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Clear existing data first
        print("\nClearing existing data...")
        db.query(Transaction).delete()
        db.query(Asset).delete()
        db.query(Liability).delete()
        db.query(FinancialMetric).delete()
        db.query(MonthlyTrend).delete()
        db.query(Recommendation).delete()
        db.commit()
        print("[OK] Cleared existing data")
        
        # Load financial summary JSON
        with open('data/financial_summary.json', 'r', encoding='utf-8') as f:
            summary = json.load(f)
        
        print("\nLoading data into MySQL database...")
        
        # Load financial metrics
        load_financial_metrics(db, summary)
        
        # Load monthly trends
        load_monthly_trends(db, summary)
        
        # Load recommendations
        load_recommendations(db, summary)
        
        # Load transactions from CSV
        load_transactions_from_csv(db, 'data/transactions_clean.csv')
        
        # Load assets from CSV
        load_assets_from_csv(db, 'data/assets_clean.csv')
        
        # Load liabilities from CSV
        load_liabilities_from_csv(db, 'data/liabilities_clean.csv')
        
        print("\n[SUCCESS] All data loaded successfully!")
        print("\nDatabase now contains:")
        print(f"- Financial metrics")
        print(f"- Monthly trends")
        print(f"- Recommendations")
        print(f"- Transactions")
        print(f"- Assets")
        print(f"- Liabilities")

    except Exception as e:
        print(f"\n[ERROR] Error loading data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
