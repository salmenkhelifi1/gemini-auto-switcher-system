#!/usr/bin/env python3
import json
import time
import subprocess
import os
from pathlib import Path
import requests

# Configuration
COCKPIT_DIR = Path.home() / ".antigravity_cockpit"
GEMINI_DIR = Path.home() / ".gemini"
ACCOUNTS_DIR = COCKPIT_DIR / "gemini_accounts"
THRESHOLD = 10  # Switch if quota < 10%
CHECK_INTERVAL = 60  # Check every 1 minute
TARGET_PROJECT = "rosy-odyssey-86f3p"

def get_active_email():
    ga_path = GEMINI_DIR / "google_accounts.json"
    if not ga_path.exists():
        return None
    try:
        data = json.loads(ga_path.read_text())
        return data.get("active")
    except:
        return None

def get_account_by_email(email):
    index_path = COCKPIT_DIR / "gemini_accounts.json"
    if not index_path.exists():
        return None
    try:
        data = json.loads(index_path.read_text())
        for acc in data.get("accounts", []):
            if acc.get("email") == email:
                return acc
        return None
    except:
        return None

def get_quota_percentage(account_id):
    acc_file = ACCOUNTS_DIR / f"{account_id}.json"
    if not acc_file.exists():
        return 100
    try:
        data = json.loads(acc_file.read_text())
        usage = data.get("gemini_usage_raw", {})
        buckets = usage.get("buckets", [])
        if not buckets:
            return 100
        # Return the lowest remaining fraction for Gemini 3/3.1 models
        min_fraction = 1.0
        found_model = False
        for b in buckets:
            model = b.get("modelId", "")
            if "gemini-3" in model:
                f = b.get("remainingFraction", 1.0)
                if f < min_fraction:
                    min_fraction = f
                    found_model = True
        return float(min_fraction * 100) if found_model else 100.0
    except:
        return 100.0

def switch_to_best_account():
    index_path = COCKPIT_DIR / "gemini_accounts.json"
    if not index_path.exists():
        return False
    
    try:
        data = json.loads(index_path.read_text())
        accounts = data.get("accounts", [])
        best_acc = None
        max_quota = -1
        
        active_email = get_active_email()
        
        for acc in accounts:
            if acc.get("email") == active_email:
                continue
            q = float(get_quota_percentage(acc["id"]))
            if q > max_quota: # This will pick the highest quota among target project accounts
                max_quota = q
                best_acc = acc
        
        if best_acc and max_quota > float(THRESHOLD):
            print(f"Auto-Switching to {best_acc['email']} (Quota: {max_quota:.1f}%)")
            subprocess.run([str(Path.home() / "gemini-switch.py"), best_acc["email"]])
            return True
        return False
    except Exception as e:
        print(f"Error in auto-switch: {e}")
        return False

def main():
    print(f"Gemini Auto-Switch Service started (Threshold: {THRESHOLD}%)")
    while True:
        try:
            active_email = get_active_email()
            if not active_email:
                print("No active Gemini account found. Waiting...")
            else:
                acc = get_account_by_email(active_email)
                if acc:
                    quota = get_quota_percentage(acc["id"])
                    print(f"Current Account: {active_email} | Quota: {quota:.1f}%")
                    if quota < THRESHOLD:
                        print("Quota below threshold! Triggering switch...")
                        switch_to_best_account()
                else:
                    print(f"Active account {active_email} not found in Cockpit index.")
            
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Loop error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
