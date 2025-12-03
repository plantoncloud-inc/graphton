"""Sandbox backend factory for declarative configuration.

This module provides a factory function to create sandbox backend instances
from declarative configuration dictionaries, following the same pattern as
MCP server/tool configuration in Graphton.
"""

from __future__ import annotations

from typing import Any

from deepagents.backends.protocol import BackendProtocol  # type: ignore[import-untyped]


def create_sandbox_backend(config: dict[str, Any]) -> BackendProtocol:
    """Create sandbox backend from declarative configuration.
    
    This factory function instantiates appropriate backend implementations
    based on configuration dictionaries, enabling declarative agent setup
    without manual backend instantiation.
    
    Args:
        config: Sandbox configuration dictionary with required 'type' key.
            Supported types:
            - 'filesystem': Local filesystem with execution support
            - 'modal': Modal.com cloud sandbox (future)
            - 'runloop': Runloop cloud sandbox (future)
            - 'daytona': Daytona workspace sandbox (future)
            - 'harbor': LangGraph Cloud/Harbor (future)
    
    Returns:
        Configured backend instance implementing BackendProtocol.
        For 'filesystem' type, returns FilesystemBackend which provides file
        operations (read, write, edit, ls, glob, grep) but not terminal execution.
        The execute tool will be available but returns an error when called.
    
    Raises:
        ValueError: If config is missing 'type' key or type is unsupported.
        ValueError: If required configuration parameters are missing.
    
    Examples:
        Create filesystem backend for local execution:
        
        >>> config = {"type": "filesystem", "root_dir": "/workspace"}
        >>> backend = create_sandbox_backend(config)
        >>> # Agent will have execute tool enabled for shell commands
        
        Create filesystem backend with default root:
        
        >>> config = {"type": "filesystem"}
        >>> backend = create_sandbox_backend(config)
        >>> # Uses current working directory as root
    
    """
    if not isinstance(config, dict):
        raise ValueError(
            f"sandbox_config must be a dictionary, got {type(config).__name__}"
        )
    
    backend_type = config.get("type")
    
    if not backend_type:
        raise ValueError(
            "sandbox_config must include 'type' key. "
            "Supported types: filesystem, modal, runloop, daytona, harbor"
        )
    
    if backend_type == "filesystem":
        # Import only when needed to avoid hard dependencies
        from deepagents.backends import FilesystemBackend  # type: ignore[import-untyped]
        
        root_dir = config.get("root_dir", ".")
        return FilesystemBackend(root_dir=root_dir)
    
    elif backend_type == "modal":
        raise ValueError(
            "Modal sandbox support coming soon. "
            "For now, use 'filesystem' type for local execution."
        )
    
    elif backend_type == "runloop":
        raise ValueError(
            "Runloop sandbox support coming soon. "
            "For now, use 'filesystem' type for local execution."
        )
    
    elif backend_type == "daytona":
        raise ValueError(
            "Daytona sandbox support coming soon. "
            "For now, use 'filesystem' type for local execution."
        )
    
    elif backend_type == "harbor":
        raise ValueError(
            "Harbor sandbox support coming soon. "
            "For now, use 'filesystem' type for local execution."
        )
    
    else:
        raise ValueError(
            f"Unsupported sandbox type: {backend_type}. "
            f"Supported types: filesystem, modal, runloop, daytona, harbor"
        )

