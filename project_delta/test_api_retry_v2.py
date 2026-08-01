
import requests
import sys
import time

BASE_URL = "http://127.0.0.1:8000"

def wait_for_server(url, timeout=30):
    print(f"Waiting for server at {url}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            resp = requests.get(f"{url}/docs")
            if resp.status_code == 200:
                print("Server is UP!")
                return True
        except Exception:
            pass
        time.sleep(2)
    return False

def test_api():
    if not wait_for_server(BASE_URL):
        print("FAILURE: Server did not become available in time.")
        sys.exit(1)

    print("\n--- STARTING API INTEGRATION TEST ---")
    
    # 1. Create Category
    print("Step 1: Creating Category...")
    cat_payload = {"name": "Electronics", "description": "Gadgets and more"}
    resp = requests.post(f"{BASE_URL}/categories/", json=cat_payload)
    if resp.status_code not in [200, 201]:
        print(f"FAILURE: Could not create category. {resp.status_code} {resp.text}")
        sys.exit(1)
    category = resp.json()
    print(f"SUCCESS: Created Category ID {category['id']}")

    # 2. Create Product
    print("\nStep 2: Creating Product...")
    prod_payload = {
        "name": "Smart Watch",
        "description": "A high-end smartwatch",
        "price": 199.99,
        "image_url": "http://example.com/watch.jpg",
        "category_id": {category['id']},
        "is_featured": True
    }
    resp = requests.post(f"{BASE_URL}/products/", json=prod_payload)
    if resp.status_code not in [200, 201]:
        print(f"FAILURE: Could not create product. {resp.status_code} {resp.text}")
        sys.exit(1)
    product = resp.json()
    print(f"SUCCESS: Created Product ID {product['id']}")

    # 3. Query Products
    print("\nStep 3: Querying Products...")
    resp = requests.get(f"{BASE_URL}/products/?category_id={category['id']}")
    if resp.status_code != 200:
        print(f"FAILURE: Could not fetch products. {resp.status_code} {resp.text}")
        sys.exit(1)
    products = resp.json()
    print(f"SUCCESS: Found {len(products)} products in category.")

    # 4. Query Featured
    print("\nStep 4: Querying Featured Products...")
    resp = requests.get(f"{BASE_URL}/products/featured/")
    if resp.status_code != 200:
        print(f"FAILURE: Could not fetch featured products. {resp.status_code} {resp.text}")
        sys.exit(1)
    featured = resp.json()
    print(f"SUCCESS: Found {len(featured)} featured products.")

    print("\n--- ALL TESTS PASSED SUCCESSFULLY ---")

if __name__ == '__main__':
    test_api()
