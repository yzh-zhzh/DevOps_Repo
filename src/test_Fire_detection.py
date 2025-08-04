import pytest
from unittest.mock import patch
import Fire_detection

# Test smoke_detected: IR True, LDR < 600
@patch('Fire_detection.ir_sensor.get_ir_sensor_state', return_value=True)
@patch('Fire_detection.adc.get_adc_value', return_value=500)
def test_smoke_detected_true(mock_ldr, mock_ir):
    assert Fire_detection.smoke_detected() is True

# Test smoke_detected: IR False, LDR < 600
@patch('Fire_detection.ir_sensor.get_ir_sensor_state', return_value=False)
@patch('Fire_detection.adc.get_adc_value', return_value=500)
def test_smoke_detected_false_ir(mock_ldr, mock_ir):
    assert Fire_detection.smoke_detected() is False

# Test smoke_detected: IR True, LDR > 600
@patch('Fire_detection.ir_sensor.get_ir_sensor_state', return_value=True)
@patch('Fire_detection.adc.get_adc_value', return_value=700)
def test_smoke_detected_false_ldr(mock_ldr, mock_ir):
    assert Fire_detection.smoke_detected() is False

# Test high_temp_detected: temp > 40
@patch('Fire_detection.temp_humid_sensor.read_temp_humidity', return_value=(41, 50))
def test_high_temp_detected_true(mock_temp):
    assert Fire_detection.high_temp_detected() is True

# Test high_temp_detected: temp < 40
@patch('Fire_detection.temp_humid_sensor.read_temp_humidity', return_value=(30, 50))
def test_high_temp_detected_false(mock_temp):
    assert Fire_detection.high_temp_detected() is False

# Test fire_detected: smoke_detected True
@patch('Fire_detection.smoke_detected', return_value=True)
@patch('Fire_detection.high_temp_detected', return_value=False)
def test_fire_detected_smoke(mock_temp, mock_smoke):
    assert Fire_detection.fire_detected() is True

# Test fire_detected: high_temp_detected True
@patch('Fire_detection.smoke_detected', return_value=False)
@patch('Fire_detection.high_temp_detected', return_value=True)
def test_fire_detected_temp(mock_temp, mock_smoke):
    assert Fire_detection.fire_detected() is True

# Test fire_detected: both False
@patch('Fire_detection.smoke_detected', return_value=False)
@patch('Fire_detection.high_temp_detected', return_value=False)
def test_fire_detected_false(mock_temp, mock_smoke):
    assert Fire_detection.fire_detected() is False