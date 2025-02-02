from flow_prediction.app.use_cases.simulation import (
    CashflowSimulationUseCaseInitData,
)


data: CashflowSimulationUseCaseInitData = {
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
            "recurringValue": {"amount": 0, "referenceTime": 0},
            "fundingCorpora": [
                {
                    "id": "savings-bank",
                }
            ],
        },
        {
            "id": "kid-1",
            "startYear": 2026,
            "endYear": 2030,
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
            "initialAmount": 1_50_000,
        },
        {
            "id": "epf",
            "growthRate": 0.08,
            "startYear": 2025,
            "initialAmount": 0,
        },
        {
            "id": "large-cap-mutual-fund",
            "growthRate": 0.12,
            "startYear": 2025,
            "initialAmount": 0,
        },
        {
            "id": "small-cap-mutual-fund",
            "growthRate": 0.15,
            "startYear": 2025,
            "initialAmount": 0,
        },
        {
            "id": "medium-large-cap-mutual-fund",
            "growthRate": 0.13,
            "startYear": 2025,
            "initialAmount": 0,
        },
        {
            "id": "medium-small-cap-mutual-fund",
            "growthRate": 0.14,
            "startYear": 2025,
            "initialAmount": 0,
        },
        {
            "id": "arbitrage-fund",
            "growthRate": 0.06,
            "startYear": 2025,
            "initialAmount": 0,
        },
    ],
    "cashflows": [
        {
            "id": "my-salary",
            "recurringValue": {
                "amount": 2080000,
                "referenceTime": 2025,
                "growthRate": 10,
            },
            "enabled": True,
            "startYear": 2025,
            "endYear": 2091,
            "allocations": [
                {
                    "startYear": 2025,
                    "endYear": 2091,
                    "split": [
                        {"corpusId": "savings-bank", "ratio": 0.5},
                        {"corpusId": "large-cap-mutual-fund", "ratio": 0.5},
                    ],
                }
            ],
            "expandedDescription": "my income",
        }
    ],
    "simulation": {
        "startYear": 2025,
        "endYear": 2091,
    },
    "currency": "INR",
}
