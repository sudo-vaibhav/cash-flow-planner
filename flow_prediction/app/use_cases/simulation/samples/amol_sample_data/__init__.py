from ...init_data import (
    CashflowSimulationUseCaseInitData,
)


amol_sample_data: CashflowSimulationUseCaseInitData = {
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
                    "id": "large-cap-mutual-fund",
                },
                {
                    "id": "arbitrage-fund",
                },
            ],
        },
        {
            "id": "retirement",
            "startYear": 2061,
            "endYear": 2091,
            "enabled": True,
            "growthRate": 0.09,
            "initialValue": {
                "amount": 0,
                "referenceTime": 2025,
            },
            "recurringValue": {
                "amount": 1_50_000 * 12,
                "referenceTime": 2025,
            },
            "fundingCorpora": [
                {
                    "id": "savings-bank",
                },
                {
                    "id": "epf",
                },
                {
                    "id": "large-cap-mutual-fund",
                },
                {
                    "id": "medium-large-cap-mutual-fund",
                },
                {
                    "id": "medium-small-cap-mutual-fund",
                },
                {
                    "id": "arbitrage-fund",
                },
                {
                    "id": "small-cap-mutual-fund",
                },
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
            "initialAmount": 1_50_000,
            "successorCorpusId": "large-cap-mutual-fund",
        },
        {
            "id": "epf",
            "growthRate": 0.08,
            "startYear": 2025,
            "initialAmount": 0,
            "endYear": 2061,
            "successorCorpusId": "large-cap-mutual-fund",
        },
        {
            "id": "large-cap-mutual-fund",
            "growthRate": 0.12,
            "startYear": 2025,
            "initialAmount": 0,
            "endYear": 2100,
            "successorCorpusId": "large-cap-mutual-fund",
        },
        {
            "id": "small-cap-mutual-fund",
            "growthRate": 0.15,
            "startYear": 2025,
            "initialAmount": 0,
            "endYear": 2100,
            "successorCorpusId": "large-cap-mutual-fund",
        },
        {
            "id": "medium-large-cap-mutual-fund",
            "growthRate": 0.13,
            "startYear": 2025,
            "initialAmount": 0,
            "endYear": 2100,
            "successorCorpusId": "large-cap-mutual-fund",
        },
        {
            "id": "medium-small-cap-mutual-fund",
            "growthRate": 0.14,
            "startYear": 2025,
            "initialAmount": 0,
            "endYear": 2100,
            "successorCorpusId": "large-cap-mutual-fund",
        },
        {
            "id": "arbitrage-fund",
            "growthRate": 0.06,
            "startYear": 2025,
            "initialAmount": 0,
            "endYear": 2100,
            "successorCorpusId": "large-cap-mutual-fund",
        },
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
