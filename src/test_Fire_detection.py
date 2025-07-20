
from src import Fire_detection
import time 
import pytest
#import RPI.GPIO as GPIO
import sys
from unittest.mock import MagicMock
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()

def test_smoke_detector():
    result = Fire_detection.smoke_detector(True, True)
    assert result is True