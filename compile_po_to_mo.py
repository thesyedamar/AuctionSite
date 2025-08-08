import polib
import os

po_path = os.path.join('auctions', 'locale', 'ar', 'LC_MESSAGES', 'django.po')
mo_path = os.path.join('auctions', 'locale', 'ar', 'LC_MESSAGES', 'django.mo')

po = polib.pofile(po_path)
po.save_as_mofile(mo_path)

print(f"Compiled {po_path} to {mo_path}") 