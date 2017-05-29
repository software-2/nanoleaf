E:
cd E:\GitNanoleaf
move E:\GitNanoleaf\dist\* E:\GitNanoleaf\old-dist\
copy /y LICENSE LICENSE.txt
pandoc -o README.rst README.md
python setup.py sdist bdist_wheel
del README.rst
del LICENSE.txt
rd /Q /S E:\GitNanoleaf\nanoleaf.egg-info
rd /Q /S E:\GitNanoleaf\build
PAUSE