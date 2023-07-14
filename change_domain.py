import os
import sys
import pandas as pd

def copy_and_change_emails(file_column_pairs, suffix, domain):
    for file_column_pair in file_column_pairs:
        csv_file, cols = file_column_pair.split(':')
        cols = cols.split(',')

        # Creating copy
        new_csv_file = csv_file.rsplit('.', 1)[0] + '_' + suffix + '.csv'
        os.system('copy {} {}'.format(csv_file, new_csv_file))

        # Changing domain of emails
        df = pd.read_csv(new_csv_file)
        for col in cols:
            if col in df.columns:
                df[col] = df[col].str.replace(r'@[\w\.-]+', '@'+domain, regex=True)
        df.to_csv(new_csv_file, index=False)

if __name__ == "__main__":
    file_column_pairs = sys.argv[1].split(';')
    suffix = sys.argv[2]
    domain = sys.argv[3]
    copy_and_change_emails(file_column_pairs, suffix, domain)
