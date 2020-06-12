import pandas as pd

pd.set_option("display.max_rows", 200)

import getpass
import logging

logging.basicConfig(level=logging.ERROR)
from adapter_covid19.data_structures import Scenario, ModelParams
from adapter_covid19.scenarios import SCENARIO_10_DAYS
from adapter_covid19.simulator import Simulator
import os

if __name__ == "__main__":
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests/adapter_covid19/data"
    )

    simulator = Simulator(data_path)

    scenarios = {"10 days only": SCENARIO_10_DAYS}

    result = simulator.simulate_multi(scenarios, show_plots=True, figsize=(5, 15))
