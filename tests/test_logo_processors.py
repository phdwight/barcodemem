"""Unit tests for logo processors."""

import pytest
from PIL import Image
from unittest.mock import Mock, patch
from src.logo_processors import CircularLogoProcessor, SquareLogoProcessor, NoLogoProcessor


class TestCircularLogoProcessor:
    """Test CircularLogoProcessor class."""
    
    def test_initialization_with_defaults(self):
        """Test initialization with default values."""
        processor = CircularLogoProcessor()
        assert processor.logo_scale == 3.5
    
    def test_initialization_with_custom_scale(self):
        """Test initialization with custom scale."""
        processor = CircularLogoProcessor(logo_scale=5.0)
        assert processor.logo_scale == 5.0
    
    def test_minimum_scale_enforced(self):
        """Test that minimum scale of 2.0 is enforced."""
        processor = CircularLogoProcessor(logo_scale=1.0)
        assert processor.logo_scale == 2.0
    
    @patch('src.logo_processors.Image.open')
    def test_process_logo_returns_image(self, mock_open):
        """Test that process_logo returns a processed image."""
        # Create mock logo
        mock_logo = Image.new("RGBA", (100, 100), "red")
        mock_open.return_value = mock_logo
        
        processor = CircularLogoProcessor()
        result = processor.process_logo("dummy.png", (400, 400))
        
        assert result is not None
        assert isinstance(result, Image.Image)
        assert result.mode == "RGBA"
    
    def test_paste_logo_centers_logo(self):
        """Test that paste_logo centers the logo."""
        processor = CircularLogoProcessor()
        qr_image = Image.new("RGBA", (400, 400), "white")
        logo = Image.new("RGBA", (100, 100), "red")
        
        result = processor.paste_logo(qr_image, logo)
        
        assert result is qr_image  # Should modify in place
        assert result.size == (400, 400)


class TestSquareLogoProcessor:
    """Test SquareLogoProcessor class."""
    
    def test_initialization_with_defaults(self):
        """Test initialization with default values."""
        processor = SquareLogoProcessor()
        assert processor.logo_scale == 3.5
        assert processor.rounded is False
    
    def test_initialization_with_rounded(self):
        """Test initialization with rounded corners."""
        processor = SquareLogoProcessor(logo_scale=4.0, rounded=True)
        assert processor.logo_scale == 4.0
        assert processor.rounded is True
    
    @patch('src.logo_processors.Image.open')
    def test_process_logo_returns_square(self, mock_open):
        """Test that process_logo returns a square image."""
        # Create mock non-square logo
        mock_logo = Image.new("RGBA", (150, 100), "blue")
        mock_open.return_value = mock_logo
        
        processor = SquareLogoProcessor()
        result = processor.process_logo("dummy.png", (400, 400))
        
        assert result is not None
        # Should be square after processing
        assert result.size[0] == result.size[1]


class TestNoLogoProcessor:
    """Test NoLogoProcessor class."""
    
    def test_process_logo_returns_none(self):
        """Test that process_logo returns None."""
        processor = NoLogoProcessor()
        result = processor.process_logo("dummy.png", (400, 400))
        assert result is None
    
    def test_paste_logo_returns_unchanged(self):
        """Test that paste_logo returns image unchanged."""
        processor = NoLogoProcessor()
        qr_image = Image.new("RGBA", (400, 400), "white")
        result = processor.paste_logo(qr_image, None)
        assert result is qr_image
