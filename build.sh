#!/bin/bash
# Cross-platform build script for SysProbe
# Builds binaries for Windows, macOS (Intel & Apple Silicon), Linux, and FreeBSD

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}SysProbe Cross-Platform Builder${NC}"
echo "======================================"

# Check if PyInstaller is installed
if ! python3 -m pip show pyinstaller > /dev/null 2>&1; then
    echo -e "${YELLOW}Installing PyInstaller...${NC}"
    pip3 install PyInstaller
fi

# Detect OS and architecture
OS=$(uname -s)
ARCH=$(uname -m)

case "$OS" in
    Linux)
        PLATFORM="linux"
        if [ "$ARCH" = "x86_64" ]; then
            ARCH_NAME="x86_64"
        elif [ "$ARCH" = "aarch64" ]; then
            ARCH_NAME="arm64"
        else
            ARCH_NAME="$ARCH"
        fi
        SPEC_FILE="build/linux-${ARCH_NAME}.spec"
        echo -e "${GREEN}Building for Linux ${ARCH_NAME}${NC}"
        ;;
    Darwin)
        PLATFORM="macos"
        if [ "$ARCH" = "arm64" ]; then
            ARCH_NAME="apple-silicon"
        elif [ "$ARCH" = "x86_64" ]; then
            ARCH_NAME="intel"
        else
            ARCH_NAME="$ARCH"
        fi
        SPEC_FILE="build/macos-${ARCH_NAME}.spec"
        echo -e "${GREEN}Building for macOS ${ARCH_NAME}${NC}"
        ;;
    FreeBSD)
        PLATFORM="freebsd"
        if [ "$ARCH" = "amd64" ]; then
            ARCH_NAME="x86_64"
        else
            ARCH_NAME="$ARCH"
        fi
        SPEC_FILE="build/freebsd-${ARCH_NAME}.spec"
        echo -e "${GREEN}Building for FreeBSD ${ARCH_NAME}${NC}"
        ;;
    *)
        echo -e "${RED}Unsupported OS: $OS${NC}"
        exit 1
        ;;
esac

# Ensure build directory exists
mkdir -p build dist

# Create spec file if it doesn't exist
if [ ! -f "$SPEC_FILE" ]; then
    echo -e "${YELLOW}Generating spec file: $SPEC_FILE${NC}"
    pyinstaller --onefile --windowed --name=SysProbe main.py --specpath=build -p . 2>/dev/null || true
    mv build/CPU-Z-Clone.spec "$SPEC_FILE" 2>/dev/null || mv build/SysProbe.spec "$SPEC_FILE" 2>/dev/null || true
fi

# Build the executable
echo -e "${YELLOW}Building executable...${NC}"
pyinstaller "$SPEC_FILE" --distpath dist --workpath build/build

# Determine output location
case "$PLATFORM" in
    linux)
        OUTPUT="dist/SysProbe-linux-${ARCH_NAME}"
        ;;
    macos)
        OUTPUT="dist/SysProbe-macos-${ARCH_NAME}"
        ;;
    freebsd)
        OUTPUT="dist/SysProbe-freebsd-${ARCH_NAME}"
        ;;
esac

# Rename the executable
if [ -f "dist/SysProbe" ]; then
    mv "dist/SysProbe" "$OUTPUT"
    chmod +x "$OUTPUT"
    echo -e "${GREEN}✓ Build complete!${NC}"
    echo -e "${GREEN}Executable: $OUTPUT${NC}"
else
    echo -e "${RED}✗ Build failed${NC}"
    exit 1
fi

