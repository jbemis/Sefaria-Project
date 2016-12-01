# -*- coding: utf-8 -*-

from sefaria.model.text import Index, CommentaryIndex, IndexSet, VersionSet
from sefaria.model.schema import Term
from sefaria.system.database import db
import re

talmud_commentaries = IndexSet({'dependence': 'Commentary', 'categories.0': 'Talmud'})
for idx in talmud_commentaries:
    print idx.title
    idx.categories.remove('Bavli')
    idx.categories.insert(1, 'Bavli')
    idx.save(override_dependencies=True)