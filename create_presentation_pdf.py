from fpdf import FPDF
import os

class PresentationPDF(FPDF):
    def header(self):
        if self.page_no() != 1:
            self.set_font("helvetica", "B", 10)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, "CareerPath AI - Project Presentation", align="C", ln=1)
            self.line(10, 20, 287, 20)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def create_pdf(filepath):
    pdf = PresentationPDF(orientation="L", unit="mm", format="A4")
    
    # Slide 1: Cover
    pdf.add_page()
    pdf.set_fill_color(10, 14, 39) # Deep Blue/Black #0a0e27
    pdf.rect(0, 0, 297, 210, "F")
    pdf.set_y(80)
    pdf.set_font("helvetica", "B", 36)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 20, "CareerPath AI", align="C", ln=1)
    
    pdf.set_font("helvetica", "B", 18)
    pdf.set_text_color(59, 130, 246) # Blue
    pdf.cell(0, 15, "Intelligent Career Recommendation System", align="C", ln=1)
    
    pdf.set_font("helvetica", "", 14)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(0, 10, "Transforming Education & Skills into Targeted Success", align="C", ln=1)

    # Slide 2: Problem
    pdf.add_page()
    pdf.set_y(30)
    pdf.set_font("helvetica", "B", 24)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 15, "1. The Problem: Misalignment in Career Paths", ln=1)
    
    pdf.set_y(60)
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "The Skills Gap Paradox:", ln=1)
    pdf.set_font("helvetica", "", 14)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 8, "Despite heavy educational investment, graduates regularly enter the workforce lacking precise skills demanded by employers. This causes deep career dissatisfaction and economic inefficiency.")
    
    pdf.set_y(100)
    pdf.set_font("helvetica", "B", 16)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 10, "Lack of Personalized Guidance:", ln=1)
    pdf.set_font("helvetica", "", 14)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 8, "Traditional career counseling is rigid and slow. It fails to correlate multidimensional data like psychological traits (RIASEC) with fast-changing modern job scopes.")

    # Slide 3: Solution
    pdf.add_page()
    pdf.set_y(30)
    pdf.set_font("helvetica", "B", 24)
    pdf.set_text_color(59, 130, 246)
    pdf.cell(0, 15, "2. Our Solution: A Decentralized Machine Learning Hub", ln=1)
    
    pdf.set_y(60)
    pdf.set_font("helvetica", "", 14)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 10, "- Predictive ML Matching: Ingests skills and education to predict optimal careers utilizing multi-vector confidence scoring matrices.\n\n- RIASEC Personality Model: Incorporates psychology (Realistic, Investigative, Artistic, Social, Enterprising, Conventional) into the core technical algorithm.\n\n- Automated Skill Gaps: Instead of just mapping goals, we strictly define exactly what technical/soft skills are missing to achieve that target.")

    # Slide 4: Features
    pdf.add_page()
    pdf.set_y(30)
    pdf.set_font("helvetica", "B", 24)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 15, "3. Core Features", ln=1)
    
    pdf.set_y(60)
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "Resume Analyzer Engine (NLP)", ln=1)
    pdf.set_font("helvetica", "", 14)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 8, "Users upload absolute raw PDF or DOCX resumes. Our intelligent parser breaks it down locally, extracts active keywords, matches missing ATS standards, and converts unstructured text into deeply structured intelligence models directly against industry standards.")
    
    pdf.set_y(110)
    pdf.set_font("helvetica", "B", 16)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 10, "Dashboard Analytics & Learning Roadmaps", ln=1)
    pdf.set_font("helvetica", "", 14)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 8, "- Glassmorphic UX UI built for ultra-responsiveness.\n- Live Confidence Trajectory graphs and Direct Job Search integration pathways.\n- Step-by-step modular education targets with time-estimated milestones.")

    # Slide 5: System Architecture
    pdf.add_page()
    pdf.set_y(30)
    pdf.set_font("helvetica", "B", 24)
    pdf.set_text_color(139, 92, 246) # Purple
    pdf.cell(0, 15, "4. System Architecture", ln=1)
    
    pdf.set_y(60)
    pdf.set_font("helvetica", "B", 16)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 10, "Backend (Python 3 & Flask)", ln=1)
    pdf.set_font("helvetica", "", 14)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 8, "Engineered securely in Flask providing dynamic routing, secure token storage (werkzeug.security), and blazing-fast REST APIs.")
    
    pdf.set_y(100)
    pdf.set_font("helvetica", "B", 16)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 10, "ML Matrix", ln=1)
    pdf.set_font("helvetica", "", 14)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 8, "Operates decoupled logic within src/ml managing strict recommendation scoring heuristics via JSON datasets bridging millions of traits.")
    
    pdf.set_y(140)
    pdf.set_font("helvetica", "B", 16)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 10, "Frontend Stack", ln=1)
    pdf.set_font("helvetica", "", 14)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 8, "High-fidelity Deep Space Glassmorphism utilizing raw robust HTML5 / CSS3 / Vanilla JS caching overrides, preserving supreme performance.")

    # Save
    pdf.output(filepath)

if __name__ == "__main__":
    create_pdf("CareerPath_AI_Presentation.pdf")
