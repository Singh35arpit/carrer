# Quick Start Guide

## Installation (5 minutes)

1. **Open terminal in project directory:**
   ```bash
   cd c:\Users\ASUS\carrer
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```bash
   venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python main.py
```

## Example Session

### Creating a Profile

When prompted, enter information like:

**Basic Info:**
```
Name: John Doe
Age: 25
Education: Bachelor's Degree in Computer Science
Current Role: Junior Developer
```

**Skills (format: SkillName:Level):**
```
Python:4
JavaScript:3
Machine Learning:3
Communication:4
Problem Solving:5
```

**Interests:**
```
Technology:5
Data Science:5
Business:3
```

**Personality Type:** Choose from the 6 options (e.g., Investigative for thinkers/researchers)

**Work Environment:** Office/Remote

**Career Goals:** Want to work in AI/ML field developing innovative solutions

### Getting Recommendations

The system will analyze your profile and provide:
- Top 5 career matches with confidence scores
- Why each career is a good fit
- Skills you need to develop
- Actionable next steps

## Tips for Best Results

1. ✅ Be honest about your skill levels
2. ✅ List at least 5 skills for better matching
3. ✅ Include diverse interests
4. ✅ Think carefully about personality type
5. ✅ Be specific about career goals

## Understanding Results

**Confidence Scores:**
- Very High (85%+): Excellent match
- High (75-84%): Strong match
- Moderate (65-74%): Good potential fit
- Low (55-64%): Possible match with development
- Very Low (<55%): May not be ideal

**Skill Gaps:** These are skills required for the career that you haven't listed. Consider developing these through courses or projects.

**Recommended Actions:** Follow these steps to pursue the recommended careers.

## Saving Your Profile

Your profile is automatically saved with a unique User ID (8 characters). Save this ID to reload your profile later!

Example: `a1b2c3d4`

---

For detailed information, see README.md
