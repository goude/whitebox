.phony: all clean build watch compile test

all: clean test compile build

clean:
	rm -f output/whitebox.*
	find . | grep -E "(__pycache__|\.mypy_cache|\.pyc|\.pyo$$)" | xargs rm -rf

test:
	pipenv run pytest --mypy --color yes

watch:
	openscad output/whitebox.scad &
	echo whitebox.py | entr -s 'make compile'

compile:
	pipenv run python3 whitebox.py

build:
	openscad -o output/whitebox.stl output/whitebox.scad
	openscad --render -o output/whitebox.png output/whitebox.scad
