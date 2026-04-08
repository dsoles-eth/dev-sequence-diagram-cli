import pytest
from unittest.mock import patch, mock_open, MagicMock
from ExportHandler import ExportHandler

# Assuming ExportHandler uses external libraries for conversion, we mock them.
# In a real scenario, these might be 'svglib', 'pillow', 'cairosvg', etc.
svg_lib_mock = MagicMock()
png_lib_mock = MagicMock()


@pytest.fixture
def handler():
    return ExportHandler()


@pytest.fixture
def sample_diagram_data():
    return {"nodes": [{"id": 1, "label": "User"}], "edges": []}


@pytest.fixture
def mock_filesystem():
    return mock_open(read_data="mocked_binary_data")


class TestExportHandlerSvg:

    @patch('ExportHandler.svg_lib.convert')
    @patch('builtins.open', mock_filesystem())
    def test_export_svg_happy_path(self, mock_open, mock_convert, handler):
        """Test successful SVG export with valid data and path."""
        filepath = "/tmp/output.svg"
        handler.export_svg(sample_diagram_data(), filepath)
        
        # Verify data conversion was called
        mock_convert.assert_called_once_with(sample_diagram_data())
        # Verify file was opened and written
        mock_open.assert_called_once_with(filepath, 'wb')
        mock_open().write.assert_called_once()

    @patch('builtins.open', mock_open())
    @patch('builtins.open', side_effect=PermissionError("No write access"))
    def test_export_svg_permission_error(self, mock_open_side_effect, handler):
        """Test handling of file permission errors gracefully."""
        filepath = "/root/no_access.svg"
        with pytest.raises(PermissionError):
            handler.export_svg(sample_diagram_data(), filepath)
        
        # Ensure the error is not swallowed
        mock_open_side_effect.assert_called_once()

    @patch('ExportHandler.svg_lib.convert')
    @patch('builtins.open', mock_open())
    def test_export_svg_invalid_format(self, mock_open, mock_convert, handler):
        """Test handling of invalid diagram data causing conversion failure."""
        mock_convert.side_effect = ValueError("Invalid SVG syntax")
        filepath = "/tmp/error.svg"
        
        with pytest.raises(ValueError):
            handler.export_svg({"invalid": "data"}, filepath)
        
        # Verify we don't proceed to write if conversion fails
        mock_open().write.assert_not_called()


class TestExportHandlerPng:

    @patch('ExportHandler.png_lib.render')
    @patch('builtins.open', mock_open())
    def test_export_png_happy_path(self, mock_open, mock_render, handler):
        """Test successful PNG export to specified path."""
        filepath = "/tmp/output.png"
        handler.export_png(sample_diagram_data(), filepath)
        
        mock_render.assert_called_once_with(sample_diagram_data())
        mock_open.assert_called_once_with(filepath, 'wb')
        mock_open().write.assert_called_once()

    @patch('ExportHandler.png_lib.render')
    @patch('builtins.open')
    def test_export_png_missing_path(self, mock_open, mock_render, handler):
        """Test handling of missing output path argument."""
        mock_open.side