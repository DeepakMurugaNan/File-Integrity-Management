import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fim_project.settings')
django.setup()

from dashboard.utils import calculate_file_hash

# Create a dummy file
test_file = 'test_hash.txt'
with open(test_file, 'w') as f:
    f.write('Hello FIM!')

# Calculate hash
h = calculate_file_hash(test_file)
print(f"File: {test_file}")
print(f"Content: 'Hello FIM!'")
print(f"SHA-256: {h}")

# Verify against expected hash for "Hello FIM!"
# Expected: e0567f12258ea233b8a8b13d2894b9f0a2df25032b49c0617514fa613867664b
expected = 'e0567f12258ea233b8a8b13d2894b9f0a2df25032b49c0617514fa613867664b'
if h == expected:
    print("SUCCESS: Hash matches!")
else:
    print(f"FAILURE: Expected {expected}")

# Clean up
os.remove(test_file)
