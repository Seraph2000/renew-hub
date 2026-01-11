#!/bin/bash

BASE="http://127.0.0.1:5000"

echo "=============================="
echo " HEALTH CHECK"
echo "=============================="
curl "$BASE/health"
echo -e "\n"

echo "=============================="
echo " SITES"
echo "=============================="
curl "$BASE/sites/"
echo -e "\n"

echo "Create site"
curl -X POST "$BASE/sites/" \
    -H "Content-Type: application/json" \
    -d '{"name":"Test Site","country":"UK","latitude":50.0,"longitude":0.0}'
echo -e "\n"

echo "=============================="
echo " ASSETS"
echo "=============================="
curl "$BASE/assets/"
echo -e "\n"

echo "Create asset"
curl -X POST "$BASE/assets/" \
    -H "Content-Type: application/json" \
    -d '{"name":"Turbine A","site_id":1}'
echo -e "\n"

echo "=============================="
echo " METRICS"
echo "=============================="
curl "$BASE/metrics/"
echo -e "\n"

echo "Metrics filtered"
curl "$BASE/metrics/?asset_id=1&start=2024-01-01&end=2024-01-31"
echo -e "\n"

echo "Metrics for asset"
curl "$BASE/metrics/asset/1"
echo -e "\n"

echo "=============================="
echo " ETL"
echo "=============================="