#! /usr/bin/env python3

"""
A script for regressing and plotting two variables stored in columns of a
tabular data file.
"""

import os
import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
