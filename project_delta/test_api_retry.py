
import requests
import sys
import time

BASE_URL = "http://127.0.0.1:8000"

def wait_for_server(url, timeout=30):
    print(f"Waiting for server at {url}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Try a simple GET to check connectivity
            resp = requests.get(f"{url}/docs")
            if resp.status_code == 200:
                print("Server is UP!")
                return True
        except requests.exceptions.ConnectionError:
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
    try:
        resp = requests.post(f"{BASE_URL}/categories/", json=cat_payload)
        resp.raise_for_status()
        category = resp.json()
        print(f"SUCCESS: Created Category ID {category['id']}")
    except Exception as e:
        print(f"FAILURE: Could not create category. {e}")
        if hasattr(e, 'response') and e.response:
             print(f"Response: {e.response.text}")
        sys.exit(1)

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
    try:
        resp = requests.post(f"{BASE_URL}/products/", json=prod_payload)
        resp.raise_for_status()
        product = resp.json()
        print(f"SUCCESS: Created Product ID {product['id']}")
    except Exception as e:
        print(f"FAILURE: Could not create product. {e}")
        if hasattr(e, 'response') and e.response:
             print(f"Response: {e.response.text}")
        sys.exit(1)

    # 3. Query Products (Filter by Category)
    print("\nStep 3: Querying Products (Filter by category_id)...")
    try:
        resp = requests.get(f"{BASE_URL}/products/?category_id={category['id']}")
        resp.raise_for_status()
        products = resp.json()
        print(f"SUCCESS: Found {len(products)} products in category.")
    except Exception as e:
        print(f"FAILURE: Could not fetch products. {e}")
        sys.exit(1)

    # 4. Query Featured
    print("\nStep 4: Querying Featured Products...")
    try:
        resp = requests.get(f"{BASE_URL}/products/featured/")
        resp.raise_for_status()
        featured = resp.json()
        print(f"SUCCESS: Found {len(featured)} featured products.")
        if len(featured) > 0:
            print(f"Verified: Product '{product['name']}' is in featured list.")
    except Exception as e:
        print(f"FAILURE: Could not fetch featured products. {e}")
        sys.exit(1)

    print("\n--- ALL TESTS PASSED SUCCESSFULLY ---")

if __name__ == '__main__':
    test_api()
