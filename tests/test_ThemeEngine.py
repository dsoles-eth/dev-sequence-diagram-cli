import pytest
from unittest import mock
import ThemeEngine

@pytest.fixture
def valid_theme_config():
    return {
        "colors": {
            "header": "#FF0000",
            "body": "#000000",
            "accent": "#00FF00"
        },
        "style": "modern"
    }

@pytest.fixture
def invalid_theme_config():
    return {
        "style": "modern"
    }

@pytest.fixture
def sample_output_text():
    return "This is a sequence diagram node."

@pytest.fixture
def mock_api_response():
    return {"themes": ["dark", "light", "solarized"]}

@pytest.fixture
def mock_requests_module():
    with mock.patch('requests.get') as mock_get:
        yield mock_get

class TestThemeLoader:
    @pytest.mark.parametrize("theme_name, expected_color", [
        ("dark", "#121212"),
        ("light", "#FFFFFF"),
        ("solarized", "#002b36"),
    ])
    def test_load_theme_happy_path(self, theme_name, expected_color):
        with mock.patch.object(ThemeEngine, 'get_theme_source', return_value={'color': expected_color}):
            result = ThemeEngine.load_theme(theme_name)
            assert result['color'] == expected_color

    def test_load_theme_missing_name(self):
        with mock.patch.object(ThemeEngine, 'get_theme_source', return_value=None):
            with pytest.raises(ValueError, match="Theme not found"):
                ThemeEngine.load_theme("non_existent_theme")

    @mock.patch.object(ThemeEngine, 'get_theme_source', return_value={'color': '#000000'})
    def test_load_theme_caches_result(self, mock_source):
        ThemeEngine.load_theme("cached_theme")
        ThemeEngine.load_theme("cached_theme")
        assert mock_source.call_count == 1

class TestThemeApplier:
    def test_apply_colors_happy_path(self, valid_theme_config, sample_output_text):
        with mock.patch.object(ThemeEngine, 'generate_ansi', return_value="[ANSI]"):
            result = ThemeEngine.apply_colors(sample_output_text, valid_theme_config)
            assert result == "[ANSI]This is a sequence diagram node."

    def test_apply_colors_invalid_config(self, sample_output_text):
        with pytest.raises(ValueError, match="Invalid theme config"):
            ThemeEngine.apply_colors(sample_output_text, {})

    def test_apply_colors_empty_text(self, valid_theme_config):
        with mock.patch.object(ThemeEngine, 'generate_ansi', return_value=""):
            result = ThemeEngine.apply_colors("", valid_theme_config)
            assert result == ""

class TestThemeFetcher:
    def test_fetch_themes_success(self, mock_requests_module, mock_api_response):
        mock_requests_module.return_value.json.return_value = mock_api_response
        with mock.patch.object(ThemeEngine, 'requests') as mock_requests:
            mock_requests.get.return_value = mock_requests_module.return_value
            themes = ThemeEngine.fetch_themes_from_api()
            assert 'dark' in themes

    def test_fetch_themes_api_error(self, mock_requests_module):
        mock_requests_module.return_value.raise_for_status.side_effect = Exception("Network Fail")
        with mock.patch.object(ThemeEngine, 'requests'):
            with pytest.raises(Exception):
                ThemeEngine.fetch_themes_from_api()

    def test_fetch_themes_empty_list(self, mock_requests_module, mock_api_response):
        empty_response = {"themes": []}
        mock_requests_module.return_value.json.return_value = empty_response
        with mock.patch.object(ThemeEngine, 'requests'):
            themes = ThemeEngine.fetch_themes_from_api()
            assert themes == []

class TestThemeValidator:
    def test_validate_config_valid(self, valid_theme_config):
        result = ThemeEngine.validate_theme_config(valid_theme_config)
        assert result is True

    def test_validate_config_missing_color(self, invalid_theme_config):
        with pytest.raises(ValueError, match="Missing required key: colors"):
            ThemeEngine.validate_theme_config(invalid_theme_config)

    def test_validate_config_null_input(self):
        with pytest.raises(ValueError, match="Config cannot be None"):
            ThemeEngine.validate_theme_config(None)