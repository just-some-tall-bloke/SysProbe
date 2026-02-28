#!/bin/bash
# Master build script for all platforms
# This script documents how to build each platform

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}SysProbe - All Platforms Build Guide${NC}"
echo "=========================================="
echo ""
echo "To build for all platforms, run these commands on each system:"
echo ""
echo -e "${GREEN}Linux (x86_64):${NC}"
echo "  ./build.sh"
echo ""
echo -e "${GREEN}macOS (Intel):${NC}"
echo "  ./build.sh"
echo ""
echo -e "${GREEN}macOS (Apple Silicon):${NC}"
echo "  ./build.sh"
echo ""
echo -e "${GREEN}FreeBSD:${NC}"
echo "  ./build.sh"
echo ""
echo -e "${GREEN}Windows (x86_64):${NC}"
echo "  build.bat"
echo ""
echo -e "${GREEN}Or use GitHub Actions/CI to build all at once${NC}"
echo ""
echo "Building for current platform..."
./build.sh
