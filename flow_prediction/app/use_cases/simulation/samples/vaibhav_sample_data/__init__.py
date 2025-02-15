from copy import deepcopy

from ..helpers import getExpenseIdx
from ...init_data import (
    CashflowSimulationUseCaseInitData,
)

PARTNER_MONTHLY_SALARY = 74_500
HOUSE_MONTHLY_RENT = 58_000 + 1000 + 4000  # rent + water + electricity
CHEAP_HOUSE_MONTHLY_RENT = 30_000 + 1000 + 1000  # rent + water + electricity
MY_MONTHLY_SALARY = 1_32_000
MY_SALARY_GROWTH_RATE = 0.10
MARRIAGE_COST = 20_00_000
# MARRIAGE_COST = 5_00_000
PARTNER_PF_CONTRIBUTION = (
    PARTNER_MONTHLY_SALARY * 0.5 * 0.24
)  # assuming 50% of in hand is basic, not considering tax as tax on first 12.5 lakh is exempt.
# 24% assuming 12% matching from employer
RETIREMENT_YEAR = 2061
PARENTS_SUPPORT_END_YEAR = 2040
vaibhav_sample_data: CashflowSimulationUseCaseInitData = {
    "expenses": [
        {
            "id": "car",
            "startYear": 2028,
            "endYear": 2055,
            "enabled": True,
            "growthRate": 0.05,
            "initialValue": {
                "amount": 10_00_000,
                "referenceTime": 2025,
            },
            # "group": "car",
            "recurringValue": {"amount": 10_000 * 12, "referenceTime": 2025},
            "fundingCorpora": [
                {
                    "id": "microsoft-stock",
                }
            ],
        },
        {
            "id": "marriage",
            "startYear": 2028,
            "endYear": 2028,
            "enabled": False,
            "growthRate": 0.09,
            "initialValue": {
                "amount": MARRIAGE_COST,
                "referenceTime": 2025,
            },
            "group": "marriage",
            "recurringValue": {"amount": 0, "referenceTime": 2025},
            "fundingCorpora": [
                {
                    "id": "microsoft-stock",
                }
            ],
        },
        {
            "id": "my food",
            "startYear": 2025,
            "endYear": 2100,
            "enabled": True,
            "growthRate": 0.09,
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "savings-bank",
                },
                {
                    "id": "retirement-swp-fund",
                    "startYear": 2062,
                },
            ],
            "recurringValue": {
                "amount": 500 * 30 * 12,
                "referenceTime": 2025,
            },
        },
        {
            "id": "misc",
            "startYear": 2025,
            "endYear": 2100,
            "enabled": True,
            "growthRate": 0.09,
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "savings-bank",
                },
                {
                    "id": "retirement-swp-fund",
                    "startYear": 2062,
                },
            ],
            "recurringValue": {
                "amount": 10_000 * 12,
                "referenceTime": 2025,
            },
        },
        {
            "id": "partner-expenses",
            "startYear": 2029,
            "endYear": 2100,
            "enabled": True,
            "growthRate": 0.09,
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "savings-bank",
                },
                {
                    "id": "retirement-swp-fund",
                    "startYear": 2062,
                },
            ],
            "recurringValue": {
                "amount": 20_000 * 12,
                "referenceTime": 2025,
            },
        },
        {
            "id": "travel",
            "startYear": 2025,
            "endYear": 2081,
            "enabled": True,
            "growthRate": 0.09,
            "fundingCorpora": [
                {
                    "id": "savings-bank",
                },
                {"id": "retirement-swp-fund", "startYear": 2062},
            ],
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": 20_000 * 12,
                "referenceTime": 2025,
            },
        },
        {
            "id": "life-insurance",
            "startYear": 2025,
            "endYear": RETIREMENT_YEAR,
            "enabled": True,
            "growthRate": 0.00,
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": 35_344,
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "life-insurance-arbitrage-fund",
                }
            ],
        },
        {
            "id": "health-insurance",
            "startYear": 2025,
            "endYear": 2100,
            "enabled": True,
            "growthRate": 0.13,
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": 15_448,
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "health-insurance-large-cap-mutual-fund",  # assuming bulk pre-payment for 3-5 years always
                },
                {
                    "id": "retirement-swp-fund",
                    "startYear": 2062,
                },
            ],
        },
        {
            "id": "cheaper-house-rent",
            "startYear": 2026,
            "endYear": 2028,
            "enabled": True,  # True,
            "growthRate": 0.10,
            "initialValue": {
                "amount": CHEAP_HOUSE_MONTHLY_RENT * 2,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": CHEAP_HOUSE_MONTHLY_RENT * 12,
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "savings-bank",
                },
                {
                    "id": "retirement-swp-fund",
                    "startYear": 2062,
                },
            ],
        },
        {
            "id": "comfy-house-rent",
            "startYear": 2029,
            "endYear": 2091,
            "enabled": True,
            "growthRate": 0.10,
            "initialValue": {
                "amount": HOUSE_MONTHLY_RENT * 2,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": HOUSE_MONTHLY_RENT * 12,
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "savings-bank",
                },
                {
                    "id": "retirement-swp-fund",
                    "startYear": 2062,
                },
            ],
        },
        {
            "id": "parents",
            "startYear": 2025,
            "endYear": PARENTS_SUPPORT_END_YEAR,
            "enabled": True,
            "growthRate": 0.09,
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": 35_000 * 12,
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "savings-bank",
                }
            ],
        },
        {
            "id": "bills",
            "startYear": 2025,
            "endYear": 2100,
            "enabled": True,
            "growthRate": 0.09,
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": (700 + 3 * (3000 / 12))
                * 12,  # internet, phones, ott, electricity+water
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "savings-bank",
                },
                {
                    "id": "retirement-swp-fund",
                    "startYear": 2062,
                },
            ],
        },
        {
            "id": "commute",
            "startYear": 2025,
            "endYear": 2100,
            "enabled": True,
            "growthRate": 0.09,
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": 3000 * 12,
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "savings-bank",
                },
                {
                    "id": "retirement-swp-fund",
                    "startYear": 2062,
                },
            ],
        },
        {
            "id": "house-help",
            "startYear": 2026,
            "endYear": 2100,
            "enabled": True,
            "growthRate": 0.09,
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": 10_000 * 12,  # cook + maid
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "savings-bank",
                },
                {
                    "id": "retirement-swp-fund",
                    "startYear": 2062,
                },
            ],
        },
        {
            "id": "my-device-upgrades",
            "startYear": 2025,
            "endYear": 2100,
            "enabled": True,
            "growthRate": 0.10,
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": 80_000,
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "device-upgrade-large-cap-mutual-fund",
                },
                {"id": "retirement-swp-fund", "startYear": 2062},
            ],
        },
        {
            "id": "partner-device-upgrades",
            "startYear": 2029,
            "endYear": 2100,
            "enabled": True,
            "growthRate": 0.10,
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": 32_000,
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "device-upgrade-large-cap-mutual-fund",
                },
                {"id": "retirement-swp-fund", "startYear": 2062},
            ],
        },
        {
            "id": "partner-health-insurance",
            "startYear": 2029,
            "endYear": 2100,
            "enabled": True,
            "growthRate": 0.13,
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": 15_448,
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "health-insurance-large-cap-mutual-fund",  # assuming bulk pre-payment for 3-5 years always
                },
                {
                    "id": "retirement-swp-fund",
                    "startYear": 2062,
                },
            ],
        },
        {
            "id": "partner-life-insurance",
            "startYear": 2029,
            "endYear": RETIREMENT_YEAR,
            "enabled": True,
            "growthRate": 0.00,
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": 0.25 * PARTNER_MONTHLY_SALARY,
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "life-insurance-arbitrage-fund",
                }
            ],
        },
        {
            "id": "kid-1",
            "startYear": 2032,
            "endYear": 2055,
            "enabled": False,
            "growthRate": 0.09,
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": 50_000 * 12,
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "savings-bank",
                }
            ],
        },
        {
            "id": "kid-2",
            "startYear": 2038,
            "endYear": 2061,
            "enabled": False,
            "growthRate": 0.09,
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": 50_000 * 12,
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "savings-bank",
                }
            ],
        },
    ],
    "corpora": [
        {
            "id": "savings-bank",
            "growthRate": 0.03,
            "startYear": 2025,
            "endYear": 2100,
            "initialAmount": 1_50_000,
        },
        {
            "id": "retirement-swp-fund",
            "growthRate": 0.12,
            "startYear": RETIREMENT_YEAR,
            "endYear": 2100,
            "initialAmount": 0,
        },
        {
            "id": "marriage-large-mid-cap-mutual-fund",
            "growthRate": 0.11,
            "startYear": 2025,
            "endYear": 2028,
            "initialAmount": 1_02_242,
            "successorCorpusId": "retirement-small-cap-mutual-fund",
        },
        {
            "id": "retirement-epf",
            "growthRate": 0.08,
            "startYear": 2025,
            "initialAmount": 127241.28,
            "endYear": RETIREMENT_YEAR,
        },
        {
            "id": "health-insurance-large-cap-mutual-fund",
            "growthRate": 0.10,
            "startYear": 2025,
            "initialAmount": 0,
            "endYear": RETIREMENT_YEAR,
        },
        {
            "id": "retirement-small-cap-mutual-fund",
            "growthRate": 0.15,
            "startYear": 2025,
            "initialAmount": 0,
            "endYear": RETIREMENT_YEAR,
        },
        {
            "id": "mirae-asset-elss-tax-saver-fund",
            "growthRate": 0.1951,
            "startYear": 2025,
            "initialAmount": 10_326,
            "endYear": 2028,
            "successorCorpusId": "retirement-small-cap-mutual-fund",
        },
        {
            "id": "life-insurance-arbitrage-fund",
            "growthRate": 0.06,
            "startYear": 2025,
            "initialAmount": 0,
            "endYear": RETIREMENT_YEAR,
        },
        {
            "id": "microsoft-stock",
            "growthRate": 0.1694,
            "startYear": 2025,
            "initialAmount": 11_62_006 + 5_29_048.012,
            "endYear": RETIREMENT_YEAR,
        },
        {
            "id": "device-upgrade-large-cap-mutual-fund",
            "growthRate": 0.10,
            "startYear": 2025,
            "initialAmount": 0,
            "endYear": 2100,
        },
    ],
    "cashflows": [
        {
            "id": "my-salary",
            "recurringValue": {
                "amount": MY_MONTHLY_SALARY * 12,
                "referenceTime": 2025,
                "growthRate": MY_SALARY_GROWTH_RATE,
            },
            "enabled": True,
            "startYear": 2025,
            "endYear": RETIREMENT_YEAR,
            "allocations": [
                {
                    "startYear": 2025,
                    "endYear": 2028,
                    "split": [
                        {
                            "corpusId": "savings-bank",
                            "ratio": 0.91,  # 0.53 -> 12 points left
                        },
                        {
                            "corpusId": "device-upgrade-large-cap-mutual-fund",
                            "ratio": 0.051,
                        },
                        {
                            "corpusId": "health-insurance-large-cap-mutual-fund",
                            "ratio": 0.012,
                        },
                        {
                            "corpusId": "marriage-large-mid-cap-mutual-fund",
                            "ratio": 0.0,
                        },
                        {
                            "corpusId": "life-insurance-arbitrage-fund",
                            "ratio": 0.023,
                        },
                        {
                            "corpusId": "retirement-small-cap-mutual-fund",
                            "ratio": 0.004,
                        },
                    ],
                },
                {
                    "startYear": 2029,
                    "endYear": PARENTS_SUPPORT_END_YEAR,
                    "split": [
                        {"corpusId": "savings-bank", "ratio": 0.87},
                        {
                            "corpusId": "health-insurance-large-cap-mutual-fund",
                            "ratio": 0.03,
                        },
                        {
                            "corpusId": "retirement-small-cap-mutual-fund",
                            "ratio": 0.00,
                        },
                        {
                            "corpusId": "life-insurance-arbitrage-fund",
                            "ratio": 0.02,
                        },
                        {
                            "corpusId": "device-upgrade-large-cap-mutual-fund",
                            "ratio": 0.08,
                        },
                    ],
                },
                {
                    "startYear": PARENTS_SUPPORT_END_YEAR + 1,
                    "endYear": 2100,
                    "split": [
                        {"corpusId": "savings-bank", "ratio": 0.525},
                        {
                            "corpusId": "health-insurance-large-cap-mutual-fund",
                            "ratio": 0.05,
                        },
                        {
                            "corpusId": "retirement-small-cap-mutual-fund",
                            "ratio": 0.32,
                        },
                        {
                            "corpusId": "life-insurance-arbitrage-fund",
                            "ratio": 0.015,
                        },
                        {
                            "corpusId": "device-upgrade-large-cap-mutual-fund",
                            "ratio": 0.09,
                        },
                    ],
                },
            ],
            "expandedDescription": "my income",
        },
        {
            "id": "my-epf",
            "recurringValue": {
                "amount": 9_818 * 12,
                "referenceTime": 2025,
                "growthRate": MY_SALARY_GROWTH_RATE,
            },
            "enabled": True,
            "startYear": 2025,
            "endYear": RETIREMENT_YEAR,
            "allocations": [
                {
                    "startYear": 2025,
                    "endYear": RETIREMENT_YEAR,
                    "split": [{"corpusId": "retirement-epf", "ratio": 1}],
                }
            ],
            "expandedDescription": "my epf",
        },
        {
            "id": "microsoft-stock-credit",
            "recurringValue": {
                "amount": 59_151 * 12,
                "referenceTime": 2025,
                "growthRate": 0.10,
            },
            "enabled": True,
            "startYear": 2025,
            "endYear": 2026,
            "allocations": [
                {
                    "startYear": 2025,
                    "endYear": 2026,
                    "split": [{"corpusId": "microsoft-stock", "ratio": 1}],
                }
            ],
            "expandedDescription": "microsoft stock credit",
        },
        {
            "id": "wife-income",
            "recurringValue": {
                "amount": PARTNER_MONTHLY_SALARY * 12,
                "referenceTime": 2025,
                "growthRate": 0.10,
            },
            "enabled": True,
            "startYear": 2029,
            "endYear": RETIREMENT_YEAR,
            "allocations": [
                {
                    "startYear": 2029,
                    "endYear": 2100,
                    "split": [{"corpusId": "savings-bank", "ratio": 1}],
                }
            ],
            "expandedDescription": "income from wife's salary",
        },
        {
            "id": "partner-epf",
            "recurringValue": {
                "amount": PARTNER_PF_CONTRIBUTION * 12,
                "referenceTime": 2025,
                "growthRate": 0.10,
            },
            "enabled": True,
            "startYear": 2029,
            "endYear": RETIREMENT_YEAR,
            "allocations": [
                {
                    "startYear": 2029,
                    "endYear": RETIREMENT_YEAR,
                    "split": [{"corpusId": "retirement-epf", "ratio": 1}],
                }
            ],
            "expandedDescription": "partner's epf",
        },
    ],
    "simulation": {
        "startYear": 2025,
        "endYear": 2091,  # PARENTS_SUPPORT_END_YEAR + 10,
    },
    "currency": "INR",
    "fallbackCorpusId": "retirement-swp-fund",
    "baseInflation": 0.09,
}

no_marriage_cost = deepcopy(vaibhav_sample_data)
no_marriage_cost["expenses"][getExpenseIdx(no_marriage_cost, "marriage")][
    "enabled"
] = False
