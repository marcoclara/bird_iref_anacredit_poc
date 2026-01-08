################################################################################
# BIRD & IReF
# Data Model Definition & Implementation for BIRD and IReF Framework Enablement
# Universidade Aberta - MEIW - Marco Clara (nº 2302597)
################################################################################

import os
import json
from arelle import Cntlr

# Path to your xBRL-JSON file
json_file_path = "anacredit_ecb/output/metadata/xbrl.json"

# Step 1: Check if file exists
if not os.path.exists(json_file_path):
    print(f"❌ File not found: {json_file_path}")
else:
    # Step 2: Check JSON syntax before loading into Arelle
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON syntax error: {e}")
    else:
        # Step 3: Load and validate with Arelle
        controller = Cntlr.Cntlr()
        model_xbrl = controller.modelManager.load(json_file_path)

        if not model_xbrl or not hasattr(model_xbrl, "errors"):
            print("❌ Failed to load the file or access validation errors.")
        elif model_xbrl.errors:
            print("❌ Validation errors found:")
            for error in model_xbrl.errors:
                print(f"- {error}")
        else:
            print("✅ No validation errors found.")

        print("\n🔍 Validation process completed.")