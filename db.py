import firebase_admin
from firebase_admin import credentials,firestore , storage
import uuid

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred,
        {'storageBucket':'blog-website-84ade.firebasestorage.app'})
db = firestore.client()
bucket = storage.bucket()

def set_post(i,h,d,r,s):
  post = db.collection(u'blog_data').document()
  post.set({
      "image_link": i,
      "Heading": h,
      "description": d,
      "read_more_link": r,
      "slug": s
  })

def get_post():
  data = [] 
  post = db.collection(u'blog_data').stream()
  for p in post:
    data.append(p.to_dict())
  return data
  
def set_user(e,u,p):
  user = db.collection(u'users').document()
  user.set({"email": e,
          "name":u,
          "password":p,
          "avatar" :
            {
              "data":"https://img.freepik.com/premium-vector/user-profile-icon-flat-style-member-avatar-vector-illustration-isolated-background-human-permission-sign-business-concept_157943-15752.jpg?semt=ais_hybrid&w=740",
              "filename" : "demo.png"
            }
      })
    
# def get_user():
#   data = []
#   user = db.collection(u'users').stream()
#   for u in user:
#     data.append(u.to_dict())
#   return data

def get_user():
    data = []
    user = db.collection(u'users').stream()
    for u in user:
        user_dict = u.to_dict()
        user_dict['id'] = u.id
        data.append(user_dict)
    return data

def update_user(current_user):
  db.collection('users').document(current_user.id).update({
            'name': current_user.name,
            'email': current_user.email,
            'avatar': current_user.avatar
  })
def set_contact(n,m,e,d):
  contact = db.collection(u'contacts').document()
  contact.set({
    "name" : n,
    "mobile" : m,
    "email" : e,
    "description" : d
  })

def get_contact():
  data =[]
  contact = db.collection(u'contacts').stream()
  for c in contact:
    data.append(c.to_dict())
  return data

def upload_image_to_firebase(file, filename):
    b = bucket.blob(filename)
    b.upload_from_file(file.stream)
    b.make_public()
    url = b.public_url
    return url
  
def update_user_in_firebase(email, name, image_url=None):
    users = db.collection('users').stream()
    for user in users:
      if(user['email']==email):
        if image_url:
          user['avatar'] = image_url
          break

def delete_post(post_id):
    doc_ref = db.collection(u'blog_data').document(post_id)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.delete()
        return True
    else:
        return False



  
# all_post = [
#     {
#       "image_link": "https://images.unsplash.com/photo-1555066931-4365d14bab8c",
#       "Heading": "The Future of Artificial Intelligence",
#       "description": "Explore how AI is transforming industries and what the future holds for this groundbreaking technology.",
#       "read_more_link": "/blog/future-of-artificial-intelligence",
#       "slug": "future-of-artificial-intelligence"
#     },
#     {
#       "image_link": "https://images.unsplash.com/photo-1547658719-da2b51169166",
#       "Heading": "Web Development Trends in 2024",
#       "description": "Discover the latest trends in web development including new frameworks, tools, and best practices.",
#       "read_more_link": "/blog/web-development-trends-2024",
#       "slug": "web-development-trends-2024"
#     },
#     {
#       "image_link": "https://images.unsplash.com/photo-1518770660439-4636190af475",
#       "Heading": "Cybersecurity Essentials for Small Businesses",
#       "description": "Protect your business from digital threats with these essential cybersecurity practices.",
#       "read_more_link": "/blog/cybersecurity-for-small-businesses",
#       "slug": "cybersecurity-for-small-businesses"
#     },
#     {
#       "image_link": "https://images.unsplash.com/photo-1517430816045-df4b7de11d1d",
#       "Heading": "Mobile App Development: Native vs Hybrid",
#       "description": "Compare native and hybrid mobile app development approaches to choose the right one for your project.",
#       "read_more_link": "/blog/native-vs-hybrid-app-development",
#       "slug": "native-vs-hybrid-app-development"
#     },
#     {
#       "image_link": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4",
#       "Heading": "Cloud Computing for Beginners",
#       "description": "An introduction to cloud computing concepts, services, and benefits for those just getting started.",
#       "read_more_link": "/blog/cloud-computing-for-beginners",
#       "slug": "cloud-computing-for-beginners"
#     },
#     {
#       "image_link": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45",
#       "Heading": "Data Science Career Path Explained",
#       "description": "Learn about the skills, tools, and career opportunities in the growing field of data science.",
#       "read_more_link": "/blog/data-science-career-path",
#       "slug": "data-science-career-path"
#     },
#     {
#       "image_link": "https://images.unsplash.com/photo-1516116216624-53e697fedbea",
#       "Heading": "Blockchain Technology Fundamentals",
#       "description": "Understand the core concepts of blockchain technology and how it's changing digital transactions.",
#       "read_more_link": "/blog/blockchain-fundamentals",
#       "slug": "blockchain-fundamentals"
#     },
#     {
#       "image_link": "https://images.unsplash.com/photo-1518770660439-4636190af475",
#       "Heading": "UI/UX Design Principles for Developers",
#       "description": "Essential design principles every developer should know to create better user experiences.",
#       "read_more_link": "/blog/ui-ux-principles-for-developers",
#       "slug": "ui-ux-principles-for-developers"
#     },
#     {
#       "image_link": "https://images.unsplash.com/photo-1551288049-bebda4e38f71",
#       "Heading": "Machine Learning in Healthcare",
#       "description": "How machine learning is revolutionizing healthcare with predictive analytics and personalized medicine.",
#       "read_more_link": "/blog/machine-learning-in-healthcare",
#       "slug": "machine-learning-in-healthcare"
#     }
# ]
  
# def create_post():
#     for i in all_post:
#         post = db.collection(u'blog_data').document()
#         post.set(i)

# e = "shindeonkar704@gamil.com"
# u = "Sarkar"
# p = "scrypt:32768:8:1$8lfKvlwqobGQxZOc$9679c1a77d283820b8208004f535cb75ae99b477c531abb06ffb5bffa15ff7b0780c77950f2834191c426678c889cd90ee16556aa2f530c23edac2b76d851dd6"
# set_user(e,u,p)