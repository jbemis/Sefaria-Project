
# -*- coding: utf-8 -*-

from sefaria.model import *
from sefaria.utils.hebrew import hebrew_term, is_hebrew
import re


commentary2 = IndexSet({"categories.0": "Commentary2"})
targums = IndexSet({"categories.1": "Targum"})

### ---------------------------- Targum ----------------------------------------------- #####

targum_collective_titles = [('Aramaic Targum', 'to ', u'תרגום'),
                            ('Targum Jonathan', 'on ', u'תרגום יונתן'),
                            ('Onkelos', '', u'תרגום אונקלוס'),
                            ('Targum Neofiti', None),
                            ('Targum Jerusalem', None),
                            ('Tafsir Rasag', None)]
for trg in targums:
    print trg.title
    for t in targum_collective_titles:
        if t[0] in trg.title:
            tup = t
            collective_title = tup[0]
            if tup[1] is not None:
                base_books = [trg.title.replace(tup[0]+' '+tup[1], '')]
            else:
                base_books = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy']
            break
    trg.dependence = 'Targum'
    trg.collective_title = collective_title
    trg.auto_linking_scheme = 'match_base_text_depth'
    if base_books:
        trg.base_text_titles = base_books
        for b in base_books:
            bidx = library.get_index(b)
            trg.related_categories = [c for c in bidx.categories if c not in trg.categories]
    trg.save(override_dependencies=True)
    if not Term().load({"name": trg.collective_title}):
        term = Term({"name": trg.collective_title, 'scheme': 'targum_titles'})
        if len(tup) >= 2:
            he_collective_title = tup[2]
        else:
            he_collective_title = trg.get_title('he')
        titles = [
            {
                "lang": "en",
                "text": trg.collective_title,
                "primary": True
            },
            {
                "lang": "he",
                "text": he_collective_title,
                "primary": True
            }
        ]
        term.set_titles(titles)
        term.save()

### ---------------------------- Commentary 2 ----------------------------------------------- #####

base_text_mappings = {
    'Shney Luchot HaBrit' : ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"],
    'Meshech Hochma' : ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"],
    'Siftei Hakhamim' : ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"],
    'Ralbag Esther': ["Esther"],
    'Chizkuni': ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"],
    'Lev Sameach' : ["Sefer HaMitzvot LaRambam"],
    'Penei David' : ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"],
    'Ralbag Song of Songs' : ['Song of Songs'],
    'Rabbeinu Bahya' : ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"],
    "Ralbag Ruth" : ["Ruth"],
    "Eben Ezra on Lamentations" : ["Lamentations"],
    "Kinaat Sofrim al Sefer Hamitzvot" : ["Sefer HaMitzvot LaRambam"],
    "Marganita Tava al Sefer Hamitzvot" : ["Sefer HaMitzvot LaRambam"],
    "Megilat Esther al Sefer Hamitzvot" : ["Sefer HaMitzvot LaRambam"],
    "Rambam Introduction to Masechet Horayot" : ["Mishnah Horayot"]
}

for com2 in commentary2:
    print com2.title
    if ' on ' in com2.title:
        on_title = com2.title.split(" on ")[1].strip()
        try:
            base_books = [library.get_index(on_title).title]
        except Exception as e:
            base_books = [t for t in library.get_indexes_in_category(on_title)]
    elif com2.title in base_text_mappings:
        base_books = []
        for i in base_text_mappings[com2.title]:
            try:
                base_books.append(library.get_index(i).title)
            except Exception as ex:
                pass
    else:
        base_books = []

    com2.categories = [com2.categories[1], 'Commentary'] + com2.categories[2:]
    com2.dependence = 'Commentary'
    com2.collective_title = com2.categories[2]
    com2.auto_linking_scheme = None
    if len(base_books):
        com2.base_text_titles = base_books
        other_categories = []
        for b in base_books:
            bidx = library.get_index(b)
            o_cats = [c for c in bidx.categories if c not in com2.categories and c not in other_categories]
            other_categories += o_cats
        com2.related_categories = other_categories
    com2.save(override_dependencies=True)

    if not Term().load({"name": com2.collective_title}):
        he_collective_title = hebrew_term(com2.collective_title)
        if not he_collective_title or not is_hebrew(he_collective_title):
            he_collective_title = com2.get_title("he").split(u" על ")[0]
        term = Term({"name": com2.collective_title, 'scheme': 'commentary_titles'})
        titles = [
            {
                "lang": "en",
                "text": com2.collective_title,
                "primary": True
            },
            {
                "lang": "he",
                "text": he_collective_title,
                "primary": True
            }
        ]
        term.set_titles(titles)
        term.save()










