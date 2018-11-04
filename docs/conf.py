# -- Project information -----------------------------------------------------

project = "zsm"
copyright = "2018, Mattias Lindvall"
author = "Mattias Lindvall"

# The short X.Y version
version = "0.1.0"
# The full version, including alpha/beta/rc tags
release = version


# -- General configuration ---------------------------------------------------
master_doc = "index"

needs_sphinx = "1.0"

language = "en"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

pygments_style = "sphinx"

html_theme = "sphinx_rtd_theme"


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "zsmdoc"


# -- Options for LaTeX output ------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "zsm.tex", "ZSM Documentation",
     author, "manual"),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, "zsm", "ZSM Documentation",
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, "zsm", "ZSM Documentation",
     author, "zsm", "ZFS Snapshot Manager",
     "Miscellaneous"),
]
