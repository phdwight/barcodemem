"""Unit tests for configuration classes."""

import pytest
import qrcode
from src.config import StandardQRConfig, AestheticQRConfig


class TestStandardQRConfig:
    """Test StandardQRConfig class."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = StandardQRConfig()
        assert config.get_version() == 1
        assert config.get_error_correction() == qrcode.constants.ERROR_CORRECT_H
        assert config.get_box_size() == 10
        assert config.get_border() == 4
        assert config.get_colors() == ("black", "white")
    
    def test_custom_values(self):
        """Test custom configuration values."""
        config = StandardQRConfig(
            version=2,
            error_correction="L",
            box_size=15,
            border=2,
            fg_color="blue",
            bg_color="yellow"
        )
        assert config.get_version() == 2
        assert config.get_error_correction() == qrcode.constants.ERROR_CORRECT_L
        assert config.get_box_size() == 15
        assert config.get_border() == 2
        assert config.get_colors() == ("blue", "yellow")
    
    def test_error_correction_mapping(self):
        """Test error correction level mapping."""
        config_l = StandardQRConfig(error_correction="L")
        config_m = StandardQRConfig(error_correction="M")
        config_q = StandardQRConfig(error_correction="Q")
        config_h = StandardQRConfig(error_correction="H")
        
        assert config_l.get_error_correction() == qrcode.constants.ERROR_CORRECT_L
        assert config_m.get_error_correction() == qrcode.constants.ERROR_CORRECT_M
        assert config_q.get_error_correction() == qrcode.constants.ERROR_CORRECT_Q
        assert config_h.get_error_correction() == qrcode.constants.ERROR_CORRECT_H
    
    def test_invalid_error_correction_defaults_to_h(self):
        """Test that invalid error correction defaults to H."""
        config = StandardQRConfig(error_correction="INVALID")
        assert config.get_error_correction() == qrcode.constants.ERROR_CORRECT_H


class TestAestheticQRConfig:
    """Test AestheticQRConfig class."""
    
    def test_inherits_from_standard(self):
        """Test that AestheticQRConfig inherits StandardQRConfig behavior."""
        config = AestheticQRConfig()
        assert config.get_version() == 1
        assert config.get_box_size() == 10
        assert config.get_colors() == ("black", "white")
    
    def test_additional_aesthetic_properties(self):
        """Test additional aesthetic properties."""
        config = AestheticQRConfig(
            border_color="red",
            rounded_corners=True,
            dot_scale=0.5
        )
        assert config.get_border_color() == "red"
        assert config.has_rounded_corners() is True
        assert config.get_dot_scale() == 0.5
    
    def test_border_color_defaults_to_bg_color(self):
        """Test that border color defaults to background color."""
        config = AestheticQRConfig(bg_color="blue")
        assert config.get_border_color() == "blue"
    
    def test_custom_border_color(self):
        """Test custom border color."""
        config = AestheticQRConfig(bg_color="white", border_color="gray")
        assert config.get_border_color() == "gray"
