"""
Workaround for pypa/pipx#1539.

Ensures the shared libs are built, then uninstalls setuptools.
"""

import os
import re
import shutil
import subprocess


def get_pipx_shared_libs():
    """Retrieves the PIPX_SHARED_LIBS path from pipx environment."""
    result = subprocess.run(['pipx', 'environment'], capture_output=True, text=True)
    match = re.search(r'PIPX_SHARED_LIBS=(.+)', result.stdout)
    if match:
        return match.group(1)
    else:
        raise ValueError("Could not find PIPX_SHARED_LIBS in pipx environment output")


def main():
    # Upgrade the pipx shared environment
    subprocess.run(['pipx', 'upgrade-shared'])

    # Get the PIPX_SHARED_LIBS path
    shared_libs_path = get_pipx_shared_libs()

    # Construct search paths for 'python' executable within the shared environment
    search_paths = [
        os.path.join(shared_libs_path, 'bin'),  # Linux
        os.path.join(shared_libs_path, 'Scripts'),  # Windows
    ]

    # Resolve the 'python' executable path using shutil.which
    python_path = shutil.which('python', path=os.pathsep.join(search_paths))

    if not python_path:
        raise ValueError(
            "Could not find 'python' executable in the pipx shared environment"
        )

    # Uninstall setuptools if present
    subprocess.run([python_path, '-m', 'pip', 'uninstall', '-y', 'setuptools'])


if __name__ == "__main__":
    main()
