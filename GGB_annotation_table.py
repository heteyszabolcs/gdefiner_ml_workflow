import pandas as pd
import re

# Load your ChocoPhlAn species taxonomy file
path = '../../data/mpa_vJan21_CHOCOPhlAnSGB_202103_species.txt'
df = pd.read_csv(path, sep="\t", header=None, names=["SGB", "taxonomy"], dtype=str)

# Function to extract taxonomy ranks
def split_taxonomy(taxonomy):
    ranks = {"kingdom": pd.NA, "phylum": pd.NA, "class": pd.NA, "order": pd.NA,
             "family": pd.NA, "genus": pd.NA, "species": pd.NA}
    if pd.isna(taxonomy):
        return pd.Series(ranks)
    
    # Split by '|'
    parts = taxonomy.split("|")
    for part in parts:
        if part.startswith("k__"): ranks["kingdom"] = part[3:] or pd.NA
        elif part.startswith("p__"): ranks["phylum"] = part[3:] or pd.NA
        elif part.startswith("c__"): ranks["class"] = part[3:] or pd.NA
        elif part.startswith("o__"): ranks["order"] = part[3:] or pd.NA
        elif part.startswith("f__"): ranks["family"] = part[3:] or pd.NA
        elif part.startswith("g__"): ranks["genus"] = part[3:] or pd.NA
        elif part.startswith("s__"): ranks["species"] = part[3:] or pd.NA
    return pd.Series(ranks)

# Apply function
tax_df = df["taxonomy"].apply(split_taxonomy)

# Combine with original
df_tax_split = pd.concat([df, tax_df], axis=1)

# Optional: filter only GGB species
ggb_df = df_tax_split[df_tax_split["species"].str.contains(r"GGB\d+", na=False)].copy()

# Save
ggb_df.to_csv("GGB_species_split_taxonomy.tsv", sep="\t", index=False)

# Preview
print(ggb_df.head(10))