#!/usr/bin/env python3
"""TRIZ Contradiction Matrix lookup.

Usage:
    python3 scripts/lookup.py IMPROVING WORSENING [IMPROVING WORSENING ...]

Each argument pair is a TRIZ engineering parameter number (1-39):
the parameter being improved, then the one that worsens. Prints the
Inventive Principles the classical Altshuller matrix recommends for
each pair. Run from the skill root (the script locates the matrix
relative to itself, so any working directory works).
"""
import json
import os
import sys

PARAMETERS = {
    1: "Weight of moving object", 2: "Weight of stationary object",
    3: "Length of moving object", 4: "Length of stationary object",
    5: "Area of moving object", 6: "Area of stationary object",
    7: "Volume of moving object", 8: "Volume of stationary object",
    9: "Speed", 10: "Force", 11: "Stress or pressure", 12: "Shape",
    13: "Stability of composition", 14: "Strength",
    15: "Duration of action (moving)", 16: "Duration of action (stationary)",
    17: "Temperature", 18: "Illumination intensity",
    19: "Energy use by moving object", 20: "Energy use by stationary object",
    21: "Power", 22: "Loss of energy", 23: "Loss of substance",
    24: "Loss of information", 25: "Loss of time",
    26: "Quantity of substance/matter", 27: "Reliability",
    28: "Measurement accuracy", 29: "Manufacturing precision",
    30: "Object-affected harmful factors", 31: "Object-generated harmful factors",
    32: "Ease of manufacture", 33: "Ease of operation", 34: "Ease of repair",
    35: "Adaptability / versatility", 36: "Device complexity",
    37: "Difficulty of detecting and measuring", 38: "Extent of automation", 39: "Productivity",
}

PRINCIPLES = {
    1: "Segmentation", 2: "Taking out (Extraction)", 3: "Local quality",
    4: "Asymmetry", 5: "Merging", 6: "Universality", 7: "Nested doll",
    8: "Anti-weight (Counterweight)", 9: "Preliminary anti-action",
    10: "Preliminary action", 11: "Beforehand cushioning", 12: "Equipotentiality",
    13: "The other way round (Inversion)", 14: "Spheroidality / Curvature",
    15: "Dynamics", 16: "Partial or excessive action", 17: "Another dimension",
    18: "Mechanical vibration", 19: "Periodic action",
    20: "Continuity of useful action", 21: "Skipping / Rushing through",
    22: "Blessing in disguise", 23: "Feedback", 24: "Intermediary",
    25: "Self-service", 26: "Copying", 27: "Cheap short-living (Disposable)",
    28: "Mechanics substitution", 29: "Pneumatics and hydraulics",
    30: "Flexible shells and thin films", 31: "Porous materials",
    32: "Color changes", 33: "Homogeneity", 34: "Discarding and recovering",
    35: "Parameter changes", 36: "Phase transitions", 37: "Thermal expansion",
    38: "Accelerated oxidation", 39: "Inert atmosphere", 40: "Composite materials",
}


def main() -> int:
    args = sys.argv[1:]
    if not args or len(args) % 2 != 0:
        print(__doc__.strip())
        return 1
    try:
        nums = [int(a) for a in args]
    except ValueError:
        print(f"All arguments must be integers 1-39, got: {' '.join(args)}")
        return 1
    if any(not 1 <= n <= 39 for n in nums):
        print("Parameter numbers must be between 1 and 39.")
        return 1

    matrix_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "references", "contradiction-matrix.json",
    )
    with open(matrix_path) as f:
        matrix = json.load(f)["matrix"]

    for improving, worsening in zip(nums[::2], nums[1::2]):
        header = (
            f"Improving #{improving} ({PARAMETERS[improving]}) "
            f"vs worsening #{worsening} ({PARAMETERS[worsening]})"
        )
        print(header)
        if improving == worsening:
            print("  Same parameter on both sides: that's a physical contradiction —")
            print("  use references/separation-principles.md instead of the matrix.")
            print()
            continue
        cell = matrix[str(improving)][str(worsening)]
        if not cell:
            print("  No standard recommendation for this cell.")
            print("  Try an alternate parameter mapping, or the transposed pair "
                  f"({worsening} {improving}).")
        else:
            for p in cell:
                print(f"  {p:2d}  {PRINCIPLES[p]}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
