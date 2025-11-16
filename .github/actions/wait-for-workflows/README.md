# Wait for Workflows

A composite GitHub Action that waits for specified workflows to complete before continuing execution. This is useful for ensuring mutual exclusion between workflows without blocking workflows from running concurrently with each other.

## Features

- ✅ Wait for multiple workflows to complete
- ✅ Configurable timeout and check intervals
- ✅ Non-blocking for workflows not in the wait list
- ✅ Detailed logging of workflow status
- ✅ Graceful error handling

## Usage

### Basic Example

```yaml
steps:
  - name: Checkout repository
    uses: actions/checkout@v4
  
  - name: Wait for template workflows
    uses: ./.github/actions/wait-for-workflows
    with:
      workflow_files: 'workflow-a.yml, workflow-b.yml, workflow-c.yml'
```

### With Custom Timeouts

```yaml
steps:
  - name: Wait for long-running workflow
    uses: ./.github/actions/wait-for-workflows
    with:
      workflow_files: 'deploy.yml'
      max_wait_minutes: 120
      check_interval_seconds: 60
```

### Complete Workflow Example

```yaml
name: Sync All Templates

on:
  workflow_dispatch:

jobs:
  sync-templates:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Wait for individual template workflows to complete
        uses: ./.github/actions/wait-for-workflows
        with:
          workflow_files: 'template-a.yml, template-b.yml, template-c.yml'
          max_wait_minutes: 60
          check_interval_seconds: 30
      
      - name: Sync all templates
        run: |
          echo "All template workflows completed, syncing..."
          # Your sync logic here
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `workflow_files` | Comma-separated list of workflow filenames to wait for (e.g., `workflow-a.yml, workflow-b.yml`) | Yes | - |
| `max_wait_minutes` | Maximum time to wait for workflows to complete (in minutes) | No | `60` |
| `check_interval_seconds` | How often to check workflow status (in seconds) | No | `30` |
| `github_token` | GitHub token for API access | No | `${{ github.token }}` |

## How It Works

1. The action queries the GitHub Actions API to check if any of the specified workflows are currently running
2. If any workflows are in progress, it waits for the specified check interval before checking again
3. Once all specified workflows have completed (or are not running), the action completes successfully
4. If workflows don't complete within the maximum wait time, the action fails with a timeout error

## Use Cases

### Mutual Exclusion Between Workflows

Prevent two workflows from running simultaneously while allowing other workflows to run freely:

**Workflow A** (can run anytime unless Workflow B is running):
```yaml
steps:
  - uses: actions/checkout@v4
  - uses: ./.github/actions/wait-for-workflows
    with:
      workflow_files: 'workflow-b.yml'
  - run: echo "Running A"
```

**Workflow B** (can run anytime unless Workflow A is running):
```yaml
steps:
  - uses: actions/checkout@v4
  - uses: ./.github/actions/wait-for-workflows
    with:
      workflow_files: 'workflow-a.yml'
  - run: echo "Running B"
```

### Coordinating Multiple Workflows

Wait for several related workflows to complete before starting a consolidation workflow:

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: ./.github/actions/wait-for-workflows
    with:
      workflow_files: 'build.yml, test.yml, lint.yml'
  - run: echo "All checks passed, deploying..."
```

## Requirements

- The action requires `actions: read` permission (typically granted by default with `GITHUB_TOKEN`)
- The workflow files must exist in `.github/workflows/` directory
- The `actions/github-script@v7` action must be available

## Troubleshooting

### Action times out

If the action consistently times out, consider:
- Increasing `max_wait_minutes`
- Checking if the workflows you're waiting for are stuck or have issues
- Verifying the workflow filenames are correct

### "Could not check workflow" warnings

These warnings occur when:
- A workflow file doesn't exist
- The workflow has never been run
- There are permission issues

The action will continue and only fail if it times out.

### Workflows not detecting each other

Make sure:
- Workflow filenames match exactly (including `.yml` extension)
- Both workflows have the wait step configured
- The `workflow_files` input uses the correct filenames

## Permissions

This action requires the following permissions:

```yaml
permissions:
  actions: read  # To query workflow run status
```

These are typically included by default with `GITHUB_TOKEN`.

## License

This action is provided as-is for use in your GitHub workflows.