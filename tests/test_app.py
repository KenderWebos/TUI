"""
Tests for TUI Application
"""
import pytest
from TUI_APP.config import APP_NAME


def test_app_name():
    """Test that app name is configured"""
    assert APP_NAME == "TUI App"


def test_imports():
    """Test that main imports work"""
    from TUI_APP.app import tui_app
    from TUI_APP.screens import DashboardScreen, LogsScreen
    
    assert tui_app is not None
    assert DashboardScreen is not None
    assert LogsScreen is not None
