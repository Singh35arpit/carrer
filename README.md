# CareerPath AI

**Intelligent Career Recommendation System powered by Machine Learning**

CareerPath AI is an advanced career guidance platform that uses ML algorithms to provide personalized career recommendations based on individual skills, interests, personality traits, and preferences.

## Features

✨ **Core Capabilities:**
- Intelligent career matching using ML-based similarity algorithms
- Comprehensive personality type assessment (RIASEC model)
- Skill gap analysis with personalized learning recommendations
- Confidence scoring for each career recommendation
- Detailed match explanations and actionable insights
- Profile persistence and recommendation history tracking

🎯 **What It Provides:**
- Personalized career recommendations with confidence scores
- Analysis of required skills vs. current skills
- Personality-career compatibility assessment
- Industry-specific career information
- Salary range and growth outlook data
- Actionable steps to pursue recommended careers

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or download the project:**
   ```bash
   cd carrer
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   
   Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python main.py
```

### Interactive Workflow

1. **Welcome Screen**: The application starts with a welcome message
   
2. **Main Menu Options:**
   - **Create New Profile**: Build your complete user profile
   - **Load Existing Profile**: Retrieve a previously saved profile
   - **Get Career Recommendations**: Receive personalized career suggestions
   - **View Current Profile**: Review your loaded profile
   - **Exit**: Close the application

3. **Profile Creation Process:**
   - Enter basic information (name, age, education)
   - List your skills with proficiency levels (1-5)
     - Format: `SkillName:4` (e.g., `Python:4`, `Communication:5`)
   - Specify your interests with intensity levels (1-5)
   - Complete personality type assessment
   - Indicate work environment preferences
   - Describe career goals

4. **Receive Recommendations:**
   - Get top 5 career matches with confidence scores
   - View detailed match reasons
   - Identify skill gaps to address
   - See recommended next steps

### Input Format Examples

**Skills:**
```
Python:4
JavaScript:3
Communication:5
Data Analysis:4
Project Management:3
```

**Interests:**
```
Technology:5
Business:4
Data Science:5
```

## Project Structure

```
carrer/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── src/
│   ├── main.py           # Main application logic and CLI
│   ├── models/
│   │   └── profile.py    # Data models (User, Career, etc.)
│   ├── ml/
│   │   ├── matcher.py              # ML matching algorithm
│   │   └── recommendation_engine.py # Recommendation generator
│   ├── utils/
│   │   ├── input_processor.py      # User input handling
│   │   └── data_manager.py         # Data persistence
│   └── data/
│       └── career_db.py   # Career database
└── data/                  # Runtime data storage
    ├── profiles/          # Saved user profiles
    └── recommendations/   # Generated recommendations
```

## Architecture

### Components

1. **Data Models** (`src/models/profile.py`)
   - UserProfile: Stores user information, skills, interests
   - Career: Career information and requirements
   - CareerRecommendation: Recommendation with confidence score

2. **ML Engine** (`src/ml/`)
   - CareerMatcher: Multi-factor matching algorithm
   - RecommendationEngine: Generates recommendations and insights

3. **Utilities** (`src/utils/`)
   - InputProcessor: Handles interactive user input
   - DataManager: Manages data persistence

4. **Database** (`src/data/career_db.py`)
   - Pre-populated with 20+ careers across industries
   - Searchable by industry, personality type, keywords

### Matching Algorithm

The ML-based matching considers:
- **Skills Match (35%)**: Cosine similarity between user skills and career requirements
- **Interest Alignment (25%)**: Overlap between user interests and career domains
- **Personality Fit (20%)**: RIASEC model compatibility
- **Education Match (10%)**: Education level requirements
- **Work Environment (10%)**: Environment preference alignment

## Career Database

The system includes careers in:
- 🖥️ Technology (Software Engineer, Data Scientist, Web Developer, Cybersecurity Analyst)
- 💼 Business (Business Analyst, Project Manager, Marketing Specialist)
- 🏥 Healthcare (Registered Nurse, Medical Researcher)
- 📚 Education (Teacher, Instructional Designer)
- ⚙️ Engineering (Mechanical Engineer, Civil Engineer)
- 🎨 Creative (Graphic Designer, Content Writer)
- 💰 Finance (Financial Analyst, Accountant)
- 🤝 Social Services (Social Worker, HR Specialist)

## Data Storage

- **Profiles**: Saved as JSON files in `data/` directory
- **Recommendations**: History tracked per user
- **Export**: Profiles can be exported with full history

## Configuration

### Customization Options

You can modify the matching weights in `src/ml/matcher.py`:
```python
self.weights = {
    'skills': 0.35,
    'interests': 0.25,
    'personality': 0.20,
    'education': 0.10,
    'work_environment': 0.10
}
```

Add more careers in `src/data/career_db.py` by creating new Career objects.

## Troubleshooting

### Common Issues

**Issue: Module not found errors**
- Solution: Ensure you're running from the project root directory and virtual environment is activated

**Issue: Dependencies won't install**
- Solution: Update pip: `python -m pip install --upgrade pip`

**Issue: Profile not saving**
- Solution: Check write permissions in the `data/` directory

## Future Enhancements

Potential features to add:
- Web-based GUI interface
- Advanced ML models (neural networks, collaborative filtering)
- Integration with job boards
- Skills assessment quizzes
- Career path visualization
- Mentorship matching
- Industry trend analysis
- Resume optimization suggestions

## Contributing

This is an open-source project. Contributions are welcome!

## License

MIT License - Feel free to use and modify for your needs.

## Support

For questions or issues, please create an issue in the repository.

---

**Made with ❤️ for career seekers everywhere**

*Disclaimer: Career recommendations are suggestions based on the information provided. Always conduct thorough research and consult with career professionals when making important career decisions.*
