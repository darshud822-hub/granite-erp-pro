from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    SALES = "SALES"
    PRODUCTION = "PRODUCTION"
    PURCHASE = "PURCHASE"
    ACCOUNTANT = "ACCOUNTANT"