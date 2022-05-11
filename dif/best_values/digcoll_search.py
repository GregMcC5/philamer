import metadata_utils as mu
import urllib.parse

def encode(x):
    """Takes a string; Returns URL query string URL encoded"""
    encoded_string = []
    if isinstance(x,str):
        for character in x:
            if character == " ":
                encoded_string.append("+")
            else:
                encoded_string.append(urllib.parse.quote(character, safe=""))
    encoded_string = "".join(encoded_string)
    return encoded_string

best_values = mu.read_csv("new_full_best_values.csv")
dlxs = mu.read_csv("dlxs_full.csv")

search_doc = [["mms_id","dlxs_id", "dlxs_title", "dlxs_link", "cat_search_link", "digicoll-only_id","notes"]]
for dlxs_entry in dlxs[1:]:
    for row in best_values[1:]:
        if dlxs_entry[1] ==  row[1]:
            dlxs_title = dlxs_entry[2]
            dlxs_link = f'https://quod.lib.umich.edu/p/philamer/{dlxs_entry[1]}'
            cat_search_link = f'https://search.lib.umich.edu/catalog?library=All+libraries&query=title%3A%28{encode(dlxs_title)}%29'
            search_doc.append([row[0], dlxs_entry[1], dlxs_title, dlxs_link, cat_search_link,"",""])

mu.write_csv("digcoll_search.csv", search_doc)

new_search_links = [["mms_id", "new_cat_search_link"]]
for dlxs_entry in dlxs[1:]:
    for row in best_values[1:]:
        if dlxs_entry[1] == row[1]:
            dlxs_title = dlxs_entry[2]
            new_cat_search_link = f'https://search.lib.umich.edu/catalog?library=All+libraries&query={encode(dlxs_title)}'
            #print(new_cat_search_link)
            new_search_links.append([row[0], new_cat_search_link])

mu.write_csv("new_search_links.csv", new_search_links)

print("done")