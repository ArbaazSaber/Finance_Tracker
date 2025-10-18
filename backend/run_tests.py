#!/usr/bin/env python3
"""
Test runner for Finance Tracker Backend

Usage:
    python run_tests.py                 # Run all tests
    python run_tests.py --unit          # Run only unit tests
    python run_tests.py --models        # Run only model tests
    python run_tests.py --repositories  # Run only repository tests
    python run_tests.py --services      # Run only service tests
    python run_tests.py --apis          # Run only API tests
    python run_tests.py --coverage      # Run with coverage report
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_command(command):
    """Run a shell command and return the result."""
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, capture_output=False)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Run tests for Finance Tracker Backend")
    parser.add_argument("--unit", action="store_true", help="Run only unit tests")
    parser.add_argument("--models", action="store_true", help="Run only model tests")
    parser.add_argument("--repositories", action="store_true", help="Run only repository tests")
    parser.add_argument("--services", action="store_true", help="Run only service tests")
    parser.add_argument("--apis", action="store_true", help="Run only API tests")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Base pytest command
    cmd = [sys.executable, "-m", "pytest"]
    
    if args.verbose:
        cmd.append("-v")
    
    # Determine which tests to run
    test_paths = []
    if args.models:
        test_paths.append("tests/models")
    elif args.repositories:
        test_paths.append("tests/repositories")
    elif args.services:
        test_paths.append("tests/services")
    elif args.apis:
        test_paths.append("tests/apis")
    else:
        test_paths.append("tests")  # Run all tests
    
    # Add coverage if requested
    if args.coverage:
        cmd.extend([
            "--cov=models",
            "--cov=repositories", 
            "--cov=services",
            "--cov=apis",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov"
        ])
    
    # Add test paths
    cmd.extend(test_paths)
    
    # Run the tests
    return run_command(cmd)


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)