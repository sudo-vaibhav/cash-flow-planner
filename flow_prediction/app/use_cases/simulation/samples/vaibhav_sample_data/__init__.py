from gc import enable

from ...init_data import (
    CashflowSimulationUseCaseInitData,
)

vaibhav_sample_data: CashflowSimulationUseCaseInitData = {
    "expenses": [
        {
            "id": "marriage",
            "startYear": 2028,
            "endYear": 2028,
            "enabled": True,
            "growthRate": 0.09,
            "initialValue": {
                "amount": 30_00_000,
                "referenceTime": 2025,
            },
            "recurringValue": {"amount": 0, "referenceTime": 2025},
            "fundingCorpora": [
                {
                    "id": "marriage-large-mid-cap-mutual-fund",
                }
            ],
        },
        {
            "id": "travel",
            "startYear": 2025,
            "endYear": 2100,
            "enabled": True,
            "growthRate": 0.09,
            "fundingCorpora": [
                {
                    "id": "arbitrage-fund",
                },
                {
                    "id": "savings-bank",
                },
            ],
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": 3_60_000,
                "referenceTime": 2025,
            },
        },
        {
            "id": "life-insurance",
            "startYear": 2025,
            "endYear": 2061,
            "enabled": False,
            "growthRate": 0.00,
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": 36_000,
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "arbitrage-fund",
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
                }
            ],
        },
        {
            "id": "retirement",
            "startYear": 2061,
            "endYear": 2091,
            "enabled": False,
            "growthRate": 0.09,
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": 1_50_000 * 12,
                "referenceTime": 2025,
            }
        },
        {
            "id": "rent",
            "startYear": 2028,
            "endYear": 2091,
            "enabled": True,
            "growthRate": 0.10,
            "initialValue": {
                "amount": 58_000 * 2,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": 58_000 * 12,
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "savings-bank",
                }
            ],
        },
        {
            "id": "parents",
            "startYear": 2025,
            "endYear": 2035,
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
            "id": "kid-1",
            "startYear": 2032,
            "endYear": 2055,
            "enabled": True,
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
            "startYear": 2026,
            "endYear": 2030,
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
            "initialAmount": 1_50_000
        },
        {
            "id": "marriage-large-mid-cap-mutual-fund",
            "growthRate": 0.11,
            "startYear": 2025,
            "endYear": 2100,
            "initialAmount": 0
        },
        {
            "id": "epf",
            "growthRate": 0.08,
            "startYear": 2025,
            "initialAmount": 0,
            "endYear": 2061,
        },
        {
            "id": "health-insurance-large-cap-mutual-fund",
            "growthRate": 0.10,
            "startYear": 2025,
            "initialAmount": 0,
            "endYear": 2100,
        },
        {
            "id": "small-cap-mutual-fund",
            "growthRate": 0.15,
            "startYear": 2025,
            "initialAmount": 0,
            "endYear": 2100,
        },
        {
            "id": "medium-large-cap-mutual-fund",
            "growthRate": 0.13,
            "startYear": 2025,
            "initialAmount": 0,
            "endYear": 2100,
        },
        {
            "id": "mirae-asset-elss-tax-saver-fund",
            "growthRate": 0.1951,
            "startYear": 2025,
            "initialAmount": 10_326,
            "endYear": 2100,
        },
        {
            "id": "arbitrage-fund",
            "growthRate": 0.06,
            "startYear": 2025,
            "initialAmount": 0,
            "endYear": 2100,
        },
        {
            "id":"microsoft-stock",
            "growthRate":0.1694,
            "startYear":2025,
            "initialAmount":11_62_006,
            "endYear":2100
        }
    ],
    "cashflows": [
        {
            "id": "my-salary",
            "recurringValue": {
                "amount": 20_80_000,
                "referenceTime": 2025,
                "growthRate": 0.10,
            },
            "enabled": True,
            "startYear": 2025,
            "endYear": 2061,
            "allocations": [
                {
                    "startYear": 2025,
                    "endYear": 2091,
                    "split": [
                        {"corpusId": "savings-bank", "ratio": 0.5},
                        {"corpusId": "health-insurance-large-cap-mutual-fund", "ratio": 0.02},
                        {"corpusId":"marriage-large-mid-cap-mutual-fund","ratio":0.38},
                        {"corpusId":"arbitrage-fund","ratio":0.1},
                    ],
                }
            ],
            "expandedDescription": "my income",
        },
        {
            "id": "microsoft-stock-credit",
            "recurringValue": {
                "amount": 59_151*12,
                "referenceTime": 2025,
                "growthRate": 0.10,
            },
            "enabled":True,
            "startYear":2025,
            "endYear":2026,
            "allocations" : [
                {
                    "startYear":2025,
                    "endYear":2026,
                    "split":[
                        {"corpusId":"microsoft-stock","ratio":1}
                    ]
                }
            ],
            "expandedDescription":"microsoft stock credit"
        },
        {
            "id": "wife-income",
            "recurringValue": {
                "amount": 50_000*12,
                "referenceTime": 2025,
                "growthRate": 0.10,
            },
            "enabled":True,
            "startYear":2028,
            "endYear":2061,
            "allocations" : [
                {
                    "startYear":2025,
                    "endYear":2100,
                    "split":[
                        {"corpusId":"savings-bank","ratio":1}
                    ]
                }
            ],
            "expandedDescription":"microsoft stock credit"
        }
    ],
    "simulation": {
        "startYear": 2025,
        "endYear": 2091,
    },
    "currency": "INR",
}

