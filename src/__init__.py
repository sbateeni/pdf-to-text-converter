"""
PDF to Text Converter Package
"""

import os
import sys

# Add the package directory to the Python path
package_dir = os.path.dirname(os.path.abspath(__file__))
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)
