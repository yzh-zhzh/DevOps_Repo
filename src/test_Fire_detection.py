
import Fire_detection
import time 
from unittest import mock
import pytest
def test_smoke_detector():
    result = Fire_detection.smoke_detector(True, True)
    assert result is True