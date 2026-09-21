"""Sphinx documentation configuration file for SIDORA AI MLOps Platform."""

import os
import sys

# Add app_api to sys.path so Sphinx autodoc can import the application modules
sys.path.insert(0, os.path.abspath("../app_api"))

# Project metadata
project = "SIDORA AI - MLOps Platform"
copyright = "2026, SIDORA AI Engineering Team"
author = "SIDORA AI"
release = "0.1.0"

# Extensions
extensions = [
    "sphinx.ext.autodoc",       # Core extension to extract docstrings
    "sphinx.ext.napoleon",      # Support for Google and NumPy style docstrings
    "sphinx.ext.viewcode",      # Add links to source code in generated docs
    "sphinx.ext.githubpages",   # Creates .nojekyll for GitHub Pages compatibility
]

# Napoleon configuration for Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_ivar = True

# Suppress duplicate object description warnings between docstrings and attribute inspection
suppress_warnings = ["autodoc.duplicate_object"]

# Autodoc configuration
autodoc_member_order = "bysource"
autodoc_typehints = "description"

# Excluded patterns during build
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# HTML output settings
html_theme = "sphinx_rtd_theme"
html_static_path = []
