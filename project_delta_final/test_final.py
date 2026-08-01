
import requests
import sys
import time

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("Testing API...")
    try:
        # 1. Create Category
        cat_resp = requests.post(f"{BASE_URL}/categories/", json={"name": "Test", "description": "Test"})
        cat_resp.raise_for_status()
        cat_id = cat_resp.json()['id']
        print(f"Created Category: {cat_id}")

        # 2. Create Product
        prod_payload = {
            "name": "Test Product",
            "price": 10.0,
            "category_id": cat_id,
            "is_featured": True
        }
        prod_resp = requests.post(f"{BASE_URL}/products/", json=prod_payload)
        prod_resp.raise_for_status()
        print("Created Product successfully.")

        # 3. Verify
        query_resp = requests.get(f"{BASE_URL}/products/?category_id={cat_id}")
        query_resp.raise_for_status()
        print(f"Found {len(query_resp.json())} products in category.")

        print("ALL TESTS PASSED!")
    except Exception as e:
        print(f"TEST FAILED: {e}")
        sys.exit(1)

if __name__ == '__main__':
    test_api()
