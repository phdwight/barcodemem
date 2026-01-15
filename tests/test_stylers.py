"""Unit tests for styler classes."""

import pytest
from PIL import Image
from src.stylers import StandardStyler, CircularDotsStyler, RoundedSquareStyler


class TestStandardStyler:
    """Test StandardStyler class."""
    
    def test_apply_style_returns_unchanged_image(self):
        """Test that standard styler returns image unchanged."""
        styler = StandardStyler()
        img = Image.new("RGBA", (100, 100), "white")
        modules = [[True, False], [False, True]]
        result = styler.apply_style(img, modules, 2)
        assert result == img
        assert result.size == (100, 100)


class TestCircularDotsStyler:
    """Test CircularDotsStyler class."""
    
    def test_initialization_with_defaults(self):
        """Test initialization with default values."""
        styler = CircularDotsStyler()
        assert styler.fg_color == "black"
        assert styler.bg_color == "white"
        assert styler.dot_scale == 0.8
    
    def test_initialization_with_custom_values(self):
        """Test initialization with custom values."""
        styler = CircularDotsStyler(fg_color="blue", bg_color="yellow", dot_scale=0.5)
        assert styler.fg_color == "blue"
        assert styler.bg_color == "yellow"
        assert styler.dot_scale == 0.5
    
    def test_dot_scale_clamping(self):
        """Test that dot scale is clamped between 0.1 and 1.0."""
        styler_low = CircularDotsStyler(dot_scale=-1.0)
        styler_high = CircularDotsStyler(dot_scale=2.0)
        assert styler_low.dot_scale == 0.1
        assert styler_high.dot_scale == 1.0
    
    def test_apply_style_creates_new_image(self):
        """Test that apply_style creates a new styled image."""
        styler = CircularDotsStyler()
        img = Image.new("RGBA", (210, 210), "white")
        # Create a simple 21x21 module grid (common QR size)
        modules = [[bool((i + j) % 2) for j in range(21)] for i in range(21)]
        result = styler.apply_style(img, modules, 21)
        
        assert result is not img
        assert result.size == img.size
        assert result.mode == "RGBA"


class TestRoundedSquareStyler:
    """Test RoundedSquareStyler class."""
    
    def test_initialization_with_defaults(self):
        """Test initialization with default values."""
        styler = RoundedSquareStyler()
        assert styler.fg_color == "black"
        assert styler.bg_color == "white"
        assert styler.corner_radius == 0.3
    
    def test_corner_radius_clamping(self):
        """Test that corner radius is clamped between 0 and 0.5."""
        styler_low = RoundedSquareStyler(corner_radius=-1.0)
        styler_high = RoundedSquareStyler(corner_radius=1.5)
        assert styler_low.corner_radius == 0.0
        assert styler_high.corner_radius == 0.5
    
    def test_apply_style_creates_new_image(self):
        """Test that apply_style creates a new styled image."""
        styler = RoundedSquareStyler()
        img = Image.new("RGBA", (210, 210), "white")
        modules = [[bool((i + j) % 2) for j in range(21)] for i in range(21)]
        result = styler.apply_style(img, modules, 21)
        
        assert result is not img
        assert result.size == img.size
        assert result.mode == "RGBA"
