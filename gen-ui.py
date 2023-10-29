import os

pwd = os.path.realpath(os.path.dirname(__file__))

for ui in os.listdir("assets"):
    if ui.endswith(".ui"):
        uiname, _ = os.path.splitext(ui)
        os.system(f"pyside2-uic {pwd}/assets/{uiname}.ui -o {pwd}/views_{uiname}UI.py")

os.system(f"pyside2-rcc {pwd}/assets/Res.qrc -o {pwd}/Res.py")

print("done.")
