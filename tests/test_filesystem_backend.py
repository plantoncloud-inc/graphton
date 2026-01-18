"""Tests for FilesystemBackend with execution support."""

import tempfile
from pathlib import Path

import pytest

from graphton.core.backends import FilesystemBackend


class TestFilesystemBackend:
    """Test suite for FilesystemBackend execution capabilities."""
    
    def test_execute_simple_command(self) -> None:
        """Test basic command execution with stdout capture."""
        with tempfile.TemporaryDirectory() as tmpdir:
            backend = FilesystemBackend(root_dir=tmpdir)
            result = backend.execute("echo 'Hello World'")
            
            assert result.exit_code == 0
            assert "Hello World" in result.stdout
            assert result.stderr == ""
    
    def test_execute_with_exit_code(self) -> None:
        """Test that non-zero exit codes are captured correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            backend = FilesystemBackend(root_dir=tmpdir)
            result = backend.execute("exit 42")
            
            assert result.exit_code == 42
    
    def test_execute_with_stderr(self) -> None:
        """Test stderr capture for commands that write to stderr."""
        with tempfile.TemporaryDirectory() as tmpdir:
            backend = FilesystemBackend(root_dir=tmpdir)
            result = backend.execute("echo 'error message' >&2")
            
            assert result.exit_code == 0
            assert "error message" in result.stderr
    
    def test_execute_in_workspace_directory(self) -> None:
        """Test that commands execute in the correct workspace directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            backend = FilesystemBackend(root_dir=tmpdir)
            
            # Create a file in the workspace
            test_file = Path(tmpdir) / "test.txt"
            test_file.write_text("test content")
            
            # Command should be able to access the file
            result = backend.execute("cat test.txt")
            
            assert result.exit_code == 0
            assert "test content" in result.stdout
    
    def test_execute_with_timeout(self) -> None:
        """Test that commands timeout after specified duration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            backend = FilesystemBackend(root_dir=tmpdir)
            
            # Command that sleeps longer than timeout
            result = backend.execute("sleep 10", timeout=1)
            
            assert result.exit_code == 124  # Standard timeout exit code
            assert "timed out" in result.stderr.lower()
    
    def test_execute_invalid_command(self) -> None:
        """Test error handling for invalid commands."""
        with tempfile.TemporaryDirectory() as tmpdir:
            backend = FilesystemBackend(root_dir=tmpdir)
            
            # Non-existent command
            result = backend.execute("nonexistent_command_xyz123")
            
            # Should return error exit code, not raise exception
            assert result.exit_code != 0
    
    def test_execute_preserves_environment(self) -> None:
        """Test that environment variables are inherited."""
        import os
        
        with tempfile.TemporaryDirectory() as tmpdir:
            backend = FilesystemBackend(root_dir=tmpdir)
            
            # Set a test environment variable
            test_key = "TEST_GRAPHTON_ENV_VAR"
            test_value = "test_value_123"
            os.environ[test_key] = test_value
            
            try:
                result = backend.execute(f"echo ${test_key}")
                assert result.exit_code == 0
                assert test_value in result.stdout
            finally:
                # Cleanup
                del os.environ[test_key]
    
    def test_file_operations(self) -> None:
        """Test basic file operation methods."""
        with tempfile.TemporaryDirectory() as tmpdir:
            backend = FilesystemBackend(root_dir=tmpdir)
            
            # Write file
            backend.write_file("test.txt", "Hello, World!")
            
            # Read file
            content = backend.read_file("test.txt")
            assert content == "Hello, World!"
            
            # List files
            files = backend.list_files()
            assert "test.txt" in files
    
    def test_workspace_directory_creation(self) -> None:
        """Test that workspace directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create path to non-existent directory
            workspace = Path(tmpdir) / "workspace" / "subdir"
            
            # Should create the directory
            backend = FilesystemBackend(root_dir=workspace)
            
            assert workspace.exists()
            assert workspace.is_dir()


class TestExecutionResult:
    """Test ExecutionResult dataclass."""
    
    def test_execution_result_creation(self) -> None:
        """Test creating ExecutionResult instances."""
        from graphton.core.backends.filesystem import ExecutionResult
        
        result = ExecutionResult(
            exit_code=0,
            stdout="output",
            stderr="",
        )
        
        assert result.exit_code == 0
        assert result.stdout == "output"
        assert result.stderr == ""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
