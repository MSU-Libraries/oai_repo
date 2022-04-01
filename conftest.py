"""
Config file executed before pytest runs tests
"""
import os
import sys
src_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "src/"
)
sys.path.insert(0, src_path)

