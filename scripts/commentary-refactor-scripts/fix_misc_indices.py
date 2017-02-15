# -*- coding: utf-8 -*-

from sefaria.model import *
print "Fixing Rif Index Records..."
rifs = IndexSet({"title": {"$regex": "^Rif"}})
for idx in rifs:
    print idx.title
    categories = ['Talmud', 'Bavli', 'Commentary', 'Rif']
    base_book = idx.title.replace("Rif ", '').strip()
    idx.dependence = 'Commentary'
    idx.collective_title = "Rif"
    idx.base_text_mapping = None
    bidx = library.get_index(base_book)
    idx.base_text_titles = [base_book]
    related_categories = [c for c in bidx.categories if c not in categories]
    idx.categories = categories + related_categories
    idx.save(override_dependencies=True)

print "Adding Yachin to Boaz base_text_titles"
boazs = IndexSet({"title": {"$regex": "^Boaz on"}})
for idx in boazs:
    new_base_text = idx.title.replace("Boaz", "Yachin")
    print "{}=>{}".format(idx.title, new_base_text)
    if new_base_text not in idx.base_text_titles:
        idx.base_text_titles.append(new_base_text)
        idx.save(override_dependencies=True)

print "Adding fields to Divrei Negisdim"
dnidx = Index().load({'title': 'Divrei Negidim'})
dnidx.collective_title = "Divrei Negidim"
dnidx.dependence = 'Commentary'
dnidx.base_text_mapping = None
dnidx.base_text_titles = ['Pesach Haggadah']
dnidx.save(override_dependencies=True)

print "Fixing Kessef Mishneh Index Records..."
ksfs = IndexSet({"title": {"$regex": "^Kessef Mishneh"}})
for idx in ksfs:
    print idx.title
    idx.categories.insert(2, "Kessef Mishneh")
    base_book = idx.title.replace("Kessef Mishneh on ", '').strip()
    idx.dependence = 'Commentary'
    idx.collective_title = "Kessef Mishneh"
    idx.base_text_mapping = None
    idx.base_text_titles = [base_book]
    idx.save(override_dependencies=True)
