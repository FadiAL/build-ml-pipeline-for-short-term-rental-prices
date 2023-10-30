# NYC AIRBNB Rental Prices

This project aims to model the prices of AirBNBs in NYC using random forests.

The pipeline is written to be scalable, modular, and production-ready.

## Weights & Biases
This project relies on Weights & Biases for experiment and artifact tracking.  Create an account on http://wandb.ai and follow the login instructions

## Dependencies
The environment is fully self-contained within the `environment.yml` file found at the root of the project repo.
Install it with conda: `conda create -f environment.yml`

## Components
For all of the below components, see their `MLproject` file for details about arguments

### get_data
This component logs the chosen sample data to Weights & Biases.

#### Input Artifacts
No input artifacts

#### Output Artifacts
Outputs the chosen initial nyc airbnb dataset to weights & biases

### eda
This component launches a jupyter notebook to examine the sample data

#### Input Artifacts
No input artifacts

#### Output Artifacts
No output artifacts beyond the notebook itself that was used to run EDA

### basic_cleaning
This component cleans a given dataset using the methods learning during EDA.  The algorithms used
are not included in the production model since they are only needed in the training/testing dataset

#### Input Artifacts
Raw dataset

#### Output Artifacts
Preprocessed, cleaned dataset

### data_check
This component checks the dataset for any violations of assumptions or statistical issues.

#### Input Artifacts
Preprocessed, cleaned dataset

#### Output Artifacts
No output artifacts

### train_val_test_split
This component splits the input dataset into a test and train subset

#### Input Artifacts
Preprocessed, cleaned dataset

#### Output Artifacts
Two split datasets, one for training and validation, the other for final testing

### train_random_forest
This component is the inference pipeline, that runs a set of transformers on the data and feeds it into a
random forests model

#### Input Artifacts
A train + validation dataset

#### Output Artifacts
An output mlflow model containing the inference pipeline.

As part of training, this component also logs metrics and summaries to W&B

### test_regression_model
This component tests an mlflow model produced during the `train_random_forest` step to validate its performance
on the test dataset, logging the results to W&B

#### Input Artifacts
An mlflow model directory, and a test dataset

#### Output Artifacts
No output artifacts