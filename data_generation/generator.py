import random
from typing import Iterator, Optional

from faker import Faker

from data_generation.models import Customer, RiskTier

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