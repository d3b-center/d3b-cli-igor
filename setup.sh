pip3 install wheel
pip3 install --upgrade pip
python3 setup.py bdist_wheel --universal
pip3 install --force-reinstall dist/d3b_cli_igor-0.2-py2.py3-none-any.whl
