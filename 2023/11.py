def find_empty_rows_and_columns(words):
    empty_rows = []
    for i,w in enumerate(words):
        if all(c!='#' for c in w):
            empty_rows.append(i)
    empty_cols = []
    for j in range(len(words[0])):
        if all(words[i][j]!='#' for i in range(len(words))):
            empty_cols.append(j)
    return empty_rows, empty_cols

def find_galaxies(words):
    galaxies = []
    for i,w in enumerate(words):
        for j,c in enumerate(w):
            if c =='#':
                galaxies.append((i,j))
    return galaxies
   
def calc_sum(words):
    empty_rows, empty_cols = find_empty_rows_and_columns(words)
    galaxies = find_galaxies(words)
    add_rows = 0
    gal_rows = sorted([g[0] for g in galaxies])
    gal_cols = sorted([g[1] for g in galaxies])
    i_e_r = 0
    #print(empty_rows)
    for i_g in range(len(gal_rows)):
        while (i_e_r < len(empty_rows)) and (gal_rows[i_g]>empty_rows[i_e_r]):
            add_rows += 1000000-1
            i_e_r+=1
        gal_rows[i_g] += add_rows
    add_cols = 0
    i_e_c = 0

    for i_g in range(len(gal_cols)):
        while (i_e_c < len(empty_cols)) and (gal_cols[i_g]>empty_cols[i_e_c]):
            add_cols += 1000000-1
            i_e_c+=1
        gal_cols[i_g] += add_cols
   
    gal_rows = sorted(gal_rows)
    gal_cols = sorted(gal_cols)
    # print(gal_rows)
    # print(gal_cols)
    final_sum = 0
    for i in range(len(gal_rows)-1):
        for j in range(i+1, len(gal_rows)):
            final_sum += gal_rows[j]-gal_rows[i] + gal_cols[j]-gal_cols[i]
    return final_sum

print(calc_sum(words))