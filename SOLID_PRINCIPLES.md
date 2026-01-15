# SOLID Principles Implementation

This document explains how SOLID principles were applied to the QR code generator.

## Single Responsibility Principle (SRP)

Each class has one clear responsibility:

- **`QRCodeConfig`**: Manages configuration data only
- **`QRCodeStyler`**: Handles QR code visual styling only
- **`LogoProcessor`**: Processes and positions logos only
- **`ImageSaver`**: Saves images to disk only
- **`QRCodeGenerator`**: Orchestrates the generation process (composition of other components)

## Open/Closed Principle (OCP)

The system is open for extension but closed for modification:

- **Abstract interfaces** define contracts that can be extended
- **New stylers** can be added by implementing `QRCodeStyler` without modifying existing code
- **New logo processors** can be added by implementing `LogoProcessor`
- **New image formats** can be supported by implementing `ImageSaver`

Example: Adding a new gradient styler requires creating a new class, not modifying existing ones:

```python
class GradientStyler(QRCodeStyler):
    def apply_style(self, qr_image, modules, modules_count):
        # New gradient implementation
        pass
```

## Liskov Substitution Principle (LSP)

All implementations can be substituted for their base types:

- Any `QRCodeStyler` implementation can be used interchangeably
- Any `LogoProcessor` can replace another without breaking functionality
- The `QRCodeGenerator` doesn't care which concrete implementation is used

Example:
```python
# All of these work identically from the generator's perspective
styler = StandardStyler()
styler = CircularDotsStyler()
styler = RoundedSquareStyler()

generator = QRCodeGenerator(config, styler, logo_processor, saver)
```

## Interface Segregation Principle (ISP)

Small, focused interfaces prevent clients from depending on methods they don't use:

- **`QRCodeConfig`**: Only configuration getters
- **`QRCodeStyler`**: Single `apply_style` method
- **`LogoProcessor`**: Two focused methods: `process_logo` and `paste_logo`
- **`ImageSaver`**: Single `save` method

No class is forced to implement irrelevant methods.

## Dependency Inversion Principle (DIP)

High-level modules depend on abstractions, not concrete implementations:

- **`QRCodeGenerator`** depends on abstract interfaces, not concrete classes
- Configuration is injected through constructor (dependency injection)
- The builder pattern further decouples construction from use

Example:
```python
# Generator depends on abstractions
def __init__(self,
    config: QRCodeConfig,          # Abstract
    styler: QRCodeStyler,          # Abstract
    logo_processor: LogoProcessor, # Abstract
    image_saver: ImageSaver        # Abstract
):
```

## Benefits Achieved

1. **Testability**: Each component can be tested in isolation with mocks
2. **Maintainability**: Changes to one component don't affect others
3. **Extensibility**: New features can be added without modifying existing code
4. **Flexibility**: Components can be mixed and matched for different use cases
5. **Clarity**: Each class has a clear, single purpose

## Example Usage

The builder pattern makes SOLID principles practical:

```python
# Easy to configure with different combinations
generator = (QRCodeGeneratorBuilder()
    .with_config(AestheticQRConfig(fg_color="blue"))
    .with_styler(CircularDotsStyler(dot_scale=0.8))
    .with_logo_processor(CircularLogoProcessor())
    .with_image_saver(StandardImageSaver(quality=95))
    .build())

generator.generate("https://example.com", "logo.png", "output.png")
```
