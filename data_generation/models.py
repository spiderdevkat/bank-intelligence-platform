import uuid
from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from enum import Enum


class RiskTier(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class AccountType(str, Enum):
    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"
    BUSINESS = "BUSINESS"


class AccountStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DORMANT = "DORMANT"
    CLOSED = "CLOSED"


class TransactionChannel(str, Enum):
    ATM = "ATM"
    ONLINE = "ONLINE"
    BRANCH = "BRANCH"
    WIRE = "WIRE"
    CARD = "CARD"


class TransactionType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER = "TRANSFER"
    PAYMENT = "PAYMENT"


class FraudLabel(str, Enum):
    VELOCITY = "VELOCITY"
    STRUCTURING = "STRUCTURING"
    ROUND_TRIPPING = "ROUND_TRIPPING"

@dataclass
class Customer:
    customer_id: str
    full_name: str
    email: str
    phone: Optional[str]
    country: str
    risk_tier: RiskTier
    created_at: datetime

    @classmethod
    def new(cls, **kwargs) -> "Customer":
        return cls(customer_id=str(uuid.uuid4()), **kwargs)

@dataclass
class Account:
    account_id: str
    customer_id: str
    parent_account_id: Optional[str]
    account_number: str
    account_type: AccountType
    currency: str
    status: AccountStatus
    opened_at: datetime

    @classmethod
    def new(cls, **kwargs) -> "Account":
        return cls(account_id=str(uuid.uuid4()), **kwargs)


@dataclass
class Transaction:
    transaction_id: str
    customer_id: str
    account_id: str
    counterparty_account_id: Optional[str]
    transaction_type: TransactionType
    channel: TransactionChannel
    amount: float
    currency: str
    transaction_timestamp: datetime
    is_fraud: bool = False
    fraud_label: Optional[FraudLabel] = None

    @classmethod
    def new(cls, **kwargs) -> "Transaction":
        return cls(transaction_id=str(uuid.uuid4()), **kwargs)