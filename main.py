from etl.extractor import extract_payload
from etl.transfomer import transform
from etl.loader import write_csv


def main():
    # Step 1: Extract
    records = extract_payload('data/transactions.json')

    # Step 2: Transform
    transactions_records, account_summary_snapshots_records, category_spend_records = transform(records)

    # Step 3: Load
    write_csv('data/transactions.csv', transactions_records)
    write_csv('data/account_summary_snapshots.csv', account_summary_snapshots_records)
    write_csv('data/category_spend.csv', category_spend_records)

if __name__ == "__main__":
    main()