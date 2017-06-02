E:
cd E:\GitNanoleaf\nanoleaf
python C:\Python36\Scripts\pdoc --html E:\GitNanoleaf\nanoleaf\aurora.py --overwrite
python C:\Python36\Scripts\pdoc --html E:\GitNanoleaf\nanoleaf\setup.py --overwrite
move /y E:\GitNanoleaf\nanoleaf\aurora.m.html E:\GitNanoleaf\docs\aurora.html
move /y E:\GitNanoleaf\nanoleaf\setup.m.html E:\GitNanoleaf\docs\setup.html
rd /Q /S E:\GitNanoleaf\nanoleaf\__pycache__
PAUSE