#!/usr/bin/env python3
"""Run conversion cases and real GDB breakpoint/local-variable checks."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def verify(binary):
    binary = Path(binary).resolve(strict=True)
    env = dict(os.environ, LC_ALL="C")
    for fahrenheit, celsius in [(32, 0), (212, 100), (-40, -40), (98.6, 37)]:
        result = subprocess.run(
            [str(binary)], input=f"{fahrenheit}\n", text=True,
            capture_output=True, timeout=10, env=env,
        )
        expected = f"{fahrenheit:.2f} F = {celsius:.2f} C"
        check(result.returncode == 0 and expected in result.stdout,
              f"{binary.name}: expected {expected!r}, got {result}")
        print(f"PASS {binary.name}: {expected}")

    result = subprocess.run(
        [str(binary)], input="not-a-number\n", text=True,
        capture_output=True, timeout=10, env=env,
    )
    check(result.returncode == 1 and "Invalid input" in result.stderr,
          f"{binary.name}: invalid input was not rejected")
    print(f"PASS {binary.name}: invalid input returns 1")

    with tempfile.TemporaryDirectory(prefix="ggi1-gdb-") as directory:
        input_file = Path(directory) / "input.txt"
        input_file.write_text("212\n")
        commands = Path(directory) / "verify.gdb"
        commands.write_text(
            "set pagination off\n"
            "set confirm off\n"
            "set debuginfod enabled off\n"
            "break fahrenheit_to_celsius\n"
            f"run < {input_file}\n"
            'printf "GGI1_ARG=%.2f\\n", fahrenheit\n'
            "next\n"
            "info locals\n"
            'printf "GGI1_RESULT=%.2f\\n", celsius\n'
            "continue\n"
        )
        result = subprocess.run(
            ["/usr/bin/gdb", "-q", "-nx", "--batch", "-x", str(commands), str(binary)],
            text=True, capture_output=True, timeout=30, env=env,
        )
        print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, file=sys.stderr, end="")
        check(result.returncode == 0 and "GGI1_ARG=212.00" in result.stdout
              and "GGI1_RESULT=100.00" in result.stdout
              and "exited normally" in result.stdout,
              f"{binary.name}: GDB breakpoint/variables/exit verification failed")
    print(f"PASS {binary.name}: GDB breakpoint, step, variables and normal exit")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: verify.py C_EXECUTABLE CPP_EXECUTABLE")
    for executable in sys.argv[1:]:
        verify(executable)
    print("ALL CHECKS PASSED: 8 conversions, 2 invalid inputs, 2 GDB sessions")
