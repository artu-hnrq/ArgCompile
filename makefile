compile:
		rm dist/*
		python3 setup.py sdist bdist_wheel
		pip3 install ./dist/*.tar.gz

publish:
		python3 -m twine upload dist/*
