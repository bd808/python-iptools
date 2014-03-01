# -*- coding: utf-8 -*-

import sys
import os
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..')))
import iptools

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'iptools'
copyright = (
    '2008-%s, Bryan Davis and iptools contributors. '
    'All Rights Reserved'
) % date.today().year
version = iptools.__version__
release = version
exclude_patterns = ['_build']
pygments_style = 'sphinx'

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    html_theme = 'default'
else:
    html_theme = 'nature'
html_static_path = ['_static']
htmlhelp_basename = 'iptoolsdoc'

autodoc_member_order = 'groupwise'
