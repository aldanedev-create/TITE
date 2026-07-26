"""
Blueprint builder for Tite.

This module handles building projects from blueprints, including
creating files, running commands, and managing dependencies.
"""

import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from tite.blueprint.parser import BlueprintParser, BlueprintVariableParser
from tite.blueprint.templates import BlueprintTemplateEngine
from tite.blueprint.validator import BlueprintValidator
from tite.core.filesystem import FileSystemManager
from tite.core.process import ProcessManager
from tite.core.installer import PackageInstaller
from tite.exceptions import ConfigurationError, FileOperationError


class BlueprintBuilder:
    """
    Builds projects from blueprints.
    
    This class handles the complete blueprint build process including
    parsing, validation, variable substitution, file creation, and
    command execution.
    
    Attributes:
        blueprint: The blueprint definition
        variables: Variables for substitution
        file_manager: Filesystem manager
        process_manager: Process manager
        installer: Package installer
        template_engine: Template engine
        validator: Blueprint validator
    """
    
    def __init__(
        self,
        project_path: Path,
        blueprint: Optional[Dict[str, Any]] = None,
        variables: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the blueprint builder.
        
        Args:
            project_path: Path where the project will be built
            blueprint: Blueprint definition
            variables: Variables for substitution
        """
        self.project_path = Path(project_path)
        self.blueprint = blueprint or {}
        self.variables = variables or {}
        
        self.file_manager = FileSystemManager(project_path)
        self.process_manager = ProcessManager(project_path)
        self.installer = PackageInstaller(project_path)
        self.template_engine = BlueprintTemplateEngine()
        self.validator = BlueprintValidator()
        self.parser = BlueprintParser()
        self.variable_parser = BlueprintVariableParser(self.variables)
        
    def build(self, blueprint: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Build the project from the blueprint.
        
        Args:
            blueprint: Blueprint definition (overrides instance blueprint)
            
        Returns:
            Dict[str, Any]: Build results
            
        Raises:
            ConfigurationError: If blueprint is invalid
            FileOperationError: If file operations fail
        """
        if blueprint:
            self.blueprint = blueprint
            
        # Validate blueprint
        if not self.validator.validate(self.blueprint):
            errors = self.validator.get_errors()
            raise ConfigurationError(f"Invalid blueprint: {', '.join(errors)}")
            
        # Parse variables
        self._parse_variables()
        
        # Build the project
        results = {
            "created_dirs": [],
            "created_files": [],
            "installed_packages": [],
            "executed_commands": [],
        }
        
        # Create directories
        dirs = self.blueprint.get("directories", [])
        for dir_path in dirs:
            full_path = self.project_path / dir_path
            self.file_manager.create_directory(full_path, exist_ok=True)
            results["created_dirs"].append(str(full_path))
            
        # Create files
        files = self.blueprint.get("files", {})
        for file_path, content in files.items():
            full_path = self.project_path / file_path
            
            # Substitute variables
            content = self.variable_parser.parse_variables(content)
            
            # Render template if needed
            if self._is_template(content):
                content = self.template_engine.render(
                    content,
                    self.variables
                )
                
            self.file_manager.write_file(full_path, content)
            results["created_files"].append(str(full_path))
            
        # Copy template files
        template_files = self.blueprint.get("template_files", [])
        for template_ref in template_files:
            self._copy_template_file(template_ref, results)
            
        # Install packages
        packages = self.blueprint.get("packages", [])
        if packages:
            self.installer.install_packages(packages)
            results["installed_packages"] = packages
            
        # Execute commands
        commands = self.blueprint.get("commands", [])
        for cmd in commands:
            result = self._execute_command(cmd)
            results["executed_commands"].append(result)
            
        return results
        
    def _parse_variables(self) -> None:
        """
        Parse and merge variables.
        """
        # Get blueprint variables
        blueprint_vars = self.blueprint.get("variables", {})
        
        # Merge with provided variables
        self.variables = {**blueprint_vars, **self.variables}
        
        # Add default variables
        import datetime
        import getpass
        import os
        
        default_vars = {
            "project_name": self.project_path.name,
            "project_path": str(self.project_path),
            "current_year": datetime.datetime.now().year,
            "current_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "user": os.environ.get("USER", getpass.getuser()),
            "hostname": os.environ.get("HOSTNAME", "localhost"),
        }
        
        self.variables = {**default_vars, **self.variables}
        self.variable_parser.add_variables(self.variables)
        
    def _is_template(self, content: str) -> bool:
        """
        Check if content is a template.
        
        Args:
            content: Content to check
            
        Returns:
            bool: True if content is a template
        """
        return "{{" in content or "{%" in content
        
    def _copy_template_file(self, template_ref: Union[str, Dict[str, str]], results: Dict) -> None:
        """
        Copy a template file.
        
        Args:
            template_ref: Template reference (path or dict with source/dest)
            results: Results dictionary
        """
        if isinstance(template_ref, str):
            # Simple template path
            source = template_ref
            dest = template_ref
        else:
            # Dict with source and dest
            source = template_ref.get("source", "")
            dest = template_ref.get("dest", source)
            
        source_path = Path(source)
        dest_path = self.project_path / dest
        
        if source_path.exists():
            # Copy the file
            shutil.copy2(source_path, dest_path)
            
            # Process as template if needed
            if self._is_template(dest_path.read_text()):
                content = dest_path.read_text()
                content = self.variable_parser.parse_variables(content)
                content = self.template_engine.render(content, self.variables)
                dest_path.write_text(content)
                
            results["created_files"].append(str(dest_path))
            
    def _execute_command(self, cmd: Union[str, List[str]]) -> Dict[str, Any]:
        """
        Execute a command.
        
        Args:
            cmd: Command to execute
            
        Returns:
            Dict[str, Any]: Command result
        """
        if isinstance(cmd, str):
            cmd = [cmd]
            
        # Substitute variables in command
        cmd = [self.variable_parser.parse_variables(c) for c in cmd]
        
        # Execute the command
        result = self.process_manager.run(
            cmd,
            capture_output=True,
            check=False,
        )
        
        return {
            "command": " ".join(cmd),
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
        
    def build_from_file(self, blueprint_path: Path) -> Dict[str, Any]:
        """
        Build a project from a blueprint file.
        
        Args:
            blueprint_path: Path to the blueprint file
            
        Returns:
            Dict[str, Any]: Build results
            
        Raises:
            ConfigurationError: If blueprint file is invalid
        """
        blueprint = self.parser.parse_file(blueprint_path)
        return self.build(blueprint)
        
    def build_from_string(self, content: str, format: str = "yaml") -> Dict[str, Any]:
        """
        Build a project from a blueprint string.
        
        Args:
            content: Blueprint content
            format: Format of the content
            
        Returns:
            Dict[str, Any]: Build results
            
        Raises:
            ConfigurationError: If blueprint is invalid
        """
        blueprint = self.parser.parse_string(content, format)
        return self.build(blueprint)