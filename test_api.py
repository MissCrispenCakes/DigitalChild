#!/usr/bin/env python
# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Quick API health check script

Tests all endpoints and reports status.
Run with: python test_api.py
"""

import json
import sys

from api.app import create_app


def test_endpoint(client, name, url):
    """Test a single endpoint"""
    try:
        response = client.get(url)
        data = json.loads(response.data)

        if response.status_code == 200 and data["status"] == "success":
            # Get some sample info
            info = ""
            if "pagination" in data.get("data", {}):
                pag = data["data"]["pagination"]
                info = f"(total: {pag['total']}, items: {len(data['data']['items'])})"
            elif "indicators" in data.get("data", {}):
                info = f"(indicators: {len(data['data']['indicators'])})"

            print(f"  ✅ {name} {info}")
            return True
        else:
            print(f"  ❌ {name} - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ {name} - Error: {str(e)[:50]}")
        return False


def main():
    """Run all API tests"""
    print("\n" + "=" * 60)
    print("  DigitalChild API Health Check")
    print("=" * 60 + "\n")

    # Create test client
    app = create_app("development")
    client = app.test_client()

    # Get a document ID for testing
    response = client.get("/api/documents?per_page=1")
    data = json.loads(response.data)
    doc_id = data["data"]["items"][0]["id"] if data["data"]["items"] else "test"

    # Test all endpoints
    tests = [
        ("Health Check", "/api/health"),
        ("System Info", "/api/info"),
        ("Documents List", "/api/documents?per_page=5"),
        ("Documents Filter", "/api/documents?region=Africa&per_page=3"),
        (f"Document Detail ({doc_id})", f"/api/documents/{doc_id}"),
        ("Scorecard List", "/api/scorecard?per_page=5"),
        ("Scorecard Filter", "/api/scorecard?region=Africa&per_page=3"),
        ("Scorecard Country", "/api/scorecard/Kenya"),
        ("Indicator Statistics", "/api/scorecard/indicators/statistics"),
    ]

    results = []
    for name, url in tests:
        results.append(test_endpoint(client, name, url))

    # Summary
    passed = sum(results)
    total = len(results)

    print("\n" + "=" * 60)
    print(f"  Results: {passed}/{total} endpoints working")
    print("=" * 60 + "\n")

    if passed == total:
        print("🎉 All endpoints are healthy!\n")
        return 0
    else:
        print(f"⚠️  {total - passed} endpoint(s) failed\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
