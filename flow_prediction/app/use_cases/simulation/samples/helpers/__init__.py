def getExpenseIdx(dataset, id):
    for i in range(len(dataset["expenses"])):
        if dataset["expenses"][i]["id"] == id:
            return i
    raise ValueError(f"Expense with id {id} not found in dataset")
