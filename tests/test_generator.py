"""Integration tests for QR code generation."""

import pytest
import tempfile
import os
from PIL import Image
from src.generator import QRCodeGenerator, QRCodeGeneratorBuilder
from src.config import StandardQRConfig
from src.stylers import StandardStyler, CircularDotsStyler
from src.logo_processors import CircularLogoProcessor, NoLogoProcessor
from src.image_savers import StandardImageSaver


class TestQRCodeGenerator:
    """Test QRCodeGenerator integration."""
    
    def test_generate_basic_qr_without_logo(self):
        """Test generating basic QR code without logo."""
        config = StandardQRConfig()
        styler = StandardStyler()
        logo_processor = NoLogoProcessor()
        image_saver = StandardImageSaver()
        
        generator = QRCodeGenerator(config, styler, logo_processor, image_saver)
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            temp_path = f.name
        
        try:
            generator.generate("https://example.com", output_path=temp_path)
            
            assert os.path.exists(temp_path)
            img = Image.open(temp_path)
            assert img.size[0] > 0
            assert img.size[1] > 0
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_generate_with_logo(self):
        """Test generating QR code with logo."""
        # Create a temporary logo
        logo_img = Image.new("RGB", (100, 100), "red")
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            logo_path = f.name
            logo_img.save(logo_path)
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            output_path = f.name
        
        try:
            config = StandardQRConfig()
            styler = StandardStyler()
            logo_processor = CircularLogoProcessor()
            image_saver = StandardImageSaver()
            
            generator = QRCodeGenerator(config, styler, logo_processor, image_saver)
            generator.generate("https://example.com", logo_path=logo_path, output_path=output_path)
            
            assert os.path.exists(output_path)
            img = Image.open(output_path)
            assert img.size[0] > 0
            assert img.size[1] > 0
        finally:
            if os.path.exists(logo_path):
                os.unlink(logo_path)
            if os.path.exists(output_path):
                os.unlink(output_path)


class TestQRCodeGeneratorBuilder:
    """Test QRCodeGeneratorBuilder."""
    
    def test_builder_with_defaults(self):
        """Test builder creates generator with defaults."""
        builder = QRCodeGeneratorBuilder()
        generator = builder.build()
        
        assert generator is not None
        assert isinstance(generator, QRCodeGenerator)
    
    def test_builder_with_custom_components(self):
        """Test builder with custom components."""
        config = StandardQRConfig(fg_color="blue")
        styler = CircularDotsStyler(fg_color="blue")
        logo_processor = NoLogoProcessor()
        image_saver = StandardImageSaver(quality=90)
        
        generator = (QRCodeGeneratorBuilder()
                     .with_config(config)
                     .with_styler(styler)
                     .with_logo_processor(logo_processor)
                     .with_image_saver(image_saver)
                     .build())
        
        assert generator is not None
        assert generator.config is config
        assert generator.styler is styler
    
    def test_create_standard_preset(self):
        """Test creating standard preset generator."""
        generator = QRCodeGeneratorBuilder.create_standard()
        assert generator is not None
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            temp_path = f.name
        
        try:
            generator.generate("https://example.com", output_path=temp_path)
            assert os.path.exists(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_create_modern_preset(self):
        """Test creating modern preset generator."""
        generator = QRCodeGeneratorBuilder.create_modern()
        assert generator is not None
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            temp_path = f.name
        
        try:
            generator.generate("https://example.com", output_path=temp_path)
            assert os.path.exists(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_create_vibrant_preset(self):
        """Test creating vibrant preset generator."""
        generator = QRCodeGeneratorBuilder.create_vibrant()
        assert generator is not None
    
    def test_create_elegant_preset(self):
        """Test creating elegant preset generator."""
        generator = QRCodeGeneratorBuilder.create_elegant()
        assert generator is not None
