import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data_generation.generator import generate_customers, generate_accounts, generate_normal_transactions
from data_generation.fraud_patterns import inject_velocity_fraud, inject_structuring, inject_round_tripping


def parse_args():
    parser = argparse.ArgumentParser(description="Generate synthetic banking data.")
    parser.add_argument("--customers", type=int, default=300)
    parser.add_argument("--normal-txns", type=int, default=3000)
    parser.add_argument("--velocity-incidents", type=int, default=5)
    parser.add_argument("--structuring-incidents", type=int, default=3)
    parser.add_argument("--round-trip-incidents", type=int, default=2)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main():
    args = parse_args()

    print(f"Generating {args.customers} customers...")
    customers = list(generate_customers(args.customers, seed=args.seed))

    print("Generating accounts...")
    accounts = list(generate_accounts(customers))
    print(f"  -> {len(accounts)} accounts")

    print(f"Generating {args.normal_txns} normal transactions...")
    normal_txns = list(generate_normal_transactions(accounts, args.normal_txns))

    print("Injecting fraud patterns...")
    velocity_txns = list(inject_velocity_fraud(accounts, args.velocity_incidents))
    structuring_txns = list(inject_structuring(accounts, args.structuring_incidents))
    round_trip_txns = list(inject_round_tripping(accounts, args.round_trip_incidents))

    all_txns = normal_txns + velocity_txns + structuring_txns + round_trip_txns
    fraud_count = len(velocity_txns) + len(structuring_txns) + len(round_trip_txns)

    print("\n--- Summary ---")
    print(f"Customers:           {len(customers)}")
    print(f"Accounts:            {len(accounts)}")
    print(f"Normal transactions: {len(normal_txns)}")
    print(f"Velocity fraud:      {len(velocity_txns)}")
    print(f"Structuring:         {len(structuring_txns)}")
    print(f"Round-tripping:      {len(round_trip_txns)}")
    print(f"Total transactions:  {len(all_txns)} (fraud rate: {fraud_count/len(all_txns):.2%})")


if __name__ == "__main__":
    main()