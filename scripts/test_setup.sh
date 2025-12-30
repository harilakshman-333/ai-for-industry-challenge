#!/bin/bash
# Quick test script to verify Docker setup

set -e

echo "==================================="
echo "Testing AI for Industry Challenge"
echo "==================================="
echo ""

# Check if Docker is installed
echo "1. Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi
echo "✅ Docker is installed"

# Check if docker-compose is available
echo ""
echo "2. Checking docker-compose..."
if ! command -v docker-compose &> /dev/null; then
    echo "⚠️  docker-compose not found, trying 'docker compose'..."
    if ! docker compose version &> /dev/null; then
        echo "❌ Neither docker-compose nor 'docker compose' found!"
        exit 1
    fi
    echo "✅ Using 'docker compose'"
else
    echo "✅ docker-compose is installed"
fi

# Check if user is in docker group
echo ""
echo "3. Checking Docker permissions..."
if groups | grep -q docker; then
    echo "✅ User is in docker group"
else
    echo "⚠️  User is not in docker group"
    echo "You may need to run: sudo usermod -aG docker $USER"
    echo "Then log out and back in"
fi

# Check for X11 display
echo ""
echo "4. Checking X11 display..."
if [ -z "$DISPLAY" ]; then
    echo "⚠️  DISPLAY variable not set"
    echo "GUI applications may not work"
else
    echo "✅ DISPLAY is set to: $DISPLAY"
fi

# Check directory structure
echo ""
echo "5. Checking project structure..."
required_files=(
    "Dockerfile"
    "docker-compose.yml"
    "src/cable_insertion/package.xml"
    "src/cable_insertion/CMakeLists.txt"
)

all_files_exist=true
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
        all_files_exist=false
    fi
done

if [ "$all_files_exist" = false ]; then
    echo ""
    echo "❌ Some required files are missing!"
    exit 1
fi

echo ""
echo "==================================="
echo "✅ All checks passed!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Build Docker image: docker-compose build"
echo "2. Start container: docker-compose up -d"
echo "3. Enter container: docker exec -it ai_challenge_dev /bin/bash"
echo ""
echo "Or use the convenience script: ./scripts/run_docker.sh"
