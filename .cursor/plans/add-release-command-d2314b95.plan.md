<!-- d2314b95-022e-4af3-bdc8-78dd64534c48 6360e989-7f00-43e9-a15a-13d1bb8a9c72 -->
# Add Release Command to Makefile

## Changes to [`Makefile`](Makefile)

Add a new `release` target that:

1. **Validates version parameter** - Ensures the user provides a version argument (e.g., `make release version=0.2.0`)
2. **Runs all build checks** - Executes the existing `build` target (lint, typecheck, test)
3. **Creates git tag** - Creates a git tag with format `v{version}` (e.g., `v0.2.0`)
4. **Pushes tag to remote** - Pushes the newly created tag to the remote repository

## Implementation Details

The release target will:

- Check if version parameter is provided, error if missing
- Use the existing `build` target as a dependency to ensure all checks pass
- Create an annotated git tag with format `v$(version)` 
- Push the tag to origin using `git push origin v$(version)`
- Display success message with the created tag

The command will be used as: `make release version=x.y.z`

## Updates to help target

Update the `.PHONY` declaration and `help` target to include the new `release` command with usage instructions.

### To-dos

- [ ] Add 'release' to .PHONY declaration
- [ ] Implement release target with version validation, tag creation, and push
- [ ] Add release command documentation to help target