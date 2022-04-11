import metadata_utils as mu


full_best = mu.read_csv("full_best_values.csv")
oor_list = []
yr_range = range(1870, 1926)
for entry in full_best:
    yr1 = entry[6].replace(".","").replace("c","").replace("[","").replace("]","")
    if "-" in yr1:
        yr1 = entry[6].split("-")[0][:4]
    if len(yr1) > 4:
        yr1 = yr1[0:4]
    print(yr1)
    try:
        test_yr = int(yr1)
        if test_yr not in yr_range:
            print("out of range found")
            oor_list.append(entry)
    except:
        continue

mu.write_csv("out_of_range.csv", oor_list)