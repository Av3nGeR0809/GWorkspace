import pandas as pd
import sys
import os

def change_email_domain(csv_path, column, new_domain):
    print(f"Processing file: '{csv_path}' with column: '{column}'")

    if not os.path.exists(csv_path):
        print(f"No such file: '{csv_path}'")
        return

    try:
        # Load the CSV data
        df = pd.read_csv(csv_path, encoding='utf-8')
    except pd.errors.EmptyDataError:
        print(f"The file '{csv_path}' is empty or does not contain valid CSV data.")
        return
    except Exception as e:
        print(f"An error occurred while reading '{csv_path}': {e}")
        return

    column = column.strip()
    
    if column not in df.columns:
        print(f"No '{column}' column in the CSV file '{csv_path}'.")
        return

    # Check how many email addresses are going to be changed
    print(f"Changing domain for {df[column].count()} email addresses...")

    # Change domain of the emails in the specified column
    df[column] = df[column].apply(lambda email: change_domain(email.strip(), new_domain))

    new_csv_path = csv_path.replace(".csv", "_new.csv")
    try:
        # Save the DataFrame to the new CSV file
        df.to_csv(new_csv_path, index=False, encoding='utf-8')
        print(f"Domain changed successfully in column '{column}' of file '{new_csv_path}'")
    except Exception as e:
        print(f"An error occurred while writing to '{new_csv_path}': {e}")


def change_domain(email, new_domain):
    try:
        username, _ = email.split('@')
    except ValueError:
        print(f"Invalid email address encountered: {email}")
        return email
    return f"{username}@{new_domain}"


if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) % 2 != 0:
        print("Usage: python script.py <new domain> <CSV file path 1> <column name 1> <CSV file path 2> <column name 2> ...")
        sys.exit()

    domain_name = sys.argv[1]
    pairs = zip(sys.argv[2::2], sys.argv[3::2])

    for csv_file_path, column_name in pairs:
        change_email_domain(csv_file_path, column_name.strip(), domain_name)
