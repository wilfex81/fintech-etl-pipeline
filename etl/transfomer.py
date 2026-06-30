from datetime import datetime, timedelta

def convert_time(utc_string):
    # Parse the UTC string into a datetime object
    dt = datetime.strptime(utc_string, "%Y-%m-%d %H:%M:%S UTC")

    # Subtract 3 hours to convert UTC to São Paulo (UTC-3)
    dt_sp = dt - timedelta(hours=3)

    # Return only the date formatted as DD/MM/YYYY
    return dt_sp.strftime("%d/%m/%Y")

def transform(records):
    # Three buckets: One per output csv
    transactions_records = []
    account_summary_snapshots_records = []
    category_spend_records = []
    
    for record in records:
        event = record['EventType']
        payload = record['Payload']
        enqueued_time = convert_time(record['EventTimestampUtc'])

        # Route each record to the appropriate bucket based on the event type
        if event == 'TransactionCompleted':
            for category in payload['categories']:
                transactions_records.append({
                    'TransactionId': payload['transactionId'],
                    'AccountId': payload['accountId'],
                    'Amount': payload['amount'],
                    'Currency': payload['currency'],
                    'Channel': payload['channel'],
                    'Status': payload['status'],
                    'Reference': payload['reference'],

                    'categoryId': category['categoryId'],
                    'categoryName': category['categoryName'],
                    'Transport': category['Transport'],
                    'Amount': category['amount'],
                    'Percentage': category['percentage'],
                    'EnqueuedTimeUtc': enqueued_time
                })
        elif event == 'AccountSnapshot':
            metrics = payload['metrics']
            account_summary_snapshots_records.append({
                'AccountId': payload['accountId'],
                'AccountType': payload['accountType'],
                'Balance': payload['balance'],
                'Currency': payload['currency'],
                'isActive': payload['isActive'],
                'EnqueuedTimeUtc': enqueued_time,

                'TotalDeposits': metrics['totalDeposits'],
                'TotalWithdrawals': metrics['totalWithdrawals'],
                'TransactionCount': metrics['transactionCount']
            })
        elif event == 'CategorySpend':
            breakdown = payload['breakdown']
            category_spend_records.append({
                'AccountId': payload['accountId'],
                'PeriodStart': payload['periodStart'],
                'PeriodEnd': payload['periodEnd'],
                'TotalSpend': payload['totalSpend'],
                'Currency': payload['currency'],
                'CategoryId': breakdown['categoryId'],
                'CategoryName': breakdown['categoryName'],
                'Amount': breakdown['amount'],
                'TransactionCount': breakdown['transactionCount'],
                'isOverBudget': breakdown['isOverBudget'],
                'EnqueuedTimeUtc': enqueued_time
            })

    return transactions_records, account_summary_snapshots_records, category_spend_records

