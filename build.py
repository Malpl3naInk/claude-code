#!/usr/bin/env python3
"""
Build script for Claude Code - creates an executable using bun build.

Supports two output formats:
1. JavaScript bundle (--format=js): Smaller file, requires bun to run
2. Native executable (--format=native): Standalone .exe file

Usage:
    python build.py --format=native --test
    python build.py -f native -o claude.exe
"""
import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], cwd: str | None = None) -> tuple[int, str, str]:
    """Run a command and return (exit_code, stdout, stderr)."""
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd
    )
    return result.returncode, result.stdout, result.stderr


def check_bun() -> bool:
    """Check if bun is installed."""
    code, _, _ = run_command(['bun', '--version'])
    return code == 0


def get_default_output_name(format_type: str) -> str:
    """Get default output name based on format and platform."""
    if format_type == 'native':
        system = platform.system()
        if system == 'Windows':
            return 'dist/claude.exe'
        elif system == 'Darwin':
            return 'dist/claude'
        else:
            return 'dist/claude'
    return 'dist/claude.js'


def build_executable(
    outfile: str,
    format_type: str = 'js',
    sourcemap: bool = False
) -> bool:
    """Build the executable using bun build."""
    print(f"Building Claude Code ({format_type} format)...")
    print(f"Output: {outfile}")

    # Ensure output directory exists
    out_path = Path(outfile)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Base command
    cmd = [
        'bun', 'build',
        '--target=bun',
        f'--outfile={outfile}',
    ]

    # Add compile flag for native executable
    if format_type == 'native':
        cmd.append('--compile')

    # Add sourcemap if requested
    if sourcemap:
        cmd.append('--sourcemap')

    # Entry point
    cmd.append('./src/entrypoints/cli.tsx')

    code, stdout, stderr = run_command(cmd)

    if stdout:
        print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)

    if code != 0:
        print(f"Build failed with exit code {code}")
        return False

    # Check if output file was created
    if out_path.exists():
        size_mb = out_path.stat().st_size / (1024 * 1024)
        print(f"Build successful: {outfile} ({size_mb:.2f} MB)")
        return True
    else:
        print("Build failed: output file not created")
        return False


def test_executable(exe_path: str, format_type: str = 'js') -> bool:
    """Test the built executable."""
    print(f"\nTesting {exe_path}...")

    if format_type == 'native':
        # Native executable can run directly
        # Use absolute path to ensure it works on Windows
        abs_path = os.path.abspath(exe_path)
        run_cmd = [abs_path, '--version']
    else:
        # JS bundle needs bun
        run_cmd = ['bun', 'run', exe_path, '--version']

    # Test --version
    code, stdout, stderr = run_command(run_cmd)
    if code != 0:
        print(f"Version test failed: {stderr}")
        return False
    print(f"  Version: {stdout.strip()}")

    # Test --help
    if format_type == 'native':
        abs_path = os.path.abspath(exe_path)
        run_cmd = [abs_path, '--help']
    else:
        run_cmd = ['bun', 'run', exe_path, '--help']

    code, stdout, stderr = run_command(run_cmd)
    if code != 0:
        print(f"Help test failed: {stderr}")
        return False
    print("  Help command: OK")

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Build script for Claude Code executable',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build native executable (recommended)
  python build.py --format=native

  # Build JS bundle (smaller, requires bun)
  python build.py --format=js

  # Build and test
  python build.py --format=native --test

  # Custom output name
  python build.py -f native -o ./my-claude.exe
        """
    )
    parser.add_argument(
        '--output', '-o',
        help='Output path for the executable (default: depends on format)'
    )
    parser.add_argument(
        '--format', '-f',
        choices=['js', 'native'],
        default='js',
        help='Build format: js (JavaScript bundle) or native (standalone executable)'
    )
    parser.add_argument(
        '--test', '-t',
        action='store_true',
        help='Test the built executable'
    )
    parser.add_argument(
        '--skip-checks',
        action='store_true',
        help='Skip prerequisite checks'
    )
    parser.add_argument(
        '--sourcemap',
        action='store_true',
        help='Include source maps (for debugging)'
    )

    args = parser.parse_args()

    # Determine output path
    if args.output:
        outfile = args.output
    else:
        outfile = get_default_output_name(args.format)

    # Check prerequisites
    if not args.skip_checks:
        if not check_bun():
            print("Error: bun is not installed or not in PATH")
            print("Please install bun from https://bun.sh/")
            sys.exit(1)

        code, version, _ = run_command(['bun', '--version'])
        print(f"Found bun version: {version.strip()}")

    # Build
    if not build_executable(outfile, args.format, args.sourcemap):
        sys.exit(1)

    # Test
    if args.test:
        if not test_executable(outfile, args.format):
            sys.exit(1)
        print("\nAll tests passed!")

    # Print summary
    print("\n" + "="*50)
    print("Build complete!")
    print(f"Output: {outfile}")
    out_path = Path(outfile)
    if out_path.exists():
        size_mb = out_path.stat().st_size / (1024 * 1024)
        print(f"Size: {size_mb:.2f} MB")

    if args.format == 'native':
        print(f"\nRun directly: {outfile}")
    else:
        print(f"\nRun with: bun run {outfile}")


if __name__ == '__main__':
    main()
