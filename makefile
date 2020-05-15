compile:
		python3 setup.py sdist bdist_wheel
		pip3 install ./dist/argcompile-0.0.1.tar.gz
