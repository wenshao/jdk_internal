## Agent Context

- `../jdk` is the JDK source code repository
- This project analyzes JDK issues, pull requests, and source code to create documentation that is easy for both humans and AI to read

## Project Structure

```
jdk_internal/
├── AGENTS.md              # Agent context (this file)
├── README.md              # Project overview
├── releases/              # Release analysis (jdk26.md)
├── jeps/                  # JEP detailed analysis (21 files)
├── deep-dive/             # Implementation deep-dive (5 files)
├── guides/                # User guides (4 files)
├── issues/                # Issue analysis (4 files)
├── prs/                   # PR analysis (3 files)
├── contributors/          # Contributor profiles (34 files)
└── modules/               # Module/component analysis (4 files)
```

## Documentation Standards

### JEP Documents
- Background and motivation
- Usage examples
- Implementation analysis
- Developer impact
- Performance data

### Issue Documents
- Overview and severity
- Problem description
- Root cause analysis
- Solution details
- Code changes
- Testing verification

### Contributor Documents
- Basic information
- Contribution statistics
- PR list with links
- Key contributions explained
- Code examples
- Development style

### Module Documents
- Module overview
- Package structure
- Core class analysis
- JDK 26 changes
- Performance characteristics
- Usage examples

## Output Language

Prefer responding in **English** for normal assistant messages and explanations.

Keep technical artifacts unchanged:
- Code blocks, CLI commands, file paths
- Stack traces, logs, JSON keys
- Identifiers and exact quoted text