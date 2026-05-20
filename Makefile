html:
	jupyter-book build .

pdf:
	jupyter-book build . --builder pdflatex

epub:
	jupyter-book build . --builder epub

all: html pdf epub
