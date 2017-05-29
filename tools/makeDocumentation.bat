E:
cd E:\GitNanoleaf
python C:\Python36\Scripts\pdoc --html E:\GitNanoleaf\nanoleaf\ --overwrite
move /y E:\GitNanoleaf\nanoleaf\Aurora.m.html E:\GitNanoleaf\docs\Aurora.m.html
move /y E:\GitNanoleaf\nanoleaf\Setup.m.html E:\GitNanoleaf\docs\Setup.m.html
move /y E:\GitNanoleaf\nanoleaf\index.html E:\GitNanoleaf\docs\index.html
rd /Q /S E:\GitNanoleaf\nanoleaf\__pycache__
PAUSE