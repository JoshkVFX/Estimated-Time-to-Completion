### Estimated Time of Arrival
A simple machine learning system designed to estimate how much time a task will take


## Running the Demo
### System Requirements:
\
Using the default options the demo takes about 1-2 minutes on a single core (2.8GHz max clock) using roughly 1.5GB of RAM
```
pip install requirements.txt
python demo.py
```
Demo.py accepts three arguments:
1. `nodes` The number of nodes each synthetic script should have, default: 10000
2. `scripts` The number of synthetic scripts you want to generate, default: 10-100
3. `nodeTypes` A list of different node types you want to generate, default: nodeTypeA nodeTypeB nodeTypeC nodeTypeD nodeTypeE nodeTypeF


# Usage
### Parser
1. Subclass Script for your relevant DCC
2. Initialise a FileStorage object (or your own Storage subclass) with a file path
3. Initialise Subclass using the Initialised Storage Object
4. Feed subclass.parse into subclass.write
5. Repeat for all scripts


### Interpolator

1. `model = EvaluationModel(model=BayesianRidge)` Initialise the EvaluationModel, providing your preferred Algorithm
2. `model.fit(scripts_with_known_render_times, execution_times)` Fit the parsed script data to the execution time data
3. `prediction = model.predict(scripts_with_unknown_execution_times)` Make a prediction on scripts where we don't know the execution time already
4. Save out your trained model for future use
