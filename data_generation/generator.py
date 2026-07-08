import random
from typing import Iterator, Optional

from faker import Faker

from data_generation.models import Customer, RiskTier, Account, AccountStatus, AccountType

from datetime import datetime, timedelta

from data_generation.models import Transaction, TransactionChannel, TransactionType

_fake = Faker()

COUNTRIES = ["US", "GB", "DE", "IN", "SG", "AE"]

RISK_TIER_WEIGHTS = {RiskTier.LOW: 0.75, RiskTier.MEDIUM: 0.20, RiskTier.HIGH: 0.05}


def _weighted_risk_tier() -> RiskTier:
    population = list(RISK_TIER_WEIGHTS.keys())
    weights = list(RISK_TIER_WEIGHTS.values())
    return random.choices(population, weights=weights, k=1)[0]


def generate_customers(n: int, seed: Optional[int] = None) -> Iterator[Customer]:
    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)

    for _ in range(n):
        yield Customer.new(
            full_name=_fake.name(),
            email=_fake.unique.email(),
            phone=_fake.phone_number(),
            country=random.choice(COUNTRIES),
            risk_tier=_weighted_risk_tier(),
            created_at=_fake.date_time_between(start_date="-5y", end_date="-30d"),
        )

CURRENCIES = ["USD", "EUR", "GBP", "INR"]


def generate_accounts(customers, accounts_per_customer=(1, 2)):
    all_account_ids = []

    for customer in customers:
        num_accounts = random.randint(*accounts_per_customer)
        for _ in range(num_accounts):
            account_type = random.choice(list(AccountType))

            parent_id = None
            if account_type == AccountType.BUSINESS and all_account_ids and random.random() < 0.3:
                parent_id = random.choice(all_account_ids)

            account = Account.new(
                customer_id=customer.customer_id,
                parent_account_id=parent_id,
                account_number=_fake.unique.bothify(text="ACCT-########"),
                account_type=account_type,
                currency=random.choice(CURRENCIES),
                status=AccountStatus.ACTIVE,
                opened_at=_fake.date_time_between(start_date=customer.created_at, end_date="-1d"),
            )
            all_account_ids.append(account.account_id)
            yield account


def generate_normal_transactions(accounts, n, start_date=None, end_date=None):
    start_date = start_date or datetime.now() - timedelta(days=180)
    end_date = end_date or datetime.now()
    span_seconds = int((end_date - start_date).total_seconds())

    for _ in range(n):
        account = random.choice(accounts)
        counterparty = random.choice(accounts)
        ts = start_date + timedelta(seconds=random.randint(0, span_seconds))
        amount = round(random.lognormvariate(mu=4.0, sigma=1.1), 2)

        yield Transaction.new(
            customer_id=account.customer_id,
            account_id=account.account_id,
            counterparty_account_id=(
                counterparty.account_id if counterparty.account_id != account.account_id else None
            ),
            transaction_type=random.choice(list(TransactionType)),
            channel=random.choice(list(TransactionChannel)),
            amount=amount,
            currency=account.currency,
            transaction_timestamp=ts,
            is_fraud=False,
            fraud_label=None,
        )