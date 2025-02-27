from typing import List


class Lease:
    """
    Defines how a single Cashflow is split among multiple corpora over time.
    We store multiple allocations in (start_year, end_year, corpus_id, proportion).

    e.g. you can specify:
      2025..2027 => 0.60 to "General", 0.40 to "Retire"
      2028..2030 => 0.20 to "General", 0.80 to "Retire"
    """

    def __init__(self, flow_id: str):
        self.flow_id = flow_id
        # Each entry: (start_year, end_year, corpus_id, proportion)
        self.allocations = []

    def add_allocation(
        self, start_year: int, end_year: int, corpus_id: str, proportion: float
    ):
        """
        proportion should be a fraction between 0.0 and 1.0
        You can add multiple allocations that overlap or vary by year range.
        """
        self.allocations.append((start_year, end_year, corpus_id, proportion))

    def get_allocations_for_year(self, year: int) -> List[tuple]:
        """
        Return a list of (corpus_id, proportion) that apply for the given year.
        If multiple allocations overlap, the proportions should sum up appropriately.
        """
        active = []
        for s_year, e_year, c_id, prop in self.allocations:
            if s_year <= year <= e_year:
                active.append((c_id, prop))
        return active
