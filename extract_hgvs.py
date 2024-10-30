import csv
import re
import sys

# regular expression to extract fields from hgvs names:
# example: NC_000003.12:g.183917980C>T
pattern = r"NC_0+(\d+)\.\d+:\w\.(\d+)([A-Z])>([A-Z])"

def process_file(input_file, output_file="parsed_variants.tsv"):
    # Open input and output files
    with open(input_file) as conn, open(output_file, "w", newline="") as out_conn:
        reader = csv.reader(conn, delimiter="\t", quotechar='"')
        writer = csv.writer(out_conn, delimiter="\t")

        # Write header row to the output file
        writer.writerow(["plink_format", "hgvs_format", "chr_pos", "chr", "pos", "ref", "alt"])

        # Process each row in the input file
        for row in reader:
            location = row[4]
            location_ref = location.split(sep=":")[0]
            synonym_list = row[10].split(sep=", ")

            for synonym in synonym_list:
                # Only process synonyms that start with the location reference and contain '>'
                if synonym.startswith(location_ref) and ">" in synonym:
                    match = re.search(pattern, synonym)
                    if match:
                        chro = match.group(1)
                        pos = match.group(2)
                        ref = match.group(3)
                        alt = match.group(4)

                        # Format the output fields
                        plink_format = f"chr{chro}:{pos}:{ref}:{alt}"
                        chr_pos = f"{location_ref}:{pos}"

                        # Write the row to the output file
                        writer.writerow([plink_format, synonym, chr_pos, chro, pos, ref, alt])

if __name__ == "__main__":
    # Use the first command-line argument as the input file name
    if len(sys.argv) < 2:
        print("no input file in entered")
        print("please use: python extract_hgvs.py <input_file>")
    else:
        input_file = sys.argv[1]
        process_file(input_file)