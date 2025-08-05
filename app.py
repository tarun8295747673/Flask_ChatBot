from flask import Flask, request, jsonify, render_template
import re
from datetime import datetime

app = Flask(__name__)

# CodroidHub Assistant Bot Knowledge Base
codroidhub_knowledge = {
    # Home & Welcome
    "welcome": {
        "keywords": ["hello", "hi", "hey", "start", "welcome", "help"],
        "response": "Welcome to CodroidHub! I'm your assistant bot. I can help you with:\n\n Courses & Trainings\n Workshops & Events\n Internship & Career\n Services for Colleges\n Technical Services\n Contact Support\n\nWhat would you like to know about?"
    },
    
    # Courses & Trainings
    "courses": {
        "keywords": ["course", "training", "learn", "study", "curriculum", "syllabus"],
        "response": "CodroidHub offers comprehensive courses in:\n\n Full Stack Development (6 months) - ₹25,000\n Game Development (4 months) - ₹20,000\n AI & IoT (5 months) - ₹30,000\n Cybersecurity (6 months) - ₹35,000\n\nAll courses include:\n✅ Hands-on projects\n✅ Industry mentorship\n✅ Placement assistance\n✅ Certificate\n\nType 'enrollment' for registration process or 'syllabus' to download course materials!"
    },
    
    "full_stack": {
        "keywords": ["full stack", "web development", "frontend", "backend", "react", "node"],
        "response": "Full Stack Development Course:\n\n Duration: 6 months\n Fee: ₹25,000\n Next batch: Starting this month\n\nWhat you'll learn:\n• HTML, CSS, JavaScript\n• React.js & Node.js\n• Database management\n• API development\n• Deployment & hosting\n\nIncludes 3 major projects and internship opportunity!"
    },
    
    "game_development": {
        "keywords": ["game development", "unity", "gaming", "game design"],
        "response": "Game Development Course:\n\n Duration: 4 months\n Fee: ₹20,000\n Engine: Unity 3D\n\nCurriculum covers:\n• Game design principles\n• C# programming\n• 2D & 3D game creation\n• Animation & physics\n• Game publishing\n\nBuild 5+ games during the course!"
    },
    
    "ai_iot": {
        "keywords": ["ai", "artificial intelligence", "iot", "machine learning", "python"],
        "response": "AI & IoT Course:\n\n Duration: 5 months\n Fee: ₹30,000\n Hot in demand!\n\nTopics include:\n• Python programming\n• Machine Learning\n• Deep Learning\n• IoT hardware integration\n• Real-world projects\n\nHands-on with Arduino, Raspberry Pi, and AI frameworks!"
    },
    
    "cybersecurity": {
        "keywords": ["cybersecurity", "security", "ethical hacking", "penetration testing"],
        "response": "Cybersecurity Course:\n\n Duration: 6 months\n Fee: ₹35,000\n Industry certified\n\nSpecializations:\n• Ethical hacking\n• Network security\n• Digital forensics\n• Risk assessment\n• Security auditing\n\nGet certified and job-ready in cybersecurity!"
    },
    
    # Workshops & Events
    "workshops": {
        "keywords": ["workshop", "event", "seminar", "webinar", "upcoming"],
        "response": "Upcoming Workshops & Events:\n\n This Month:\n• Web Development Bootcamp - Jan 15\n• AI Workshop - Jan 20\n• Cybersecurity Seminar - Jan 25\n• Game Development Meet - Jan 30\n\n Next Month:\n• Full Stack Masterclass\n• IoT Innovation Workshop\n\nAll workshops are FREE for students! Register now: contact@codroidhub.com"
    },
    
    # Internship & Career
    "internship": {
        "keywords": ["internship", "job", "career", "placement", "work", "hiring"],
        "response": "Internship & Career Opportunities:\n\n Available Positions:\n• Full Stack Developer Intern\n• Game Developer Intern\n• AI/ML Intern\n• Cybersecurity Analyst Intern\n\n Requirements:\n• Course completion or ongoing\n• Portfolio/projects\n• Technical interview\n\n Benefits:\n• Stipend provided\n• Real project experience\n• Mentorship\n• Job conversion opportunity\n\nApply now: careers@codroidhub.com"
    },
    
    # Services for Colleges
    "college_services": {
        "keywords": ["college", "university", "academic", "partnership", "faculty", "guest lecture"],
        "response": "Services for Educational Institutions:\n\n Academic Partnerships:\n• Curriculum development\n• Student training programs\n• Industry exposure\n\n Faculty Services:\n• Guest lectures\n• Faculty training\n• Technical workshops\n\n Placement Support:\n• Campus recruitment\n• Interview preparation\n• Industry connections\n\nContact: partnerships@codroidhub.com"
    },
    
    # Learning Management System
    "lms": {
        "keywords": ["lms", "learning management", "student portal", "online learning"],
        "response": "CodroidHub Learning Management System:\n\n Features:\n• Online course materials\n• Video lectures\n• Assignment submission\n• Progress tracking\n• Discussion forums\n\n Access:\n• Student login: student.codroidhub.com\n• Faculty login: faculty.codroidhub.com\n\n Available on mobile and desktop\n 24/7 technical support"
    },
    
    # Technical Services
    "technical_services": {
        "keywords": ["technical service", "development", "web development", "mobile app", "bot development"],
        "response": "CodroidHub Technical Services:\n\n Web & Mobile Development:\n• Custom websites\n• Mobile applications\n• E-commerce solutions\n\n Game Development:\n• Mobile games\n• PC games\n• Game consulting\n\n Cybersecurity Solutions:\n• Security audits\n• Penetration testing\n• Security consulting\n\n BOT Development:\n• Chatbots\n• Automation bots\n• AI assistants\n\nGet quote: services@codroidhub.com"
    },
    
    # Contact & Support
    "contact": {
        "keywords": ["contact", "support", "help", "phone", "email", "demo"],
        "response": "Contact CodroidHub:\n\n Email: info@codroidhub.com\n Phone: +91-91385 55661\n Website: www.codroidhub.com\n Address: Second Floor, Brahmakumari Chowk, above SBI Bank, Durga Nagar, Mahesh Nagar, Ambala Cantt, Haryana 133001\n\n Office Hours:\n• Monday - Friday: 9 AM - 6 PM\n• Saturday: 10 AM - 4 PM\n\n Book a FREE Demo:\n• Online consultation\n• Course walkthrough\n• Career guidance\n\nEmail: demo@codroidhub.com"
    },
    
    # Enrollment Process
    "enrollment": {
        "keywords": ["enroll", "admission", "registration", "join", "apply"],
        "response": "Enrollment Process:\n\n Step 1: Choose your course\n Step 2: Fill application form\n Step 3: Pay registration fee (₹2,000)\n Step 4: Attend counseling session\n✅ Step 5: Complete documentation\n Step 6: Start classes!\n\n Payment Options:\n• Online payment\n• Installments available\n• Scholarship programs\n\nStart enrollment: admissions@codroidhub.com"
    },
    
    # Fees & Duration
    "fees": {
        "keywords": ["fee", "cost", "price", "duration", "time", "months"],
        "response": "Course Fees & Duration:\n\n Full Stack Development: ₹25,000 (6 months)\n Game Development: ₹20,000 (4 months)\n AI & IoT: ₹30,000 (5 months)\n Cybersecurity: ₹35,000 (6 months)\n\n Special Offers:\n• Early bird discount: 10% off\n• Student discount: 15% off\n• Group enrollment: 20% off\n\n EMI available starting ₹3,000/month\n🎓 100% refund if not satisfied in first week"
    }
}

def get_bot_response(user_message):
    """Generate bot response based on user input"""
    user_message = user_message.lower().strip()
    
    # Check for specific keywords and return appropriate response
    for category, data in codroidhub_knowledge.items():
        for keyword in data["keywords"]:
            if keyword in user_message:
                return data["response"]
    
    # Check for specific questions
    if any(word in user_message for word in ["what", "how", "when", "where", "why"]):
        if "codroidhub" in user_message:
            return codroidhub_knowledge["welcome"]["response"]
        elif any(word in user_message for word in ["course", "learn"]):
            return codroidhub_knowledge["courses"]["response"]
        elif any(word in user_message for word in ["job", "work", "career"]):
            return codroidhub_knowledge["internship"]["response"]
    
    # Default response with helpful suggestions
    return """I'm here to help you with CodroidHub! 🤖

Try asking me about:
• "Courses" - Our training programs
• "Workshops" - Upcoming events
• "Internships" - Career opportunities
• "Contact" - Get in touch
• "Fees" - Course pricing
• "Enrollment" - How to join

Or just say "hello" to see all options! 😊"""

@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message", "").strip()
        
        if not user_input:
            return jsonify({"error": "Please enter a valid message."})
        
        # Get bot response
        reply = get_bot_response(user_input)
        
        return jsonify({"reply": reply})
        
    except Exception as e:
        return jsonify({"error": f"Something went wrong: {str(e)}"})

# Additional route for getting course syllabus
@app.route("/syllabus/<course_name>")
def get_syllabus(course_name):
    syllabi = {
        "fullstack": "Full Stack Development syllabus available for download",
        "gamedev": "Game Development syllabus available for download",
        "ai": "AI & IoT syllabus available for download",
        "cyber": "Cybersecurity syllabus available for download"
    }
    
    return jsonify({"syllabus": syllabi.get(course_name, "Syllabus not found")})

if __name__ == "__main__":
    print("🚀 CodroidHub Assistant Bot is starting...")
    print("📚 Loaded knowledge base with comprehensive course information")
    print("🌐 Server running on http://localhost:8080")
    
    app.run(debug=True, host="0.0.0.0", port=8080)