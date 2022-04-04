from numpy import rec
import metadata_utils as mu

best_matches = mu.read_csv("edited_sheets/best_matches.csv")
authors = mu.read_csv("edited_sheets/check_author.csv")
keywords = mu.read_csv("edited_sheets/check_keywords.csv")
languages = mu.read_csv("edited_sheets/check_language.csv")
pub_places = mu.read_csv("edited_sheets/check_pub_place.csv")
pub_dates = mu.read_csv("edited_sheets/check_publication_date.csv")
publishers = mu.read_csv("edited_sheets/check_pub_place.csv")

mul_lang = []

#starting_loop
for record in best_matches[1:]:
    #author
    if not record[3]:
        for author_entry in authors:
            if author_entry[1] == record[1]:
                if author_entry[4]:
                    record[3] = author_entry[4]
                else:
                    record[3] = author_entry[2]
    #keywords
    if not record[9]:
        for keyword_entry in keywords:
            if keyword_entry[4]:
                record[9] = keyword_entry[4]
            else:
                record[9] = keyword_entry[2]
    #language:
    if record[7] == "mul":
        mul_lang.append([record[0], record[1], record[7], f"https://search.lib.umich.edu/catalog/record/{record[0]}", f"https://quod.lib.umich.edu/p/philamer/{record[1]}" ])
        record[7] = "eng spa"
    if not record[7]:
        for language_entry in languages:
            if languages[4]:
                record[7] = language_entry[4]
            else:
                record[7] = language_entry[2]
    #pub_place
    if not record[4]:
        for pub_place in pub_places:
            if pub_place[4]:
                record[4] = pub_place[4]
            else:
                record[4] = pub_place[2]
    #pub_date
    if not record[6]:
        for pub_date in pub_dates:
            if pub_date[4]:
                record[6] = pub_date[4]
            else:
                record[6] = pub_date[2]
    #publisher
    if not record[5]:
        for publisher in publishers:
            if publisher[4]:
                record[5] = publisher[4]
            else:
                record[5] = publisher[2]

mu.write_csv("full_best_values.csv", best_matches)
mu.write_csv("mul_languages.csv", mul_lang)

print("done")