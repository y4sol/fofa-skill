#!/bin/bash
# Quick test script for FOFA CLI
# Run this before uploading to GitHub to ensure no errors

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== FOFA CLI Test Script ==="
echo ""

# Test 1: Help command
echo "[Test 1] Testing help command..."
python "$SCRIPT_DIR/fofa_query.py" --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Help command works"
else
    echo "❌ Help command failed"
    exit 1
fi

# Test 2: Import test
echo "[Test 2] Testing Python import..."
cd "$SCRIPT_DIR"
python -c "from fofa_query import FOFA, CVE_SIGNATURES, cve_lookup; print('✅ Import successful')" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Python import works"
else
    echo "❌ Python import failed"
    exit 1
fi

# Test 3: CVE lookup test
echo "[Test 3] Testing CVE lookup..."
python -c "
from fofa_query import cve_lookup
result = cve_lookup('redis')
if result and 'query' in result[0]:
    print('✅ CVE lookup works')
else:
    print('❌ CVE lookup failed')
    exit 1
" 2>/dev/null

# Test 4: FOFA class test
echo "[Test 4] Testing FOFA class..."
python -c "
from fofa_query import FOFA
print('✅ FOFA class loads correctly')
" 2>/dev/null

echo ""
echo "=== All tests passed! ==="
echo ""
echo "Ready to upload to GitHub!"
