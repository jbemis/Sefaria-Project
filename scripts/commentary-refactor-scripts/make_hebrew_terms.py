# -*- coding: utf-8 -*-

from sefaria.model import *
from sefaria.utils.hebrew import hebrew_term, is_hebrew
from sefaria.system.exceptions import InputError
import re



"""
Simple translations for common Hebrew words
"""
categories = {
    "Torah":                u"תורה",
    "Tanakh":               u'תנ"ך',
    "Tanakh":               u'תנ"ך',
    "Prophets":             u"נביאים",
    "Writings":             u"כתובים",
    "Commentary":           u"מפרשים",
    "Targum":               u"תרגומים",
    "Mishnah":              u"משנה",
    "Tosefta":              u"תוספתא",
    "Talmud":               u"תלמוד",
    "Bavli":                u"בבלי",
    "Yerushalmi":           u"ירושלמי",
    "Rif":		            u'רי"ף',
    "Kabbalah":             u"קבלה",
    "Halakha":              u"הלכה",
    "Halakhah":             u"הלכה",
    "Law":					u"הלכה",
    "Midrash":              u"מדרש",
    "Aggadic Midrash":      u"מדרש אגדה",
    "Halachic Midrash":     u"מדרש הלכה",
    "Midrash Rabbah":       u"מדרש רבה",
    "Responsa":             u'שו"ת',
    "Other":                u"שונות",
    "Siddur":               u"סידור",
    "Liturgy":              u"תפילה",
    "Piyutim":              u"פיוטים",
    "Musar":                u"ספרי מוסר",
    "Chasidut":             u"חסידות",
    "Parshanut":            u"פרשנות",
    "Philosophy":           u"מחשבת ישראל",
    "Maharal":              u'מהר"ל מפראג',
    "Apocrypha":            u"ספרים חיצונים",
    "Seder Zeraim":         u"סדר זרעים",
    "Seder Moed":           u"סדר מועד",
    "Seder Nashim":         u"סדר נשים",
    "Seder Nezikin":        u"סדר נזיקין",
    "Seder Kodashim":       u"סדר קדשים",
    "Seder Toharot":        u"סדר טהרות",
    "Seder Tahorot":        u"סדר טהרות",
    "Dictionary":           u"מילון",
    "Early Jewish Thought": u"מחשבת ישראל קדומה",
    "Minor Tractates":      u"מסכתות קטנות",
    "Modern Works":		u"יצירות מודרניות",
    "Grammatica Hebraica" : u'דקדוק'
}

collective_works_categories = {
    "Rosh":                 u'רא"ש',
    "Maharsha":             u'מהרש"א',
    "Rashba":	        u'רשב"א',
    "Ritva":			 u'ריטב"א',
    "Maharam Shif":		u'מהר"ם שיף',
    "Rambam":	        u'רמב"ם',
    "Yad Ramah":		u"יד רמה",
    "Raavad":		u'ראב"ד',
    "Radbaz":		u'רדב"ז',
    "Pri Yitzhak": u'פרי יצחק',
    "Tosafot Yom Tov":      u"תוספות יום טוב",
    "Chidushei Halachot":   u"חידושי הלכות",
    "Chidushei Agadot":     u"חידושי אגדות",
    "Tiferet Shmuel":       u"תפארת שמואל",
    "Korban Netanel":       u"קרבן נתנאל",
    "Pilpula Charifta":     u"פילפולא חריפתא",
    "Divrey Chamudot":      u"דברי חמודות",
    "Maadaney Yom Tov":     u"מעדני יום טוב",
    "Shita Mekubetzet":     u'שיטה מקובצת',
    "Maharshal": u'מהרש"ל',
    "Gur Aryeh": u'גור אריה',
    "Tur and Commentaries": u'טור ומפרשיו',
    "Yachin": u'יכין',
    "Boaz": u'בועז',
    "Harchev Davar": u'הרחב דבר',
    "Minchat Shai": u'מנחת שי'
}

pseudo_categories = {
    "Mishneh Torah":   u"משנה תורה",
    'Introduction':    u"הקדמה",
    'Sefer Madda':     u"ספר מדע",
    'Sefer Ahavah':    u"ספר אהבה",
    'Sefer Zemanim':   u"ספר זמנים",
    'Sefer Nashim':    u"ספר נשים",
    'Sefer Kedushah':  u"ספר קדושה",
    'Sefer Haflaah':   u"ספר הפלאה",
    'Sefer Zeraim':    u"ספר זרעים",
    'Sefer Avodah':    u"ספר עבודה",
    'Sefer Korbanot':  u"ספר קורבנות",
    'Sefer Taharah':   u"ספר טהרה",
    'Sefer Nezikim':   u"ספר נזיקין",
    'Sefer Kinyan':    u"ספר קניין",
    'Sefer Mishpatim': u"ספר משפטים",
    'Sefer Shoftim':   u"ספר שופטים",
    "Shulchan Arukh":  u"שולחן ערוך",
}

section_names = {
    "Chapter":          u"פרק",
    "Chapters":         u"פרקים",
    "Perek":            u"פרק",
    "Line":             u"שורה",
    "Negative Mitzvah": u"מצות לא תעשה",
    "Positive Mitzvah": u"מצות עשה",
    "Negative Mitzvot": u"מצוות לא תעשה",
    "Positive Mitzvot": u"מצוות עשה",
    "Daf":              u"דף",
    "Paragraph":        u"פסקה",
    "Parsha":           u"פרשה",
    "Parasha":          u"פרשה",
    "Parashah":         u"פרשה",
    "Seif":             u"סעיף",
    "Se'if":            u"סעיף",
    "Siman":            u"סימן",
    "Section":          u"חלק",
    "Verse":            u"פסוק",
    "Sentence":         u"משפט",
    "Sha'ar":           u"שער",
    "Gate":             u"שער",
    "Comment":          u"פירוש",
    "Phrase":           u"ביטוי",
    "Mishna":           u"משנה",
    "Chelek":           u"חלק",
    "Helek":            u"חלק",
    "Year":             u"שנה",
    "Masechet":         u"מסכת",
    "Massechet":        u"מסכת",
    "Letter":           u"אות",
    "Halacha":          u"הלכה",
    "Piska":            u"פסקה",
    "Seif Katan":       u"סעיף קטן",
    "Se'if Katan":      u"סעיף קטן",
    "Volume":           u"כרך",
    "Book":             u"ספר",
    "Shar":             u"שער",
    "Seder":            u"סדר",
    "Part":             u"חלק",
    "Pasuk":            u"פסוק",
    "Sefer":            u"ספר",
    "Teshuva":          u"תשובה",
    "Teshuvot":         u"תשובות",
    "Tosefta":          u"תוספתא",
    "Halakhah":         u"הלכה",
    "Kovetz":           u"קובץ",
    "Path":             u"נתיב",
    "Parshah":          u"פרשה",
    "Midrash":          u"מדרש",
    "Mitzvah":          u"מצוה",
    "Tefillah":         u"תפילה",
    "Torah":            u"תורה",
    "Perush":           u"פירוש",
    "Peirush":          u"פירוש",
    "Aliyah":           u"עלייה",
    "Tikkun":           u"תיקון",
    "Tikkunim":         u"תיקונים",
    "Hilchot":          u"הילכות",
    "Topic":            u"נושא",
    "Contents":         u"תוכן",
    "Article":	    u"סעיף",
    "Shoresh":	u"שורש",
    "Story":	u"סיפור",
    "Remez":	u"רמז"
}


def create_term(eng_title, he_title, scheme):
    term = Term().load({"name": eng_title})
    if not term:
        term = Term({"name": eng_title, 'scheme': scheme})
        titles = [
            {
                "lang": "en",
                "text": eng_title,
                "primary": True
            },
            {
                "lang": "he",
                "text": he_title,
                "primary": True
            }
        ]
        term.set_titles(titles)
        term.save()
        return term
    elif term.scheme != scheme:
        raise InputError("The term {} exists in an unexpected scheme {}".format(eng_title, term.scheme))
    else:
        return term


def turn_translation_table_into_terms(table, term_scheme):
    for eng_term in table:
        try:
            create_term(eng_term, table[eng_term], term_scheme)
        except InputError as e:
            print e.message

print "TOC CATEGORIES"
turn_translation_table_into_terms(categories, 'toc_categories')
print "COMMENTATOR TERMS"
turn_translation_table_into_terms(collective_works_categories, 'commentary_works')
print "PSEUDO CATEGORIES"
turn_translation_table_into_terms(pseudo_categories, 'pseudo_toc_categories')
print "SECTION NAMES"
turn_translation_table_into_terms(section_names, 'section_names')
