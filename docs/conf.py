# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.abspath('../src'))

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'python-iptools'
copyright = u'2012, Bryan Davis'
version = '0.4.0'
release = '0.4.0'
exclude_patterns = ['_build']
pygments_style = 'sphinx'

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
  html_theme = 'default'
else:
  html_theme = 'nature'
html_static_path = ['_static']
htmlhelp_basename = 'iptoolsdoc'

