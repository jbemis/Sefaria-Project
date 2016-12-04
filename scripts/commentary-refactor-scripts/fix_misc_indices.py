# -*- coding: utf-8 -*-

from sefaria.model import *
print "Fixing Rif Index Records..."
rifs = IndexSet({"title": {"$regex": "^Rif"}})
for idx in rifs:
    print idx.title
    categories = ['Talmud', 'Bavli', 'Commentary', 'Rif']
    base_book = idx.title.replace("Rif ", '').strip()
    idx.dependence = 'Commentary'
    idx.work_title = "Rif"
    idx.base_text_mapping = None
    bidx = library.get_index(base_book)
    idx.base_text_titles = [base_book]
    related_categories = [c for c in bidx.categories if c not in categories]
    idx.categories = categories + related_categories
    idx.save(override_dependencies=True)

