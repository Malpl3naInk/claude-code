# Building Claude Code Executable

This project can be built into two formats:
1. **JavaScript bundle** (~23 MB): Requires bun to run
2. **Native executable** (~133 MB): Standalone .exe/.bin file that can run directly

## Prerequisites

- [bun](https://bun.sh/) 1.3.11 or later

## Quick Start

### Build Native Executable (Recommended)

```bash
python build.py --format=native --test
```

This creates `dist/claude.exe` (Windows) or `dist/claude` (macOS/Linux) that can run directly:
```bash
dist/claude.exe --version
dist/claude.exe --help
```

### Build JavaScript Bundle

```bash
python build.py --format=js --test
```

Run with bun:
```bash
bun run dist/claude.js --version
```

## Build Options

### Python Build Script

```bash
python build.py [options]
```

Options:
- `--format, -f`: Build format
  - `native`: Standalone executable (default on Windows)
  - `js`: JavaScript bundle (default)
- `--output, -o`: Custom output path
- `--test, -t`: Run tests after build
- `--sourcemap`: Include source maps for debugging
- `--skip-checks`: Skip prerequisite checks

### Examples

```bash
# Build native executable with custom name
python build.py -f native -o ./claude-cli.exe

# Build JS bundle
python build.py -f js

# Build all formats
python build.py -f js && python build.py -f native
```

### Using bun directly

**JavaScript bundle:**
```bash
bun build --target=bun --outfile=dist/claude.js ./src/entrypoints/cli.tsx
```

**Native executable:**
```bash
bun build --compile --target=bun --outfile=dist/claude.exe ./src/entrypoints/cli.tsx
```

## Format Comparison

| Format | Size | Requirements | Use Case |
|--------|------|--------------|----------|
| JavaScript | ~23 MB | bun installed | Development, CI/CD |
| Native | ~133 MB | None | Distribution, end users |

## Architecture Notes

- The build uses `--target=bun` to preserve Node.js builtin module imports (like `child_process`, `async_hooks`, etc.)
- The `feature()` function in `src/_stubs/bun-bundle.ts` returns `false` for all features, which causes many code paths to be excluded from the build
- Stub files have been created for modules that are conditionally imported based on feature flags
- The `MACRO` global is defined at build time in `cli.tsx` since bun's preload doesn't apply to builds
- Native executables are created using bun's `--compile` flag which embeds the bun runtime
