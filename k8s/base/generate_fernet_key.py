
from cryptography.fernet import Fernet

# Generate a new Fernet key
fernet_key = Fernet.generate_key()

print("=" * 70)
print("AIRFLOW FERNET KEY GENERATED")
print("=" * 70)
print()
print("Your Fernet Key:")
print(fernet_key.decode())
print()
print("Copy this key and update it in:")
print("  - k8s/base/02-secrets.yaml (for Kubernetes)")
print()
print(" IMPORTANT: Keep this key safe!")
print("   - Don't commit it to Git")
print("   - Use the same key if you backup/restore Airflow")
print("=" * 70)