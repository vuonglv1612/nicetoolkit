#!/usr/bin/env python3
import re
from datetime import datetime
from pathlib import Path


def read_version():
    """Read version from VERSION file."""
    version_file = Path("VERSION")
    if not version_file.exists():
        return None
    return version_file.read_text().strip()


def parse_version(version_str):
    """Parse version string into year, month, and patch components."""
    match = re.match(r"(\d{4})\.(\d{2})\.(\d+)", version_str)
    if not match:
        return None
    return tuple(map(int, match.groups()))


def bump_version():
    """
    Auto-bump version based on current date.
    - If year changed: reset to year.month.1
    - If month changed: reset to year.month.1
    - If same year/month: increment patch
    """
    now = datetime.now()
    current_version = read_version()

    if not current_version:
        # Initialize with current year/month and patch 1
        new_version = f"{now.year}.{now.month:02d}.1"
    else:
        version_parts = parse_version(current_version)
        if not version_parts:
            print(f"Error: Invalid version format in VERSION file: {current_version}")
            return False

        year, month, patch = version_parts

        if now.year != year or now.month != month:
            # Year or month changed, reset patch
            new_version = f"{now.year}.{now.month:02d}.1"
        else:
            # Same year and month, increment patch
            new_version = f"{year}.{month:02d}.{patch + 1}"

    # Write new version
    Path("VERSION").write_text(new_version + "\n")
    print(f"Version bumped to: {new_version}")
    return True


if __name__ == "__main__":
    bump_version()
