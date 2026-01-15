"""Unit tests for image savers."""

import pytest
import tempfile
import os
from PIL import Image
from src.image_savers import StandardImageSaver


class TestStandardImageSaver:
    """Test StandardImageSaver class."""
    
    def test_initialization_with_defaults(self):
        """Test initialization with default values."""
        saver = StandardImageSaver()
        assert saver.quality == 95
        assert saver.optimize is True
    
    def test_initialization_with_custom_values(self):
        """Test initialization with custom values."""
        saver = StandardImageSaver(quality=80, optimize=False)
        assert saver.quality == 80
        assert saver.optimize is False
    
    def test_quality_clamping(self):
        """Test that quality is clamped between 1 and 100."""
        saver_low = StandardImageSaver(quality=-10)
        saver_high = StandardImageSaver(quality=150)
        assert saver_low.quality == 1
        assert saver_high.quality == 100
    
    def test_save_png(self):
        """Test saving PNG format."""
        saver = StandardImageSaver()
        img = Image.new("RGBA", (100, 100), "blue")
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            temp_path = f.name
        
        try:
            saver.save(img, temp_path)
            assert os.path.exists(temp_path)
            
            # Verify saved image
            saved_img = Image.open(temp_path)
            assert saved_img.size == (100, 100)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_save_jpeg(self):
        """Test saving JPEG format."""
        saver = StandardImageSaver()
        img = Image.new("RGB", (100, 100), "red")
        
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            temp_path = f.name
        
        try:
            saver.save(img, temp_path)
            assert os.path.exists(temp_path)
            
            # Verify saved image
            saved_img = Image.open(temp_path)
            assert saved_img.size == (100, 100)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_save_rgba_as_jpeg_converts_to_rgb(self):
        """Test that RGBA images are converted to RGB for JPEG."""
        saver = StandardImageSaver()
        img = Image.new("RGBA", (100, 100), (255, 0, 0, 128))
        
        with tempfile.NamedTemporaryFile(suffix=".jpeg", delete=False) as f:
            temp_path = f.name
        
        try:
            saver.save(img, temp_path)
            assert os.path.exists(temp_path)
            
            # Verify saved image is RGB
            saved_img = Image.open(temp_path)
            assert saved_img.mode == "RGB"
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
