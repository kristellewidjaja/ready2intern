# Autonomous Build Workflow - [PROJECT-NAME]

This document tracks the progress of the autonomous build workflow.

## Workflow Status

<workflow-status>
```json
{
  "status": "ready",
  "message": "Ready to begin autonomous build",
  "processPid": null
}
```
</workflow-status>

---

## Status Values

- `ready`: Workflow hasn't started yet
- `in-progress`: Workflow is actively running
- `completed`: Workflow finished successfully
- `failed`: Workflow encountered an error

---

## Instructions for Kiro CLI Agent

Update the JSON block above with:
- **`status`**: Current workflow state (`ready` | `in-progress` | `completed` | `failed`)
- **`message`**: Brief user-facing message about current activity or result
- **`processPid`**: DO NOT MODIFY - This is managed by the extension

### Example Updates

**Progress update**:
```json
{
  "status": "in-progress",
  "message": "Building and deploying to AWS...",
  "processPid": 12345
}
```

**Note:** Only update `status` and `message`. Leave `processPid` unchanged.