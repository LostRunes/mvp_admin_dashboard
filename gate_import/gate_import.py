import sys
import os
import json
import argparse
from importer import GateImporter

def main():
    parser = argparse.ArgumentParser(description="Import GATE questions JSON dataset into Supabase.")
    parser.add_argument("json_file", help="Path to the JSON file containing subject, topics, and questions.")
    parser.add_argument("--no-rollback", action="store_true", help="Disable automatic rollback of newly inserted rows if an error occurs.")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.json_file):
        print(f"Error: File '{args.json_file}' does not exist.")
        sys.exit(1)
        
    try:
        with open(args.json_file, 'r', encoding='utf-8') as f:
            import_data = json.load(f)
    except json.JSONDecodeError as jde:
        print(f"Error parsing JSON file: {jde}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
        
    print("[START] Initializing GATE Importer...")
    print(f"[LOAD] Loaded dataset: {args.json_file}")
    
    importer = GateImporter(rollback_on_failure=not args.no_rollback)
    
    try:
        importer.run_import(import_data)
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main()
