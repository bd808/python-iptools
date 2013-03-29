# -*- coding: utf-8 -*-

import sys
import os
import datetime

sys.path.append(os.path.abspath('../src'))
import iptools

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'python-iptools'
copyright = '%s, Bryan Davis. All Rights Reserved' % datetime.date.today().year
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

