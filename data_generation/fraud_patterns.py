import random
from datetime import datetime, timedelta

from data_generation.models import FraudLabel, Transaction, TransactionChannel, TransactionType


def inject_velocity_fraud(accounts, num_incidents, txns_per_incident=(8, 20), window_minutes=10):
    for _ in range(num_incidents):
        account = random.choice(accounts)
        burst_start = datetime.now() - timedelta(
            days=random.randint(1, 180), minutes=random.randint(0, 1440)
        )
        n_txns = random.randint(*txns_per_incident)

        for _i in range(n_txns):
            ts = burst_start + timedelta(seconds=random.randint(0, window_minutes * 60))
            yield Transaction.new(
                customer_id=account.customer_id,
                account_id=account.account_id,
                counterparty_account_id=None,
                transaction_type=TransactionType.WITHDRAWAL,
                channel=random.choice([TransactionChannel.ATM, TransactionChannel.CARD]),
                amount=round(random.uniform(50, 500), 2),
                currency=account.currency,
                transaction_timestamp=ts,
                is_fraud=True,
                fraud_label=FraudLabel.VELOCITY,
            )

def inject_structuring(accounts, num_incidents, reporting_threshold=10_000.0, txns_per_incident=(4, 8)):
    for _ in range(num_incidents):
        account = random.choice(accounts)
        start_day = datetime.now() - timedelta(days=random.randint(30, 300))
        n_txns = random.randint(*txns_per_incident)

        for day_offset in range(n_txns):
            ts = start_day + timedelta(
                days=day_offset, hours=random.randint(9, 17), minutes=random.randint(0, 59)
            )
            amount = round(reporting_threshold * random.uniform(0.85, 0.99), 2)

            yield Transaction.new(
                customer_id=account.customer_id,
                account_id=account.account_id,
                counterparty_account_id=None,
                transaction_type=TransactionType.DEPOSIT,
                channel=TransactionChannel.BRANCH,
                amount=amount,
                currency=account.currency,
                transaction_timestamp=ts,
                is_fraud=True,
                fraud_label=FraudLabel.STRUCTURING,
            )

def inject_round_tripping(accounts, num_incidents, ring_size=(3, 5)):
    for _ in range(num_incidents):
        size = random.randint(*ring_size)
        ring = random.sample(accounts, k=min(size, len(accounts)))
        if len(ring) < 2:
            continue

        amount = round(random.uniform(5_000, 50_000), 2)
        start_ts = datetime.now() - timedelta(days=random.randint(1, 300))

        for step in range(len(ring)):
            source = ring[step]
            destination = ring[(step + 1) % len(ring)]
            ts = start_ts + timedelta(hours=step * random.randint(1, 6))
            hop_amount = round(amount * (0.97 ** step), 2)

            yield Transaction.new(
                customer_id=source.customer_id,
                account_id=source.account_id,
                counterparty_account_id=destination.account_id,
                transaction_type=TransactionType.TRANSFER,
                channel=TransactionChannel.WIRE,
                amount=hop_amount,
                currency=source.currency,
                transaction_timestamp=ts,
                is_fraud=True,
                fraud_label=FraudLabel.ROUND_TRIPPING,
            )