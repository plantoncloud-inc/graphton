<!-- 75d87cfd-eb26-4581-8d0d-d7d8f0c1a42c 853f21c6-84e8-4ed3-97e0-5ed1f7b1f201 -->
# Fix Test Async Methods

## Problem

The middleware now only implements async methods (`abefore_agent`, `aafter_agent`) after the critical timeout fix, but tests are still calling the old synchronous methods (`before_agent`, `after_agent`) which no longer exist. This causes all calls to silently do nothing, resulting in 10 test failures.

## Root Cause

From the changelog `2025-11-28-fix-mcp-timeout-async-middleware.md`:

- Synchronous `before_agent` and `after_agent` were **intentionally removed** to fix a production-blocking deadlock
- They were replaced with async versions `abefore_agent` and `aafter_agent`
- Tests were not updated to match this change

## Solution

Convert failing tests to async and update them to call the async middleware methods.

## Implementation

### 1. Update [`tests/test_mcp_remote.py`](tests/test_mcp_remote.py)

Convert 7 test methods from sync to async:

**Pattern to apply**:

```python
# BEFORE (sync)
def test_config_parameter_extraction(self) -> None:
    middleware.before_agent(state={}, runtime=config)

# AFTER (async)
async def test_config_parameter_extraction(self) -> None:
    await middleware.abefore_agent(state={}, runtime=config)
```

**Tests to update**:

- Line 20: `test_config_parameter_extraction` → `async def`, call `await middleware.abefore_agent(...)`
- Line 85: `test_missing_config_raises_clear_error` → `async def`, call `await middleware.abefore_agent(...)`
- Line 106: `test_missing_configurable_raises_clear_error` → `async def`, call `await middleware.abefore_agent(...)`
- Line 129: `test_missing_token_in_config` → `async def`, call `await middleware.abefore_agent(...)`
- Line 178: `test_idempotency_second_call_skips_loading` → `async def`, call `await middleware.abefore_agent(...)` (both calls)
- Line 216: `test_tool_cache_access` → `async def`, call `await middleware.abefore_agent(...)`
- Line 273: `test_get_nonexistent_tool_fails` → `async def`, call `await middleware.abefore_agent(...)`

### 2. Update [`tests/test_static_dynamic_mcp.py`](tests/test_static_dynamic_mcp.py)

Convert 3 test methods in the `TestDynamicConfigValidation` class from sync to async:

**Tests to update**:

- Line 137: `test_missing_template_value_error` → `async def`, call `await middleware.abefore_agent(...)`
- Line 155: `test_missing_multiple_template_values` → `async def`, call `await middleware.abefore_agent(...)`
- Line 180: `test_missing_configurable_dict` → `async def`, call `await middleware.abefore_agent(...)`

## Expected Results

- All 10 failing tests should pass
- Middleware methods are actually called and execute their logic
- Validation errors are properly raised
- Tools are properly loaded and cached
- No breaking changes to production code