# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = ''
copyright = '2026, Pdrops'
author = ''

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx_book_theme",
    "sphinx_design",
    "sphinx_copybutton",
]

templates_path = ['_templates']
exclude_patterns = []

language = 'pt_BR'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
# html_theme_options = {
#     # Altera a profundidade máxima do menu lateral para aceitar mais subníveis
#     "navigation_depth": 2,
    
#     # Opcional: Garante que os níveis fiquem expandidos e visíveis por padrão
#     "show_nav_level": 2, 
# }

html_static_path = ['_static']

myst_enable_extensions = [
    "tasklist",
    "colon_fence",     # Permite usar os blocos ::: para os cards e alertas
    "attrs_inline",
]
