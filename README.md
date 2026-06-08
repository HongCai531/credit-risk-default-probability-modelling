# Credit Risk Default Probability Modelling

This project builds a Python-based credit risk analytics framework to estimate option-implied bankruptcy probabilities using risk-neutral density methods. It is inspired by my master's thesis on forecasting implicit bankruptcy probability using the Positive Convolution Approximation (PCA) method.

The objective is to demonstrate how market-based information from options can be transformed into forward-looking default probability estimates and compared with CDS-implied default probability benchmarks.

## Project Objectives

- Estimate risk-neutral densities from option price data
- Apply the Positive Convolution Approximation method to infer option-implied bankruptcy probabilities
- Optimise bandwidth parameters to reduce option pricing errors
- Compare bankruptcy and non-bankruptcy firms using implied default probability signals
- Benchmark option-implied bankruptcy probabilities against CDS-implied default probabilities
- Evaluate predictive performance using ROC and CAP analysis

## Methods

- Option price filtering and preprocessing
- Conversion of American option prices into European-style prices
- Out-of-the-money put option selection
- Risk-neutral density estimation
- Positive Convolution Approximation
- Bandwidth parameter optimisation
- Bankruptcy probability calculation
- CDS-implied default probability estimation
- Mean absolute percentage error analysis
- Receiver Operating Characteristic analysis
- Cumulative Accuracy Profile analysis

## Key Credit Risk Measures

- Risk-neutral density
- Option-implied bankruptcy probability
- CDS-implied default probability
- Mean Absolute Percentage Error
- ROC curve
- CAP curve
- Bankruptcy vs non-bankruptcy probability spread
- Short-window default prediction signal

## Tools

- Python
- pandas
- NumPy
- SciPy
- statsmodels
- matplotlib
- Jupyter Notebook

## Repository Structure

```text
credit-risk-default-probability-modelling/
├── README.md
├── credit_risk_default_probability.py
├── data_sample/
├── figures/
└── requirements.txt
