import polib
from collections import OrderedDict

po_path = 'auctions/locale/ar/LC_MESSAGES/django.po'

# Load the .po file
po = polib.pofile(po_path)

# OrderedDict to keep only the last occurrence of each msgid
unique_entries = OrderedDict()
for entry in po:
    unique_entries[entry.msgid] = entry

# Create a new POFile and add only unique entries
cleaned_po = polib.POFile()
for entry in unique_entries.values():
    cleaned_po.append(entry)

# Save the cleaned .po file (overwrite original)
cleaned_po.save(po_path)
print(f"Cleaned duplicates from {po_path}") 