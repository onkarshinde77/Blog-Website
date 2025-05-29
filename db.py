import firebase_admin
from firebase_admin import credentials,firestore

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

all_post = [
    {
      "image_link": "https://images.unsplash.com/photo-1555066931-4365d14bab8c",
      "Heading": "The Future of Artificial Intelligence",
      "description": "Explore how AI is transforming industries and what the future holds for this groundbreaking technology.",
      "read_more_link": "/blog/future-of-artificial-intelligence",
      "slug": "future-of-artificial-intelligence"
    },
    {
      "image_link": "https://images.unsplash.com/photo-1547658719-da2b51169166",
      "Heading": "Web Development Trends in 2024",
      "description": "Discover the latest trends in web development including new frameworks, tools, and best practices.",
      "read_more_link": "/blog/web-development-trends-2024",
      "slug": "web-development-trends-2024"
    },
    {
      "image_link": "https://images.unsplash.com/photo-1518770660439-4636190af475",
      "Heading": "Cybersecurity Essentials for Small Businesses",
      "description": "Protect your business from digital threats with these essential cybersecurity practices.",
      "read_more_link": "/blog/cybersecurity-for-small-businesses",
      "slug": "cybersecurity-for-small-businesses"
    },
    {
      "image_link": "https://images.unsplash.com/photo-1517430816045-df4b7de11d1d",
      "Heading": "Mobile App Development: Native vs Hybrid",
      "description": "Compare native and hybrid mobile app development approaches to choose the right one for your project.",
      "read_more_link": "/blog/native-vs-hybrid-app-development",
      "slug": "native-vs-hybrid-app-development"
    },
    {
      "image_link": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4",
      "Heading": "Cloud Computing for Beginners",
      "description": "An introduction to cloud computing concepts, services, and benefits for those just getting started.",
      "read_more_link": "/blog/cloud-computing-for-beginners",
      "slug": "cloud-computing-for-beginners"
    },
    {
      "image_link": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45",
      "Heading": "Data Science Career Path Explained",
      "description": "Learn about the skills, tools, and career opportunities in the growing field of data science.",
      "read_more_link": "/blog/data-science-career-path",
      "slug": "data-science-career-path"
    },
    {
      "image_link": "https://images.unsplash.com/photo-1516116216624-53e697fedbea",
      "Heading": "Blockchain Technology Fundamentals",
      "description": "Understand the core concepts of blockchain technology and how it's changing digital transactions.",
      "read_more_link": "/blog/blockchain-fundamentals",
      "slug": "blockchain-fundamentals"
    },
    {
      "image_link": "https://images.unsplash.com/photo-1518770660439-4636190af475",
      "Heading": "UI/UX Design Principles for Developers",
      "description": "Essential design principles every developer should know to create better user experiences.",
      "read_more_link": "/blog/ui-ux-principles-for-developers",
      "slug": "ui-ux-principles-for-developers"
    },
    {
      "image_link": "https://images.unsplash.com/photo-1551288049-bebda4e38f71",
      "Heading": "Machine Learning in Healthcare",
      "description": "How machine learning is revolutionizing healthcare with predictive analytics and personalized medicine.",
      "read_more_link": "/blog/machine-learning-in-healthcare",
      "slug": "machine-learning-in-healthcare"
    }
]

fetch_post = []

def create_post():
    for i in all_post:
        post = db.collection(u'blog_data').document()
        post.set(i)
    
def add_post(i,h,d,r,s):
    post = db.collection(u'blog_data').document()
    post.set({
        "image_link": i,
        "Heading": h,
        "description": d,
        "read_more_link": r,
        "slug": s
    })
    
def read_post():
    posts = db.collection(u'blog_data').stream()
    for post in posts:
        fetch_post.append(post.to_dict())

def get_post():    
    return fetch_post