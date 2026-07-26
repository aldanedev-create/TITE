"""
Browser launcher for Tite.

This module provides functionality to open the browser
for the development server.
"""

import os
import subprocess
import sys
import webbrowser
from typing import Dict, Optional

from loguru import logger


class BrowserLauncher:
    """
    Launches the browser for development.
    
    This class handles opening the browser to the development
    server URL with support for different browsers.
    
    Attributes:
        default_browser: Default browser to use
        auto_open: Whether to auto-open the browser
    """
    
    def __init__(self, default_browser: Optional[str] = None, auto_open: bool = True):
        """
        Initialize the browser launcher.
        
        Args:
            default_browser: Default browser to use
            auto_open: Whether to auto-open the browser
        """
        self.default_browser = default_browser
        self.auto_open = auto_open
        
    def open(self, url: str, browser: Optional[str] = None) -> bool:
        """
        Open the browser to a URL.
        
        Args:
            url: URL to open
            browser: Browser to use (overrides default)
            
        Returns:
            bool: True if browser was opened
        """
        if not self.auto_open:
            logger.info(f"Auto-open disabled. Open {url} manually.")
            return False
            
        logger.info(f"Opening browser: {url}")
        
        try:
            # Use specific browser if provided
            if browser:
                return self._open_with_browser(url, browser)
                
            # Use default browser
            if self.default_browser:
                return self._open_with_browser(url, self.default_browser)
                
            # Use system default
            return webbrowser.open(url)
            
        except Exception as e:
            logger.error(f"Failed to open browser: {e}")
            return False
            
    def _open_with_browser(self, url: str, browser: str) -> bool:
        """
        Open URL with a specific browser.
        
        Args:
            url: URL to open
            browser: Browser command
            
        Returns:
            bool: True if browser was opened
        """
        try:
            if sys.platform == "win32":
                os.startfile(browser)
                return True
            elif sys.platform == "darwin":
                subprocess.run(["open", "-a", browser, url])
                return True
            else:
                subprocess.run([browser, url])
                return True
        except Exception as e:
            logger.error(f"Failed to open with {browser}: {e}")
            return False
            
    def get_available_browsers(self) -> list:
        """
        Get a list of available browsers.
        
        Returns:
            list: List of available browser commands
        """
        browsers = []
        
        if sys.platform == "win32":
            common_browsers = ["chrome", "firefox", "edge", "iexplore"]
        elif sys.platform == "darwin":
            common_browsers = ["Google Chrome", "Firefox", "Safari", "Brave"]
        else:
            common_browsers = ["google-chrome", "firefox", "chromium-browser", "brave-browser"]
            
        for browser in common_browsers:
            if self._is_browser_available(browser):
                browsers.append(browser)
                
        return browsers
        
    def _is_browser_available(self, browser: str) -> bool:
        """
        Check if a browser is available.
        
        Args:
            browser: Browser command
            
        Returns:
            bool: True if browser is available
        """
        try:
            if sys.platform == "win32":
                # Check if executable exists in PATH
                for path in os.environ["PATH"].split(";"):
                    if os.path.exists(os.path.join(path, f"{browser}.exe")):
                        return True
                return False
            else:
                result = subprocess.run(
                    ["which", browser],
                    capture_output=True,
                    text=True,
                )
                return result.returncode == 0
        except Exception:
            return False
            
    def open_docs(self, url: str = "https://github.com/aldanedev-create/TITE") -> bool:
        """
        Open the Tite documentation.
        
        Args:
            url: Documentation URL
            
        Returns:
            bool: True if opened
        """
        return self.open(url)
        
    def open_github(self) -> bool:
        """
        Open the Tite GitHub repository.
        
        Returns:
            bool: True if opened
        """
        return self.open("https://github.com/aldanedev-create/TITE")


class BrowserManager:
    """
    Manages browser instances for development.
    
    This class provides management of multiple browser instances
    with support for different browsers and profiles.
    """
    
    def __init__(self):
        """Initialize the browser manager."""
        self.instances: Dict[str, dict] = {}
        self.launcher = BrowserLauncher()
        
    def open_url(
        self,
        url: str,
        browser: Optional[str] = None,
        profile: Optional[str] = None,
    ) -> bool:
        """
        Open a URL in a browser.
        
        Args:
            url: URL to open
            browser: Browser to use
            profile: Browser profile to use
            
        Returns:
            bool: True if opened
        """
        if browser and profile:
            # Open with profile
            return self._open_with_profile(url, browser, profile)
            
        return self.launcher.open(url, browser)
        
    def _open_with_profile(self, url: str, browser: str, profile: str) -> bool:
        """
        Open URL with a specific browser profile.
        
        Args:
            url: URL to open
            browser: Browser command
            profile: Profile name
            
        Returns:
            bool: True if opened
        """
        try:
            if browser == "chrome" or browser == "google-chrome":
                subprocess.run([browser, f"--profile-directory={profile}", url])
                return True
            elif browser == "firefox":
                subprocess.run([browser, f"-P", profile, url])
                return True
            else:
                logger.warning(f"Profile not supported for {browser}")
                return self.launcher.open(url, browser)
        except Exception as e:
            logger.error(f"Failed to open with profile: {e}")
            return False
            
    def get_open_instances(self) -> Dict[str, dict]:
        """
        Get open browser instances.
        
        Returns:
            Dict[str, dict]: Open browser instances
        """
        # This would require more complex process tracking
        # For now, just return the stored instances
        return self.instances