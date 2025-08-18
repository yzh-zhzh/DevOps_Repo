import sys
from unittest import mock
import pytest

sys.modules['RPi'] = mock.Mock()
sys.modules['RPi.GPIO'] = mock.Mock()
sys.modules['spidev'] = mock.Mock()
sys.modules['smbus'] = mock.Mock()
sys.modules['spi'] = mock.Mock()
sys.modules['MFRC522'] = mock.Mock()
sys.modules['requests'] = mock.Mock()
sys.modules['picamera2'] = mock.Mock()
sys.modules['picamera2.encoders'] = mock.Mock()
sys.modules['picamera2.outputs'] = mock.Mock()

# Make spi.transfer return a tuple/list so it is subscriptable
spi_mock = sys.modules['spi']
spi_mock.transfer = mock.Mock(return_value=[0, 0])

# Make spi.transfer return a tuple/list so it is subscriptable
spi_mock = sys.modules['spi']
spi_mock.transfer = mock.Mock(return_value=[0, 0])

@pytest.fixture(autouse=True)
def patch_dependencies(monkeypatch):
    # Patch all hardware and thread-related functions
    monkeypatch.setattr("RFID.RFID_reader", mock.Mock(side_effect=[False, True]))
    monkeypatch.setattr("Fire_detection.initialise", mock.Mock())
    monkeypatch.setattr("hal.hal_led.init", mock.Mock())
    monkeypatch.setattr("hal.hal_adc.init", mock.Mock())
    monkeypatch.setattr("hal.hal_buzzer.init", mock.Mock())
    monkeypatch.setattr("hal.hal_moisture_sensor.init", mock.Mock())
    monkeypatch.setattr("hal.hal_dc_motor.init", mock.Mock())
    monkeypatch.setattr("hal.hal_dc_motor.set_motor_speed", mock.Mock())
    monkeypatch.setattr("hal.hal_servo.init", mock.Mock())
    monkeypatch.setattr("hal.hal_temp_humidity_sensor.init", mock.Mock())
    monkeypatch.setattr("hal.hal_keypad.init", mock.Mock())
    monkeypatch.setattr("lcd_display_controller.lcd", mock.Mock())
    monkeypatch.setattr("lcd_display_controller.lcd_lock", mock.Mock())
    monkeypatch.setattr("lcd_display_controller.lcd_display_thread", mock.Mock())
    monkeypatch.setattr("temp_sensor.fire_detection_thread", mock.Mock())
    monkeypatch.setattr("notify_alert.notify_fire_alert", mock.Mock())
    monkeypatch.setattr("keypad_manual_override.keypad_manual_override_thread", mock.Mock())
    monkeypatch.setattr("water_adjustment.water_adjustment_thread", mock.Mock())
    monkeypatch.setattr("sprinkler_confirmation.moisture_sensor_sprinkler_confirmation_thread", mock.Mock())
    monkeypatch.setattr("play_fire_tone.play_fire_alert_tone", mock.Mock())
    monkeypatch.setattr("ultrasonic_data.ultrasonic_data_thread", mock.Mock())
    monkeypatch.setattr("Camera.camera_thread", mock.Mock())
    # Patch Thread to avoid starting real threads
    monkeypatch.setattr("threading.Thread", mock.Mock())

def test_main_runs(monkeypatch, capsys):
    # Import main after patching
    import main

    # Patch time.sleep to avoid delays
    monkeypatch.setattr("time.sleep", mock.Mock())

    # Patch start_all_threads to avoid starting threads
    monkeypatch.setattr(main, "start_all_threads", mock.Mock())

    # Patch initialize_hardware to avoid hardware init
    monkeypatch.setattr(main, "initialize_hardware", mock.Mock())

    # Patch the infinite loop after system start to break after one iteration
    loop_counter = {"count": 0}
    def fake_sleep(_):
        loop_counter["count"] += 1
        if loop_counter["count"] > 1:
            raise KeyboardInterrupt()
    monkeypatch.setattr("time.sleep", fake_sleep)

    # Run main and catch output
    with pytest.raises(KeyboardInterrupt):
        main.main()

    captured = capsys.readouterr()
    assert "Waiting for RFID card to activate system..." in captured.out
    assert "RFID detected! Activating all systems." in captured.out
    assert "All sensors and systems are now running in the background." in captured.out