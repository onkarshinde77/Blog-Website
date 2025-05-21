from werkzeug.security import generate_password_hash, check_password_hash

passd = 1234
passL = []
for i in range(1, 10):
    passL.append(generate_password_hash(str(passd)))
    
for i in passL:
    print(check_password_hash(i, str(passd)))