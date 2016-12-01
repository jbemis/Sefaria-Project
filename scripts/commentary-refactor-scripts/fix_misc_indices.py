# -*- coding: utf-8 -*-

from sefaria.model import *

rifs = IndexSet({"title": {"$regex": "^Rif"}})
for idx in rifs:
    print idx.title
    idx.categories.insert(1, "Commentary")
    base_book = idx.title.replace("Rif ", '').strip()
    idx.dependence = 'Commentary'
    idx.work_title = "Rif"
    idx.base_text_mapping = None
    bidx = library.get_index(base_book)
    idx.base_text_titles = [base_book]
    idx.related_categories = [c for c in bidx.categories if c not in idx.categories]
    idx.save(override_dependencies=True)

