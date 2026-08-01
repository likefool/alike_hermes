
import requests
import time
import sys
import subprocess
from pathlib import Path

API_URL = "http://127.0.0.1:8000"

def run_test_logic():
    print("\n--- STARTING INTEGRATION TEST ---")
    try:
        # 1. Create Category
        print("1. Creating Category...")
        cat_resp = requests.post(f"{API_URL}/categories/", json={"name": "Test Cat", "description": "Test Desc"})
        cat_resp.raise_for_status()
        cat_id = cat_resp.json()['id']
        print(f"   [SUCCESS] Category ID: {cat_id}")

        # 2. Create Product
        print("2. Creating Product...")
        prod_payload = {
            "name": "Test Product",
            "description": "Test Desc",
            "price": 49.99,
            "category_id": cat_id,
            "is_featured": True
        }
        prod_resp = requests.post(f"{API_URL}/products/", json=prod_payload)
        prod_resp.raise_for_status()
        prod_id = prod_resp.json()['id']
        print(f"   [SUCCESS] Product ID: {prod_id}")

        # 3. Verify List
        print("3. Verifying List...")
        list_resp = requests.get(f"{API_URL}/products/")
        list_resp.raise_for_status()
        products = list_resp.json()
        if any(p['id'] == prod_id for p in products):
            print("   [SUCCESS] Product found in listing.")
        else:
            print("   [FAILURE] Product not found in listing.")
            sys.exit(1)

        print("\n*** ALL TESTS PASSED! ***")
        return True
    except Exception as e:
        print(f"\n*** TEST FAILED: {e} ***")
        return False

if __name__ == '__main__':
    cmd = ["/app/projects/project_gamma/.venv/bin/python", "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--no-access-log"]
    print(f"Starting server: {' '.join(cmd)}")
    server_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    print("Waiting for server to become ready...")
    ready = False
    for i in range(20):
        time.sleep(2)
        try:
            r = requests.get(f"{API_URL}/docs", timeout=2)
            if r.status_code == 200:
                print(">>> Server is UP!")
                ready = True
                break
        except:
            print(f"   Attempt {i+1}: Waiting...")
            
    if ready:
        success = run_test_logic()
        if success:
            print("\n[FINAL RESULT] Integration Successful.")
        else:
            print("\n[FINAL RESULT] Integration Failed.")
        server_proc.terminate()
    else:
        print("Failed to start server.")
        server_proc.terminate()
