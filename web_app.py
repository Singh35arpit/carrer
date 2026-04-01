"""
CareerPath AI - Web Application
Flask backend API for career recommendations
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
import os
from flask_cors import CORS
import uuid
import json
from pathlib import Path
from functools import wraps
from werkzeug.utils import secure_filename

from src.models.profile import UserProfile, Skill, Interest, PersonalityType
from src.data.career_db import CareerDatabase
from src.data.large_career_db import career_database_large
from src.data.large_skills_db import skills_database_large
from src.ml.recommendation_engine import RecommendationEngine
from src.utils.data_manager import DataManager
from src.analyzer.resume_analyzer import ResumeAnalyzer, analyze_resume_file
from src.utils.auth_db import UserDatabase

app = Flask(__name__)
app.secret_key = 'careerpath_ai_secret_key_2024'  # For session management
CORS(app)  # Enable CORS for API calls

# File upload configuration
UPLOAD_FOLDER = Path('uploads')
UPLOAD_FOLDER.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Initialize components
career_db = CareerDatabase()
recommendation_engine = RecommendationEngine()
data_manager = DataManager()
user_db = UserDatabase()
resume_analyzer = ResumeAnalyzer()


@app.route('/')
def index():
    """Serve the main landing page"""
    if 'user_token' in session:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')


@app.route('/presentation')
def presentation_page():
    """Serve the standalone Presentation Slide Deck"""
    return render_template('presentation.html')

@app.route('/download-presentation-pdf')
def download_presentation_pdf():
    """Serve the standalone static PDF presentation file for user download"""
    pdf_path = os.path.join(app.root_path, 'CareerPath_AI_Presentation.pdf')
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True, download_name='CareerPath_AI_Presentation.pdf')
    return "The PDF presentation file could not be generated and is missing.", 404


@app.route('/test')
def test_page():
    """System test page"""
    return render_template('test.html')


@app.route('/diagnostic')
def diagnostic_page():
    """Complete diagnostic page with auto-fixes"""
    return render_template('diagnostic.html')


@app.route('/test-features')
def test_features_page():
    """Test career profile and resume analyzer features"""
    return render_template('test-features.html')


@app.route('/auth')
def auth_page():
    """Serve authentication page"""
    return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
    """Serve login page"""
    if 'user_token' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register')
def register_page():
    """Serve register page"""
    if 'user_token' in session:
        return redirect(url_for('dashboard'))
    return render_template('register.html')


@app.route('/auth-fixed')
def auth_fixed_page():
    """Serve fixed authentication page (guaranteed to work)"""
    if 'user_token' in session:
        return redirect(url_for('dashboard'))
    return render_template('auth-fixed.html')


@app.route('/dashboard')
def dashboard():
    """Serve user dashboard"""
    if 'user_token' not in session:
        return redirect(url_for('login_page'))
    
    # Validate token
    user_info = user_db.validate_token(session['user_token'])
    if not user_info:
        session.pop('user_token', None)
        return redirect(url_for('login_page'))
    
    return render_template('dashboard.html', user=user_info)


@app.route('/resume-analyzer')
def resume_analyzer_page():
    if 'user_token' not in session:
        return redirect(url_for('login_page'))
    user_info = user_db.validate_token(session['user_token'])
    if not user_info:
        session.pop('user_token', None)
        return redirect(url_for('login_page'))
    return render_template('resume_analyzer.html', user=user_info)

@app.route('/profiles')
def profiles_page():
    if 'user_token' not in session:
        return redirect(url_for('login_page'))
    user_info = user_db.validate_token(session['user_token'])
    if not user_info:
        session.pop('user_token', None)
        return redirect(url_for('login_page'))
    return render_template('profiles.html', user=user_info)

@app.route('/jobs')
def jobs_page():
    if 'user_token' not in session:
        return redirect(url_for('login_page'))
    user_info = user_db.validate_token(session['user_token'])
    if not user_info:
        session.pop('user_token', None)
        return redirect(url_for('login_page'))
    return render_template('jobs.html', user=user_info)

@app.route('/roadmap')
def roadmap_page():
    if 'user_token' not in session:
        return redirect(url_for('login_page'))
    user_info = user_db.validate_token(session['user_token'])
    if not user_info:
        session.pop('user_token', None)
        return redirect(url_for('login_page'))
    return render_template('roadmap.html', user=user_info)


@app.route('/api/profile', methods=['POST'])
def create_profile():
    """Create a new user profile"""
    try:
        data = request.json
        
        # Validate required fields
        if not data or not data.get('name'):
            return jsonify({
                'success': False,
                'error': 'Name is required'
            }), 400
        
        # Create user profile
        user_id = data.get('user_id') or str(uuid.uuid4())[:8]
        print(f"Creating profile for user_id: {user_id}")
        
        profile = UserProfile(
            user_id=user_id,
            name=data['name'],
            age=int(data['age']) if data.get('age') else None,
            education_level=data.get('education_level'),
            current_role=data.get('current_role')
        )
        
        # Add skills
        for skill_data in data.get('skills', []):
            skill = Skill(
                name=skill_data['name'],
                proficiency=int(skill_data['proficiency']),
                category=skill_data.get('category', 'Other')
            )
            profile.add_skill(skill)
        
        # Add interests
        for interest_data in data.get('interests', []):
            interest = Interest(
                name=interest_data['name'],
                intensity=int(interest_data['intensity'])
            )
            profile.add_interest(interest)
        
        # Set personality type
        if data.get('personality_type'):
            try:
                profile.personality_type = PersonalityType(data['personality_type'])
            except ValueError:
                pass
        
        # Set preferences
        profile.preferred_work_environment = data.get('preferred_work_environment')
        profile.career_goals = data.get('career_goals')
        
        # Save profile
        print(f"Saving profile to data_manager...")
        data_manager.save_profile(profile)
        print(f"Profile saved successfully!")
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'message': 'Profile created successfully',
            'profile': profile.to_dict()
        })
        
    except TypeError as e:
        import traceback
        error_msg = f"Type Error: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': error_msg,
            'traceback': traceback.format_exc()
        }), 500
    except Exception as e:
        import traceback
        error_msg = f"Error creating profile: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': error_msg,
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/profile/<user_id>', methods=['GET'])
def get_profile(user_id):
    """Get a user profile by ID"""
    try:
        profile = data_manager.load_profile(user_id)
        
        if not profile:
            return jsonify({
                'success': False,
                'error': 'Profile not found'
            }), 404
        
        return jsonify({
            'success': True,
            'profile': profile.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """Get career recommendations for a user"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        # Build profile from request data if it contains skills and interests
        if data.get('skills') or data.get('interests'):
            profile = UserProfile(
                user_id=user_id if user_id else 'temp',
                name=data.get('name', 'User'),
                age=int(data['age']) if data.get('age') else None,
                education_level=data.get('education_level'),
                current_role=data.get('current_role')
            )
            
            # Add skills
            for skill_data in data.get('skills', []):
                skill = Skill(
                    name=skill_data['name'],
                    proficiency=int(skill_data['proficiency']),
                    category=skill_data.get('category', 'Other')
                )
                profile.add_skill(skill)
            
            # Add interests
            for interest_data in data.get('interests', []):
                interest = Interest(
                    name=interest_data['name'],
                    intensity=int(interest_data['intensity'])
                )
                profile.add_interest(interest)
            
            # Set personality type
            if data.get('personality_type'):
                try:
                    profile.personality_type = PersonalityType(data['personality_type'])
                except ValueError:
                    pass
            
            profile.preferred_work_environment = data.get('preferred_work_environment')
            profile.career_goals = data.get('career_goals')
            
            # Save the profile if user_id is legitimate
            if user_id and user_id != 'temp':
                data_manager.save_profile(profile)
                
        else:
            if not user_id:
                return jsonify({
                    'success': False,
                    'error': 'No profile data or user_id provided'
                }), 400
                
            # Load existing profile
            profile = data_manager.load_profile(user_id)
            if not profile:
                return jsonify({
                    'success': False,
                    'error': 'Profile not found'
                }), 404
        
        # Get recommendations
        all_careers = career_db.get_all_careers()
        recommendations = recommendation_engine.get_recommendations(profile, all_careers, top_n=5)
        
        # Analyze profile completeness
        profile_analysis = recommendation_engine.analyze_profile_completeness(profile)
        
        # Get insights
        insights = recommendation_engine.get_personalized_insights(profile, recommendations)
        
        return jsonify({
            'success': True,
            'recommendations': [rec.to_dict() for rec in recommendations],
            'profile_analysis': profile_analysis,
            'insights': insights
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/careers', methods=['GET'])
def get_careers():
    """Get all available careers from large database"""
    try:
        # Get careers from large database
        careers = career_database_large.get_all_careers()
        return jsonify({
            'success': True,
            'careers': careers,
            'total_count': len(careers)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/careers/search', methods=['GET'])
def search_careers_api():
    """Search careers by keyword"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query parameter required'
            }), 400
        
        results = career_database_large.search_careers(query)
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/careers/categories', methods=['GET'])
def get_career_categories():
    """Get career categories"""
    try:
        categories = career_database_large.get_categories()
        return jsonify({
            'success': True,
            'categories': categories,
            'total_categories': len(categories)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/careers/<industry>', methods=['GET'])
def get_careers_by_industry(industry):
    """Get careers by industry"""
    try:
        careers = career_db.get_careers_by_industry(industry)
        return jsonify({
            'success': True,
            'careers': [career.to_dict() for career in careers]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/personality-types', methods=['GET'])
def get_personality_types():
    """Get all personality types"""
    try:
        types = [
            {
                'value': pt.value,
                'name': pt.name,
                'description': get_personality_description(pt)
            }
            for pt in PersonalityType
        ]
        return jsonify({
            'success': True,
            'personality_types': types
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def get_personality_description(personality_type):
    """Get description for a personality type"""
    descriptions = {
        PersonalityType.REALISTIC: "Doers - You like working with tools, machines, or animals",
        PersonalityType.INVESTIGATIVE: "Thinkers - You enjoy solving problems and conducting research",
        PersonalityType.ARTISTIC: "Creators - You prefer creative work and self-expression",
        PersonalityType.SOCIAL: "Helpers - You like helping people and working in teams",
        PersonalityType.ENTERPRISING: "Persuaders - You enjoy leading and persuading others",
        PersonalityType.CONVENTIONAL: "Organizers - You prefer structured environments and details"
    }
    return descriptions.get(personality_type, "")


@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get suggested skills from large database"""
    try:
        # Get all skills from large database
        all_skills = skills_database_large.get_all_skills()
        return jsonify({
            'success': True,
            'skills': all_skills,
            'total_count': len(all_skills)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/skills/search', methods=['GET'])
def search_skills_api():
    """Search skills by keyword"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query parameter required'
            }), 400
        
        results = skills_database_large.search_skills(query)
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/skills/categories', methods=['GET'])
def get_skill_categories():
    """Get skill categories with counts"""
    try:
        stats = skills_database_large.get_category_stats()
        return jsonify({
            'success': True,
            'categories': stats,
            'total_categories': len(stats)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/interests', methods=['GET'])
def get_interests():
    """Get suggested interests"""
    try:
        interests = career_db.get_unique_interests()
        return jsonify({
            'success': True,
            'interests': interests
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/profile/<user_id>/history', methods=['GET'])
def get_recommendation_history(user_id):
    """Get recommendation history for a user"""
    try:
        history = data_manager.get_user_history(user_id)
        return jsonify({
            'success': True,
            'history': history
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/profiles', methods=['GET'])
def get_user_profiles():
    """Get all saved profiles for the logged-in user"""
    try:
        if 'user_id' not in session:
            return jsonify({
                'success': False,
                'error': 'Unauthorized'
            }), 401
            
        user_id = session.get('user_id')
        
        # Load the profile associated with this user
        profile = data_manager.load_profile(user_id)
        
        profiles_list = []
        if profile:
            # Format the output required by dashboard.js displayProfiles
            profiles_list.append(profile.to_dict())
            
        return jsonify({
            'success': True,
            'profiles': profiles_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/profile/<user_id>', methods=['DELETE'])
def delete_profile(user_id):
    """Delete a user profile"""
    try:
        # Check authentication constraint
        if 'user_id' not in session or session['user_id'] != user_id:
            return jsonify({
                'success': False,
                'error': 'Unauthorized'
            }), 401
            
        success = data_manager.delete_profile(user_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Profile deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Profile not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Resume Analyzer Endpoints
@app.route('/api/resume/upload', methods=['POST'])
def upload_resume():
    """Upload and analyze a resume"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'File type not allowed. Please upload PDF, DOCX, or TXT files.'
            }), 400
        
        # Save file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = Path(app.config['UPLOAD_FOLDER']) / unique_filename
        file.save(str(filepath))
        
        # Analyze resume
        analysis_result = analyze_resume_file(str(filepath))
        
        # Clean up uploaded file
        filepath.unlink()
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'message': 'Resume analyzed successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/resume/analyze-text', methods=['POST'])
def analyze_resume_text():
    """Analyze resume text directly"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text or not text.strip():
            return jsonify({
                'success': False,
                'error': 'No text provided. Please paste your resume content.'
            }), 400
        
        # Check if text is long enough
        if len(text.strip()) < 50:
            return jsonify({
                'success': False,
                'error': 'Resume text is too short. Please provide a complete resume (at least 50 characters).'
            }), 400
        
        analyzer = ResumeAnalyzer()
        result = analyzer.analyze_resume(text)
        
        # Validate result
        if not result:
            return jsonify({
                'success': False,
                'error': 'Failed to analyze resume. Please try again.'
            }), 500
        
        return jsonify({
            'success': True,
            'analysis': result,
            'message': 'Resume analyzed successfully',
            'skills_found': len(result.get('skills', [])),
            'experience_years': result.get('experience_years', 0)
        })
        
    except Exception as e:
        import traceback
        print(f"Error analyzing resume: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500


@app.route('/api/resume/skill-gaps', methods=['POST'])
def get_skill_gaps():
    """Get skill gaps for a target career based on resume analysis"""
    try:
        data = request.json
        resume_data = data.get('resume_data', {})
        target_career = data.get('target_career', '')
        
        if not target_career:
            return jsonify({
                'success': False,
                'error': 'Target career is required'
            }), 400
        
        analyzer = ResumeAnalyzer()
        gaps = analyzer.get_skill_gaps(resume_data, target_career)
        
        return jsonify({
            'success': True,
            'skill_gaps': gaps,
            'recommendations': generate_learning_recommendations(gaps)
        })
        
    except Exception as e:
        import traceback
        print(f"Error getting skill gaps: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/test/resume-analyzer', methods=['GET'])
def test_resume_analyzer():
    """Test endpoint to verify resume analyzer is working"""
    try:
        # Test with sample text
        test_text = """
        John Doe
        Software Engineer
        
        Experience:
        - Developed web applications using Python, JavaScript, and React
        - Worked with databases like MySQL and PostgreSQL
        - Implemented machine learning models using scikit-learn and TensorFlow
        
        Skills:
        Programming: Python, Java, JavaScript, C++
        Web: HTML, CSS, React, Node.js, Django
        Database: SQL, MongoDB
        Tools: Git, Docker, AWS
        """
        
        print("Starting resume analysis test...")
        analyzer = ResumeAnalyzer()
        print("ResumeAnalyzer initialized")
        
        result = analyzer.analyze_resume(test_text)
        print(f"Analysis complete: {result.keys() if result else 'None'}")
        
        return jsonify({
            'success': True,
            'message': 'Resume analyzer is working!',
            'test_result': {
                'skills_found': len(result.get('skills', [])) if result else 0,
                'sample_skills': [s['name'] for s in result.get('skills', [])[:10]] if result else [],
                'experience_years': result.get('experience_years', 0) if result else 0,
                'job_titles': result.get('job_titles', []) if result else []
            }
        })
        
    except Exception as e:
        import traceback
        error_msg = f"Error in test: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Test failed: {str(e)}',
            'traceback': traceback.format_exc(),
            'message': 'Resume analyzer might not be properly initialized. Make sure spacy model is installed.'
        }), 500


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_learning_recommendations(skill_gaps: list) -> list:
    """Generate learning recommendations based on skill gaps"""
    learning_resources = {
        'python': {'name': 'Python Programming', 'platform': 'Coursera', 'duration': '8 weeks'},
        'java': {'name': 'Java Programming', 'platform': 'edX', 'duration': '10 weeks'},
        'javascript': {'name': 'JavaScript Development', 'platform': 'Udemy', 'duration': '6 weeks'},
        'machine learning': {'name': 'Machine Learning A-Z', 'platform': 'Coursera', 'duration': '12 weeks'},
        'aws': {'name': 'AWS Certified Solutions Architect', 'platform': 'A Cloud Guru', 'duration': '8 weeks'},
        'docker': {'name': 'Docker Mastery', 'platform': 'Udemy', 'duration': '4 weeks'},
        'react': {'name': 'React Developer Bootcamp', 'platform': 'Udemy', 'duration': '8 weeks'},
    }
    
    recommendations = []
    for gap in skill_gaps:
        if gap.lower() in learning_resources:
            recommendations.append({
                'skill': gap,
                **learning_resources[gap.lower()]
            })
    
    return recommendations


# Authentication Endpoints
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        # Validate input
        if not name or not email or not password:
            return jsonify({
                'success': False,
                'error': 'Name, email, and password are required'
            }), 400
        
        if len(password) < 6:
            return jsonify({
                'success': False,
                'error': 'Password must be at least 6 characters long'
            }), 400
        
        # Register user
        result = user_db.register_user(name, email, password)
        
        if result['success']:
            # Store token in session
            session['user_token'] = result['token']
            session['user_id'] = result['user']['user_id']
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        remember = data.get('remember', False)
        
        # Validate input
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400
        
        # Login user
        result = user_db.login_user(email, password, remember)
        
        if result['success']:
            # Store token in session
            session['user_token'] = result['token']
            session['user_id'] = result['user']['user_id']
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout user"""
    try:
        token = session.get('user_token')
        if token:
            user_db.logout_user(token)
        
        session.pop('user_token', None)
        session.pop('user_id', None)
        
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    """Get current logged-in user info"""
    try:
        token = session.get('user_token')
        if not token:
            return jsonify({
                'success': False,
                'error': 'Not authenticated'
            }), 401
        
        user_info = user_db.validate_token(token)
        if not user_info:
            session.pop('user_token', None)
            return jsonify({
                'success': False,
                'error': 'Invalid or expired session'
            }), 401
        
        return jsonify({
            'success': True,
            'user': user_info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
