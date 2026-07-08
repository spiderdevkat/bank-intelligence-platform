from data_generation.generator import generate_customers, generate_accounts, generate_normal_transactions
from data_generation.fraud_patterns import inject_velocity_fraud, inject_structuring, inject_round_tripping


def _make_accounts(n_customers=20):
    customers = list(generate_customers(n_customers, seed=1))
    accounts = list(generate_accounts(customers))
    return customers, accounts


def test_generate_customers_count_and_uniqueness():
    customers = list(generate_customers(50, seed=1))
    assert len(customers) == 50
    assert len({c.customer_id for c in customers}) == 50


def test_normal_transactions_are_not_fraud():
    _, accounts = _make_accounts()
    txns = list(generate_normal_transactions(accounts, 100))
    assert len(txns) == 100
    assert all(t.is_fraud is False for t in txns)


def test_velocity_fraud_burst_stays_within_window():
    _, accounts = _make_accounts()
    txns = list(inject_velocity_fraud(accounts, num_incidents=1, txns_per_incident=(10, 10), window_minutes=10))
    timestamps = sorted(t.transaction_timestamp for t in txns)
    span_seconds = (timestamps[-1] - timestamps[0]).total_seconds()
    assert span_seconds <= 600


def test_structuring_amounts_stay_under_threshold():
    _, accounts = _make_accounts()
    threshold = 10_000.0
    txns = list(inject_structuring(accounts, num_incidents=3, reporting_threshold=threshold))
    assert all(t.amount < threshold for t in txns)


def test_round_tripping_forms_a_closed_loop():
    _, accounts = _make_accounts(n_customers=10)
    txns = list(inject_round_tripping(accounts, num_incidents=1, ring_size=(4, 4)))
    sources = [t.account_id for t in txns]
    destinations = [t.counterparty_account_id for t in txns]
    assert destinations == sources[1:] + [sources[0]]