import os
import sys
import pandas as pd
from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging

@dataclass
class DataValidationConfig:

    validation_status = os.path.join(
        "artifacts",
        "validation_status.txt"
    )

