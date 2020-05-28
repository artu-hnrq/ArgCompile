c compile: build install

b build: clean
	python3 setup.py dist

i install:
	pip3 install .

u uninstall:
	pip3 uninstall .

d develop: build
	pip3 install -e .

p publish:
	python3 -m twine upload dist/*


clean:
	python3 setup.py clean --all
	rm -fr dist
