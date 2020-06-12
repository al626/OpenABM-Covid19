import pandas as pd

pd.set_option("display.max_rows", 200)

import getpass
import logging

logging.basicConfig(level=logging.ERROR)
from adapter_covid19.data_structures import Scenario, ModelParams
from adapter_covid19.simulator import Simulator
import os

if __name__ == "__main__":
    # data_path = f"/home/{getpass.getuser()}/adaptER-covid19/tests/adapter_covid19/data"
    data_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..\\tests\\adapter_covid19\\data"
    )

    simulator = Simulator(data_path)

    scenarios = {
        "10 days only": Scenario(
            lockdown_start_time=10,
            lockdown_end_time=59,
            furlough_start_time=5,
            furlough_end_time=30,
            simulation_end_time=202,
            new_spending_day=5,
            ccff_day=5,
            loan_guarantee_day=5,
            model_params=ModelParams(
                economics_params={},
                gdp_params={},
                personal_params={
                    "default_th": 300,
                    "max_earning_furloughed": 30_000,
                    "alpha": 5,
                    "beta": 20,
                },
                corporate_params={"beta": 1.4, "large_cap_cash_surplus_months": 6,},
            ),
        ),
    }

    result = simulator.simulate_multi(scenarios, show_plots=True, figsize=(5, 15))
