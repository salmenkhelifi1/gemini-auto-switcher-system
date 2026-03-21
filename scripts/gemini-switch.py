#!/usr/bin/env python3
import json
import sys
import os
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: gemini-switch.py <email_or_id>")
        sys.exit(1)

    target = sys.argv[1]
    cockpit_dir = Path.home() / ".antigravity_cockpit"
    gemini_dir = Path.home() / ".gemini"
    
    accounts_index_path = cockpit_dir / "gemini_accounts.json"
    if not accounts_index_path.exists():
        print(f"Error: {accounts_index_path} not found.")
        sys.exit(1)
        
    index_data = json.loads(accounts_index_path.read_text())
    accounts = index_data.get("accounts", [])
    
    target_account = None
    for acc in accounts:
        if acc.get("email") == target or acc.get("id") == target:
            target_account = acc
            break
            
    if not target_account:
        print(f"Error: Account '{target}' not found in cockpit-tools.")
        sys.exit(1)
        
    acc_id = target_account["id"]
    acc_file = cockpit_dir / "gemini_accounts" / f"{acc_id}.json"
    
    if not acc_file.exists():
        print(f"Error: Account detail file {acc_file} not found.")
        sys.exit(1)
        
    full_acc = json.loads(acc_file.read_text())
    
    # 1. Update google_accounts.json
    ga_path = gemini_dir / "google_accounts.json"
    ga_data = {"active": full_acc["email"], "old": []}
    if ga_path.exists():
        try:
            curr_ga = json.loads(ga_path.read_text())
            ga_data["old"] = curr_ga.get("old", [])
            curr_active = curr_ga.get("active")
            if curr_active and curr_active != full_acc["email"] and curr_active not in ga_data["old"]:
                ga_data["old"].append(curr_active)
        except:
            pass
    ga_path.write_text(json.dumps(ga_data, indent=2))
    
    # 2. Update oauth_creds.json
    oc_path = gemini_dir / "oauth_creds.json"
    oc_data = {
        "access_token": full_acc.get("access_token"),
        "refresh_token": full_acc.get("refresh_token"),
        "id_token": full_acc.get("id_token"),
        "token_type": full_acc.get("token_type", "Bearer"),
        "scope": full_acc.get("scope"),
        "expiry_date": full_acc.get("expiry_date")
    }
    # Filter out None values
    oc_data = {k: v for k, v in oc_data.items() if v is not None}
    oc_path.write_text(json.dumps(oc_data, indent=2))
    
    print(f"Successfully switched to Gemini account: {full_acc['email']}")

if __name__ == "__main__":
    main()
