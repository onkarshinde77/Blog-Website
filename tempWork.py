from flask import Flask
from db import create_post,create_user,get_user,get_post,read_post

app = Flask(__name__)

@app.route('/')
def index():
    read_post()
    return get_post()

if __name__ =="__main__":
    app.run(debug=True)








# from werkzeug.security import generate_password_hash, check_password_hash

# passd = 1234
# passL = []
# for i in range(1, 10):
#     passL.append(generate_password_hash(str(passd)))
    
# for i in passL:
#     print(check_password_hash(i, str(passd)))