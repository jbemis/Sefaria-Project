# -*- coding: utf-8 -*-

from sefaria.model import *

rifs = IndexSet({"title": {"$regex": "^Rif"}})
for idx in rifs:
    idx.categories.insert(1, "Commentary")
    idx.save()
    base_book = idx.title.replace(work_title + " ", '').strip()
    idx.dependence = 'commentary'
    idx.work_title = "Rif"
    idx.base_text_mapping = None
    bidx = library.get_index(base_book)
    idx.base_text_titles = [base_book]
    idx.related_categories = [c for c in bidx.categories if c not in idx.categories]
    idx.save(override_dependencies=True)

