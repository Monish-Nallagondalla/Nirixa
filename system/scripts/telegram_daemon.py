#!/usr/bin/env python3
"""
Nirixa OS Legacy Script Wrapper
Routes execution directly to system/engine/daemon.py
"""

import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
engine_dir = os.path.abspath(os.path.join(script_dir, "..", "engine"))
sys.path.insert(0, engine_dir)

import daemon

if __name__ == "__main__":
    test_mode = "--test-connection" in sys.argv or "--test" in sys.argv
    daemon.start_daemon(test_only=test_mode)
