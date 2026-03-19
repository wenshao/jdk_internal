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

### Contribution Statistics Principles

**IMPORTANT: Use GitHub Integrated PRs as the ONLY metric for contribution statistics.**

**Why NOT use git commits?**
- OpenJDK Committers use `@openjdk.org` email for commits
- Git commits by company email domain is inaccurate
- Many contributions are missed when filtering by company email
- GitHub PRs accurately reflect actual contributions

**Query Method:**
```
https://api.github.com/search/issues?q=repo:openjdk/jdk+author:{username}+type:pr+label:integrated
```

**Timeline Statistics:**
- Use PR merge date (`closed_at` field), NOT commit date
- Group by year for timeline visualization

**Example:**
```markdown
| 贡献者 | GitHub | PRs | 主要领域 |
|--------|--------|-----|----------|
| Shaojin Wen | @wenshao | 97 | 核心库优化 |
```

**Do NOT include:**
- Git commit counts
- Contributors without GitHub PRs
- Commit-based timelines

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