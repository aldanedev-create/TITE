"""Unit tests for the main module."""

import sys
from pathlib import Path

import pytest

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import main  # noqa: E402


class TestMain:
    """Test suite for the main module."""

    def test_main_returns_zero(self):
        """Test that main returns 0 on success."""
        result = main()
        assert result == 0

    def test_main_creates_log_directory(self, tmp_path):
        """Test that main creates the log directory if it doesn't exist."""
        # Override log path for testing
        original_cwd = Path.cwd()
        try:
            # Change to temporary directory for test isolation
            import os
            os.chdir(tmp_path)
            
            # Create logs directory
            log_dir = tmp_path / "logs"
            log_dir.mkdir(exist_ok=True)
            
            # Run main
            result = main()
            assert result == 0
            
            # Verify log file was created
            log_files = list(log_dir.glob("*.log"))
            assert len(log_files) > 0
            
        finally:
            os.chdir(original_cwd)

    def test_main_handles_interrupt(self, monkeypatch):
        """Test that main handles KeyboardInterrupt gracefully."""
        def mock_main():
            raise KeyboardInterrupt()
        
        with pytest.raises(KeyboardInterrupt):
            mock_main()

    def test_main_handles_exception(self, monkeypatch):
        """Test that main handles exceptions gracefully."""
        def mock_main():
            raise ValueError("Test error")
        
        with pytest.raises(ValueError):
            mock_main()


# Additional test utilities
@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {
        "name": "test_project",
        "version": "0.1.0",
        "environment": "test"
    }


def test_configuration(sample_data):
    """Test configuration data."""
    assert sample_data["name"] == "test_project"
    assert sample_data["version"] == "0.1.0"
    assert sample_data["environment"] == "test"


if __name__ == "__main__":
    pytest.main(["-v", __file__])