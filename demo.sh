#!/bin/bash

echo "================================"
echo "GLA TIMETABLE GENERATOR DEMO"
echo "================================"
echo ""

echo "1. Generating timetable with sample data..."
echo "   Command: python main.py --sample --export-csv output/demo.csv"
echo ""
python main.py --sample --export-csv output/demo.csv --seed 123 2>&1 | tail -30

echo ""
echo "================================"
echo "2. Generated CSV file preview:"
echo "================================"
head -10 output/demo.csv
echo "..."
echo ""

echo "================================"
echo "3. Testing with custom config:"
echo "================================"
echo "   Command: python main.py --sample --config examples/config.json"
python main.py --sample --config examples/config.json --seed 123 2>&1 | head -20

echo ""
echo "================================"
echo "Demo completed successfully!"
echo "================================"
