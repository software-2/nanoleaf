E:
cd E:\GitNanoleaf
python C:\Python36\Scripts\pdoc --html E:\GitNanoleaf\nanoleaf\nanoleaf.py --overwrite
move /y E:\GitNanoleaf\nanoleaf.m.html E:\GitNanoleaf\docs\nanoleaf.m.html
rd /Q /S E:\GitNanoleaf\nanoleaf\__pycache__
PAUSE