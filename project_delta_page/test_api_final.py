
import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    try:
        print("1. Creating Category...")
        cat_resp = requests.post(f"{BASE_URL}/categories/", json={"name": "Electronics", "description": "Testing"})
        cat_resp.raise_for-status()
        cat_id = cat_resp.json()['id']
        print(f"   SUCCESS: Category ID: {cat_id}")

        print("2. Creating Product...")
        prod_payload = {
            "name": "Smartphone",
            "price": 599.99,
            "category_id": cat_id,
            "is_featured": True
        }
        prod_resp = requests.post(f"{BASE_URL}/products/", json=prod_payload)
        prod_resp.raise_for_status()
        print(f"   SUCCESS: Product ID: {prod_resp.json()['id']}")

        print("3. Verifying Product Listing...")
        list_resp = requests.get(f"{BASE_URL}/products/")
        list_resp.raise_for_status()
        products = list_resp.json()
        print(f"   SUCCESS: Found {len(products)} products.")
        
        print("\n*** ALL TESTS PASSED SUCCESSFULLY! ***")
    except Exception as e:
        print(f"\n*** TEST FAILED: {e} ***")
        sys.exit(1)

if __name__ == '__main__':
    test_api()
