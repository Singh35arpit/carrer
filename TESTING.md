# Testing Guide - CareerPath AI

## ✅ Pre-Testing Checklist

Before testing, ensure:
- [x] Python 3.8+ installed
- [x] Virtual environment activated
- [x] Dependencies installed (`pip install -r requirements.txt`)
- [x] You're in the project directory: `cd c:\Users\ASUS\carrer`

---

## 🧪 Test Scenarios

### Test 1: Basic Application Launch

**Objective:** Verify application starts correctly

**Steps:**
```bash
python main.py
```

**Expected Result:**
- Welcome screen displays
- Main menu appears with 5 options
- No errors or exceptions

**Pass Criteria:** ✅ Application launches successfully

---

### Test 2: Profile Creation - Complete Flow

**Objective:** Create a complete user profile

**Test Data:**
```
Name: Alex Chen
Age: 24
Education: Bachelor's Degree in Marketing
Current Role: Marketing Coordinator

Skills:
- Communication:5
- Social Media:4
- Content Creation:4
- Data Analysis:3
- Project Management:3
- Creativity:5

Interests:
- Marketing:5
- Arts:4
- Technology:4
- Business:3

Personality Type: 3 (Artistic)
Work Environment: Office/Remote
Career Goals: Become a Creative Director at a tech company
```

**Steps:**
1. Select option 1 from main menu
2. Enter all information as above
3. Review profile summary
4. Choose 'y' to save profile
5. Note the User ID

**Expected Result:**
- All inputs accepted
- Profile summary displays correctly
- Profile saved to JSON file
- User ID displayed

**Pass Criteria:** ✅ Profile created and saved successfully

---

### Test 3: Profile Loading

**Objective:** Load a previously saved profile

**Steps:**
1. From main menu, select option 2
2. Enter the User ID from Test 2
3. Verify profile displays

**Expected Result:**
- Profile loads without errors
- All data matches what was entered
- Profile summary displays correctly

**Pass Criteria:** ✅ Profile loads successfully

---

### Test 4: Career Recommendations Generation

**Objective:** Generate career recommendations for loaded profile

**Steps:**
1. Ensure profile is loaded (from Test 3)
2. Select option 3 from main menu
3. Wait for recommendations to generate
4. Review the output

**Expected Result:**
- Profile completeness analysis shown
- At least 5 career recommendations provided
- Each recommendation includes:
  - Confidence score
  - Industry information
  - Salary range
  - Growth outlook
  - Match reasons
  - Skill gaps
  - Recommended actions
- Personalized insights displayed

**Pass Criteria:** ✅ Recommendations generated with all required information

---

### Test 5: Recommendation Saving

**Objective:** Save generated recommendations

**Steps:**
1. After recommendations display (Test 4)
2. When prompted, enter 'y' to save
3. Check that file is created in data/ directory

**Expected Result:**
- Confirmation message shown
- File saved to `data/recommendations_<USER_ID>.json`
- File contains valid JSON with all recommendations

**Pass Criteria:** ✅ Recommendations saved successfully

---

### Test 6: Input Validation

**Objective:** Test input validation and error handling

**Test Cases:**

**A. Invalid Skill Format**
```
Input: "Python five" (instead of "Python:5")
Expected: Error message, prompt to re-enter
```

**B. Invalid Proficiency Level**
```
Input: "Python:6" (out of range)
Expected: Error message about 1-5 range
```

**C. Empty Name**
```
Input: "" (just press Enter)
Expected: Error message, prompt to re-enter
```

**D. Invalid Age**
```
Input: "abc" (non-numeric)
Expected: Error message or age skipped
```

**E. Invalid Menu Choice**
```
Input: "7" (out of range)
Expected: Error message, menu redisplayed
```

**Pass Criteria:** ✅ All invalid inputs handled gracefully

---

### Test 7: Edge Cases

**Objective:** Test system behavior with minimal/maximal data

**Scenario A: Minimal Profile**
```
Name: Test User
All other fields: Skip (press Enter)
No skills listed
No interests listed
No personality type selected
```

**Expected:**
- System warns about incomplete profile
- Still generates recommendations (may be low confidence)
- Suggests completing profile for better results

**Scenario B: Extensive Profile**
```
List 10+ skills
List 8+ interests
Complete all optional fields
```

**Expected:**
- High profile completeness score
- More accurate recommendations
- Higher confidence scores

**Pass Criteria:** ✅ Both edge cases handled appropriately

---

### Test 8: Multiple Users

**Objective:** Test system with multiple user profiles

**Steps:**
1. Create profile for "User A", save User ID
2. Create profile for "User B", save User ID
3. Load User A's profile
4. Get recommendations for User A
5. Load User B's profile
6. Get recommendations for User B
7. Verify recommendations are different

**Expected Result:**
- Both profiles stored separately
- Each user gets personalized recommendations
- No data mixing between users

**Pass Criteria:** ✅ Multi-user support works correctly

---

### Test 9: Personality Type Matching

**Objective:** Verify personality-based career matching

**Test Profiles:**

**Profile A - Investigative Type:**
```
Personality: Investigative (Type 2)
Skills: Python:5, Research:5, Analysis:5
Interests: Science:5, Technology:5
Expected Top Matches: Data Scientist, Researcher, Analyst
```

**Profile B - Social Type:**
```
Personality: Social (Type 4)
Skills: Communication:5, Teaching:5, Empathy:5
Interests: Education:5, Social Work:5
Expected Top Matches: Teacher, Counselor, HR Specialist
```

**Profile C - Artistic Type:**
```
Personality: Artistic (Type 3)
Skills: Design:5, Creativity:5, Writing:5
Interests: Arts:5, Writing:5
Expected Top Matches: Designer, Writer, Artist
```

**Pass Criteria:** ✅ Different personalities get appropriately matched careers

---

### Test 10: Skill Gap Analysis

**Objective:** Verify skill gap identification accuracy

**Test Profile:**
```
Target Career: Data Scientist
User Skills: Python:4, Statistics:3
Missing: Machine Learning, Deep Learning, SQL
```

**Expected Result:**
- System identifies missing skills
- Recommends learning ML, Deep Learning, SQL
- Provides actionable steps

**Pass Criteria:** ✅ Skill gaps accurately identified

---

## 📊 Performance Tests

### Test 11: Response Time

**Objective:** Measure system response times

**Measurements:**

1. **Application Launch:** < 2 seconds
2. **Profile Creation:** < 5 minutes (user dependent)
3. **Recommendation Generation:** < 5 seconds
4. **Profile Loading:** < 1 second
5. **Profile Saving:** < 1 second

**Tools:** Use stopwatch or time command

**Pass Criteria:** ✅ All operations complete within acceptable time

---

### Test 12: Memory Usage

**Objective:** Monitor memory consumption

**Method:**
```bash
# On Windows, use Task Manager
# Monitor python.exe memory usage
```

**Expected:**
- Base memory: < 100 MB
- During recommendation generation: < 200 MB
- No memory leaks on repeated operations

**Pass Criteria:** ✅ Memory usage remains reasonable

---

## 🔍 Integration Tests

### Test 13: End-to-End Workflow

**Objective:** Complete workflow from start to finish

**Full Scenario:**
```
1. Install dependencies
2. Launch application
3. Create new profile
4. Save profile
5. Exit application
6. Relaunch application
7. Load saved profile
8. Generate recommendations
9. Save recommendations
10. Export profile (if feature exists)
11. Exit successfully
```

**Expected:** Every step completes successfully with no errors

**Pass Criteria:** ✅ Full workflow completes without issues

---

### Test 14: Data Persistence Verification

**Objective:** Verify data integrity across sessions

**Steps:**
1. Create profile with specific data
2. Save profile
3. Exit application
4. Restart application
5. Load profile
6. Compare loaded data with original
7. Generate recommendations
8. Save recommendations
9. Reload and verify JSON files

**Expected:**
- All data preserved exactly as entered
- JSON files are valid and readable
- No data corruption or loss

**Pass Criteria:** ✅ Data persists correctly

---

## 🐛 Error Handling Tests

### Test 15: Graceful Degradation

**Scenarios:**

**A. Missing Dependencies**
```
Action: Run without installing requirements
Expected: Clear error message about missing packages
```

**B. Corrupted Profile File**
```
Action: Manually corrupt a JSON file
Expected: Error message, option to recreate profile
```

**C. Keyboard Interrupt**
```
Action: Press Ctrl+C during operation
Expected: Graceful exit with message
```

**D. Disk Full**
```
Action: Try to save when disk is full
Expected: Appropriate error message
```

**Pass Criteria:** ✅ All errors handled gracefully with helpful messages

---

## 📋 Test Report Template

Use this template to document test results:

```markdown
## Test Results Summary

**Tester:** [Your Name]
**Date:** [Test Date]
**Environment:** Windows/Python Version

### Test Results

| Test # | Test Name | Status | Notes |
|--------|-----------|--------|-------|
| 1 | App Launch | ✅ Pass / ❌ Fail | |
| 2 | Profile Creation | ✅ Pass / ❌ Fail | |
| 3 | Profile Loading | ✅ Pass / ❌ Fail | |
| 4 | Recommendations | ✅ Pass / ❌ Fail | |
| 5 | Save Recommendations | ✅ Pass / ❌ Fail | |
| 6 | Input Validation | ✅ Pass / ❌ Fail | |
| 7 | Edge Cases | ✅ Pass / ❌ Fail | |
| 8 | Multiple Users | ✅ Pass / ❌ Fail | |
| 9 | Personality Matching | ✅ Pass / ❌ Fail | |
| 10 | Skill Gap Analysis | ✅ Pass / ❌ Fail | |
| 11 | Response Time | ✅ Pass / ❌ Fail | |
| 12 | Memory Usage | ✅ Pass / ❌ Fail | |
| 13 | End-to-End | ✅ Pass / ❌ Fail | |
| 14 | Data Persistence | ✅ Pass / ❌ Fail | |
| 15 | Error Handling | ✅ Pass / ❌ Fail | |

### Issues Found

[List any bugs or issues discovered]

### Overall Assessment

[Pass/Fail with comments]
```

---

## 🎯 Acceptance Criteria

The system passes testing if:

- ✅ All 15 tests pass successfully
- ✅ No critical bugs found
- ✅ Performance meets expectations
- ✅ User experience is smooth and intuitive
- ✅ Data persistence works correctly
- ✅ Error messages are helpful and clear
- ✅ Recommendations are relevant and accurate

---

## 🚀 Running Quick Tests

For a quick verification (5 minutes):

```bash
# 1. Launch test
python main.py

# 2. Create minimal profile
# 3. Get recommendations
# 4. Verify output makes sense
# 5. Exit and reload
# 6. Load profile again
# 7. Confirm data persisted
```

---

## 📞 Reporting Issues

If you find bugs, document:
1. Steps to reproduce
2. Expected behavior
3. Actual behavior
4. Error messages (if any)
5. Environment details

---

**Happy Testing!** 🧪✨

Remember: Thorough testing ensures a reliable, user-friendly experience!
