from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/blog_website"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Blogs_data(db.Model):
    Sr = db.Column(db.Integer, primary_key=True)
    image_link = db.Column(db.String(200), nullable=False)  # Increased from 20
    Heading = db.Column(db.String(100), nullable=False)    # Increased from 12
    description = db.Column(db.String(300), nullable=False) # Increased from 30
    read_more_link = db.Column(db.String(100), nullable=False)
    Slug = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, server_default=db.func.now())


demo_blogs = [
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


def add_demo_blogs():
    try:
        # First check if blogs already exist to avoid duplicates
        # existing_count = Blogs_data.query.count()
        # if existing_count > 0:
        #     print(f"Database already contains {existing_count} blogs. Skipping addition.")
        #     return

        for blog in demo_blogs:
            new_blog = Blogs_data(
                image_link=blog['image_link'],
                Heading=blog['Heading'],
                description=blog['description'],
                read_more_link=blog['read_more_link'],
                Slug=blog['slug']
            )
            db.session.add(new_blog)
        
        db.session.commit()
        print(f"Successfully added {len(demo_blogs)} demo blogs to database!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error adding demo blogs: {str(e)}")
        raise e

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Add demo blogs
        add_demo_blogs()