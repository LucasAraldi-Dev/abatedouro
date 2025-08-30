import asyncio
import sys
sys.path.append('.')

from fastapi.testclient import TestClient
from app.main import app

def test_endpoints():
    client = TestClient(app)
    
    print("Testando endpoint GET /api/v1/lotes-abate/")
    try:
        response = client.get("/api/v1/lotes-abate/")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error Response: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nTestando endpoint DELETE /api/v1/lotes-abate/68b226c713f66b77f3f1c4f1")
    try:
        response = client.delete("/api/v1/lotes-abate/68b226c713f66b77f3f1c4f1")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error Response: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_endpoints()