#!/usr/bin/env python3
"""
Nirixa OS Engine - Personal Financial Advisor Agent (Empirical & Stress-Free)
Models the 3-Bucket Wealth Architecture tailored to Monish's real-world cashflow:
- Salary Inflow: ₹67,000 (around 3rd of every month)
- Sustainable Savings Target: ₹10,000 / month (ad-hoc surplus review)
- Live GROWW Holdings:
  * Motilal Oswal Midcap Fund: ₹29,999 invested (Dec 11, 2024) -> Currently ₹27,452
  * ICICI Prudential Nifty 50 Index: ₹19,999 invested (Dec 11, 2024) -> Currently ₹20,291
- Priority Directive: 100% to Bucket 1 (The Armor Shield) to eliminate market anxiety.
"""

import os
import sys
import json
import sqlite3

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.insert(0, script_dir)

import db

def get_financial_baseline(workspace_root=workspace_root):
    """
    Retrieves Monish's baseline financial profile and live GROWW portfolio.
    """
    profile = db.get_user_profile(workspace_root=workspace_root)
    
    salary = profile.get("monthly_salary", 67000)
    rent = profile.get("monthly_rent", 15000)
    parents = profile.get("monthly_parents", 10000)
    living = profile.get("monthly_living_estimate", 17000) # realistic living buffer
    sustainable_savings = 10000 # realistic monthly target
    current_armor = profile.get("liquid_armor_balance", 20000)
    
    total_fixed_expenses = rent + parents + living
    unallocated_buffer = max(0, salary - total_fixed_expenses - sustainable_savings) # ~₹25,000 discretionary/contingency buffer
    
    # Armor Target: 3.5 months of basic fixed living expenses (~₹1,40,000)
    target_armor = total_fixed_expenses * 3.5
    
    # Monish's actual GROWW Portfolio holdings
    groww_portfolio = [
        {
            "fund_name": "Motilal Oswal Midcap Fund Direct Growth",
            "invested_date": "2024-12-11",
            "invested_amount": 29999,
            "current_value": 27452,
            "pnl": -2547,
            "pnl_pct": -8.5,
            "category": "Midcap Equity (High Volatility)"
        },
        {
            "fund_name": "ICICI Prudential Nifty 50 Index Direct Plan Growth",
            "invested_date": "2024-12-11",
            "invested_amount": 19999,
            "current_value": 20291,
            "pnl": 292,
            "pnl_pct": 1.5,
            "category": "Large Cap Index (Stable Foundation)"
        }
    ]
    
    total_mf_invested = sum(f["invested_amount"] for f in groww_portfolio) # ₹49,998
    total_mf_current = sum(f["current_value"] for f in groww_portfolio)   # ₹47,743
    
    return {
        "monthly_salary": salary,
        "salary_day": 3,
        "monthly_rent": rent,
        "monthly_parents": parents,
        "monthly_living_estimate": living,
        "sustainable_monthly_savings": sustainable_savings,
        "total_fixed_expenses": total_fixed_expenses,
        "contingency_buffer": unallocated_buffer,
        "current_armor_balance": current_armor,
        "target_armor_balance": target_armor,
        "armor_completion_percentage": min(100.0, round((current_armor / target_armor) * 100, 1)),
        "months_to_full_armor": round(max(0, target_armor - current_armor) / sustainable_savings, 1),
        "groww_portfolio": {
            "holdings": groww_portfolio,
            "total_invested": total_mf_invested,
            "total_current": total_mf_current,
            "net_pnl": round(total_mf_current - total_mf_invested, 2),
            "net_pnl_pct": round(((total_mf_current - total_mf_invested) / total_mf_invested) * 100, 2)
        }
    }

def simulate_wealth_compounding(monthly_sip=10000, years=10, annual_cagr=0.13):
    """
    Simulates stress-free 10-year compounding at ₹10,000/month.
    """
    monthly_rate = annual_cagr / 12
    total_months = years * 12
    total_invested = monthly_sip * total_months
    current_portfolio = 0.0
    timeline = []
    
    for month in range(1, total_months + 1):
        current_portfolio = (current_portfolio + monthly_sip) * (1 + monthly_rate)
        if month % 12 == 0:
            yr = month // 12
            timeline.append({
                "year": yr,
                "invested": monthly_sip * month,
                "portfolio_value": round(current_portfolio, 2),
                "wealth_gain": round(current_portfolio - (monthly_sip * month), 2)
            })
            
    return {
        "monthly_sip": monthly_sip,
        "years": years,
        "annual_cagr_percentage": round(annual_cagr * 100, 1),
        "total_invested": total_invested,
        "projected_portfolio_value": round(current_portfolio, 2),
        "total_gain": round(current_portfolio - total_invested, 2),
        "gain_multiplier": round(current_portfolio / total_invested, 2) if total_invested > 0 else 1.0,
        "annual_milestones": timeline
    }

def generate_wealth_advisory_summary(workspace_root=workspace_root):
    """
    Compiles an authentic, stress-free financial briefing for Monish.
    """
    baseline = get_financial_baseline(workspace_root=workspace_root)
    compounding_10yr = simulate_wealth_compounding(monthly_sip=baseline["sustainable_monthly_savings"], years=10)
    
    return {
        "status": "success",
        "baseline": baseline,
        "core_recommendation": (
            "1. Salary Day Routine (3rd of every month): Review bank balance and allocate a relaxed ₹10,000 (or ad-hoc) to Bucket 1 (The Armor Buffer). "
            "2. Stop Worrying About Market Fluctuations: The reason your GROWW midcaps caused anxiety is because money was invested without a liquid armor buffer. "
            "3. Lock in ₹1.4L in liquid savings first. Once the armor is secure, index investing is 100% stress-free."
        ),
        "compounding_projection_10yr": compounding_10yr
    }

if __name__ == "__main__":
    summary = generate_wealth_advisory_summary()
    print(json.dumps(summary, indent=2))
