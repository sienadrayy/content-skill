# FakeLocation Multi-Agent Development System

## Architecture

```
User Requirements
        ↓
   Orchestrator (You)
        ↓
  Project Manager Agent
        ↓
  Coding Agent
        ↓
  Codex (Code Executor)
        ↓
   QA Agent
        ↓
   Report to Orchestrator
```

## Agent Roles

### 1. **Project Manager Agent**
- Receives raw requirements from user
- Clarifies ambiguities
- Creates detailed specifications
- Defines acceptance criteria
- Produces: `REQUIREMENTS.md` for coding team

### 2. **Coding Agent**
- Receives detailed requirements
- Breaks into Codex tasks
- Coordinates with Codex for implementation
- Reviews code output
- Handles refactoring/fixes

### 3. **Codex (Code Executor)**
- Receives task list from Coding Agent
- Implements features in FakeLocation project
- Builds & compiles
- Commits changes to git

### 4. **QA Agent**
- Receives completed feature
- Tests functionality
- Reports bugs/issues
- Validates against requirements
- Produces: Test Report & Sign-off

### 5. **Orchestrator (Me)**
- Routes messages between agents
- Tracks progress
- Requests clarifications
- Escalates blockers
- Updates you with status

## Session Management

- Each agent runs in isolated session (sessions_spawn)
- Context passed via session messages (sessions_send)
- Status tracked in this file

## Workflow State

```
Status: READY FOR REQUIREMENTS
Current Stage: Awaiting user input
Active Agents: Initialized
Next Step: User provides requirements → PM Agent clarification
```

---

Generated: 2026-02-17 22:46 GMT+5:30
