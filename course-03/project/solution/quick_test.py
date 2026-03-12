#!/usr/bin/env python
"""Test script for UDA-Hub Agentic App"""

import sys
import os
from pathlib import Path

# Add the solution directory to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    print("Importing workflow...")
    try:
        from agentic.workflow import orchestrator
        print("✅ Workflow imported successfully!")
        print(f"Orchestrator type: {type(orchestrator)}")
        return 0
    except Exception as e:
        print(f"❌ Error importing workflow: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

