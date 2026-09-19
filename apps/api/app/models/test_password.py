from app.core.security import verify_password

hashed = "$2b$12$fQuuODgacKD/9QTiy4zumePkYeDPd7turgsvD0YaWblQXA.rVa00a"

print(verify_password("admin123", hashed))