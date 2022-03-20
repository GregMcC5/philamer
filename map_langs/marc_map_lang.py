import metadata_utils as mu

alma = mu.read_csv("alma_full.csv")
marc_lang = mu.read_csv("Marc_lang.csv")

lang_rec_doc = []

for entry in alma:
    if "map" in entry[7]:
        lang_rec = None
        for lang in marc_lang[1:]:
            if "(" in lang[1]:
                if lang[1].split("(")[0] in entry[6]:
                    lang_rec = lang[0]
                    lang_rec_doc.append([entry[0],entry[7],lang_rec, lang[1], entry[6]])
            elif lang[1] in entry[6]:
                    lang_rec = lang[0]
                    lang_rec_doc.append([entry[0],entry[7],lang_rec, lang[1], entry[6]])
        if not lang_rec:
            lang_rec_doc.append([entry[0],entry[7],lang_rec, None, entry[6]])

lang_rec_doc.insert(0, ["mms_id", "alma_lang", "language_reccomendation_marc_code", "marc_lang", "alma_notes"])
mu.write_csv("map_lang_reccomendations.csv", lang_rec_doc)
print("done")

