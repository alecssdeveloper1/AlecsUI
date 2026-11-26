from pathlib import Path

p = Path("install.sh")
c = p.read_text(encoding="utf-8")

c = c.replace("AlecsUI v1.7", "AlecsUI v1.8")
old_logo = "<span>Re</span><i>X</i><span>UI</span>"
new_logo = "<span>Alecs</span><i>UI</i>"
print("old logos before:", c.count(old_logo))
c = c.replace(old_logo, new_logo)
print("old logos after:", c.count(old_logo))
print("new logos:", c.count(new_logo))
print("v1.7 left:", c.count("AlecsUI v1.7"))
print("v1.8 count:", c.count("AlecsUI v1.8"))
print("menu line ok:", "===== AlecsUI v1.8 MENU =====" in c)

p.write_text(c, encoding="utf-8")
print("install.sh updated")
