#!/bin/bash
# Git Configuration Script for Codespace
# Runs automatically on container creation

echo "🔧 Configuring Git for nRF52840 Development..."

# Set file mode to false (prevents permission change noise in containers)
git config --local core.fileMode false

# Set default branch name
git config --local init.defaultBranch main

# Enable color output
git config --local color.ui auto

# Set up useful aliases
git config --local alias.st "status -sb"
git config --local alias.co "checkout"
git config --local alias.br "branch"
git config --local alias.last "log -1 HEAD"
git config --local alias.unstage "reset HEAD --"

# Configure line endings (LF for consistency)
git config --local core.autocrlf input

# Set up commit template (optional)
if [ -f .gitmessage ]; then
    git config --local commit.template .gitmessage
fi

echo "✅ Git configured successfully!"
echo ""
echo "Useful aliases:"
echo "  git st      → Short status"
echo "  git last    → Show last commit"
echo "  git unstage → Unstage files"
echo ""
