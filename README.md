# fbacalculator
[![Build Status](https://travis-ci.org/hamptus/fbacalculator.svg?branch=master)](https://travis-ci.org/hamptus/fbacalculator)

This script can be used to calculate FBA fees for Amazon merchants. It should return similar values to:
https://sellercentral.amazon.com/hz/fba/profitabilitycalculator/index?lang=en_US

## Usage
Pass the length, width, height, and weight to the calculate\_fees function. The fees will be returned in decimal format.

## Installation
Install the requirments in requirements.txt
`pip install -r requirements.txt`

## Testing
After installing requirements, run the following from withing the project directory:
`python tests.py`
Amazon documentation can be found here:
http://www.amazon.com/gp/help/customer/display.html/?nodeId=201119410
