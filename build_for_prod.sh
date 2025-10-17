#!/bin/bash
#
# Production Build Script
# -----------------------
# This script builds the React frontend and moves the compiled assets
# into the correct directories for the Flask backend to serve.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "✅ --- Starting Production Build Process ---"

# --- 1. Build the React Application ---
echo "📦 Building React assets..."
# Run build from within the frontend directory
(cd frontend && npm run build)

# --- 2. Define Target Directories ---
# This makes the script easier to read and modify.
FLASK_APP_DIR="app"
TEMPLATE_DIR="$FLASK_APP_DIR/templates"
STATIC_DIR="$FLASK_APP_DIR/static"
BUILD_SOURCE_DIR="frontend/dist"

# --- 3. Clean Previous Build Artifacts ---
echo "🧹 Cleaning old build files from Flask..."
# Ensure target directories exist before cleaning or moving files.
mkdir -p "$TEMPLATE_DIR"
mkdir -p "$STATIC_DIR"

# Remove old artifacts to prevent conflicts.
rm -f "$TEMPLATE_DIR/index.html"
rm -rf "$STATIC_DIR/assets"

# --- 4. Move New Build Artifacts ---
echo "🚚 Moving new build files to Flask directories..."
mv "$BUILD_SOURCE_DIR/index.html" "$TEMPLATE_DIR/"
mv "$BUILD_SOURCE_DIR/assets" "$STATIC_DIR/"

echo "🎉 --- Production build complete. Ready for deployment. ---"