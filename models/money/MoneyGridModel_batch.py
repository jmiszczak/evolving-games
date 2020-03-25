from MoneyGridModel import MoneyGridModel, gini 

import mesa.batchrunner as mb

fixed_params = {
        "width": 100,
        "height": 100
        }

variable_params = { "N" : [50, 100, 200] }

batch_run = mb.BatchRunner(
        MoneyGridModel,
        variable_params,
        fixed_params,
        iterations=5,
        max_steps=100,
        model_reporters={"Gini": gini}
        )

batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
run_data.to_csv('MoneyGridModel.zip', 
        index=False, 
        compression=dict(method='zip', archive_name='data.csv')
        )

