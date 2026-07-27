#!/bin/bash

# Project Gamma Test Runner
# Automates the ingestion and query pipeline for testing purposes.

# Define absolute paths based on current environment
BASE_DIR="/app/projects/projectGamma"
ENV_DIR="$BASE_DIR/environments"
PYTHON_EXE="$ENV_DIR/.venv/bin/python"
SRC_DIR="$ENV_DIR/projects/projectGamma/src"
SAMPLE_DIR="$BASE_DIR/src"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   PROJECT GAMMA: AUTOMATED TEST RUN    ${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if python exists
if [ ! -f "$PYTHON_EXE" ]; then
    echo -e "${RED}Error: Python executable not found at $PYTHON_EXE${NC}"
    echo "Please ensure the virtual environment is created."
    exit 1
fi

# Step 1: Ingestion
echo -e "\n${BLUE}[1/3] Starting Ingestion...${NC}"
$PYTHON_EXE "$SRC_DIR/ingest.py" --mock "$SAMPLE_DIR/sample_history.txt" "$SAMPLE_DIR/sample_tech_spec.txt"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✔ Ingestion Successful!${NC}"
else
    echo -e "${RED}✘ Ingestion Failed!${NC}"
    exit 1
fi

# Step 2: Query History
echo -e "\n${BLUE}[2/3] Testing History Query...${NC}"
echo "Query: 'When was the Gamma constellation discovered?'"
$PYTHON_EXE "$SRC_DIR/query.py" --mock "When was the Gamma constellation discovered?"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✔ History Query Successful!${NC}"
else
    echo -e "${RED}✘ History Query Failed!${NC}"
    exit 1
fi

# Step 3: Query Tech Spec
echo -e "\n${BLUE}[3/3] Testing Tech Spec Query...${NC}"
echo "Query: 'What is the project architecture?'"
$PYTHON_EXE "$SRC_DIR/query.py" --mock "What is the project architecture?"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✔ Tech Spec Query Successful!${NC}"
else
    echo -e "${RED}✘ Tech Spec Query Failed!${NC}"
    exit 1
fi

echo -e "\n${BLUE}========================================${NC}"
echo -e "${GREEN}       ALL TESTS PASSED SUCCESSFULLY    ${NC}"
echo -e "${BLUE}========================================${NC}"
