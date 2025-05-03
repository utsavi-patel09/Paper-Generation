from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from django.core.files import File
from django.shortcuts import render, get_object_or_404
from paper.models.teacher import Teacher
from paper.models import GeneratedPaper
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from django.core.files import File
from django.shortcuts import render, get_object_or_404
from paper.models.teacher import Teacher
from paper.models import GeneratedPaper
import textwrap


PDF_STORAGE_PATH = "media/generated_papers/"




import requests

import requests

def generate_question(subject, topic, difficulty, question_type):
    """
    Function to generate a clean case study-based question using the Groq API.
    """
    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    API_KEY = "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"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Clean and precise system prompt
    system_prompt = """You are an expert educator creating thoughtful questions.
Generate only the case study-based question directly.
Do NOT add any headings like 'Generated Case Study Question', 'Here's your question', 'Case Study:', etc.
Only output the question text itself, properly formatted.
The questions should engage critical thinking and application of concepts to real-world situations.
Do not create MCQs or simple recall questions."""

    user_prompt = f"""Create a {difficulty} case study-based question about {topic} in {subject} that tests {question_type} skills.
The question should:
1. Present a realistic scenario or case study
2. Require analysis and application of knowledge
3. Ask for open-ended responses
4. Challenge the student to demonstrate {question_type} thinking
5. Be appropriate for {difficulty} difficulty level."""

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 800
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"].strip()
        else:
            return "No question generated. Unexpected response format."

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

def generate_mcq(subject, topic, difficulty, question_type):
    """
    Function to generate a single MCQ question using the Groq API.
    """
    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    API_KEY = "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"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = """You are an expert educator creating high-quality multiple-choice questions (MCQs).
Each MCQ should:
- Have a clear and concise question stem
- Provide exactly four answer options (A, B, C, D)
- Test the student's understanding, logic, or memory depending on the skill requested
Avoid simple recall unless explicitly asked. Focus on meaningful, concept-testing MCQs.
- "Here is an easy difficulty MCQ about clustering in machine learning:" and "Generating MCQs..." don't print this additional stuff"""

    user_prompt = f"""Create a {difficulty} difficulty MCQ about {topic} in {subject} that tests {question_type} skills.
The MCQ should:
1. Present a clear question stem
2. Provide exactly four answer choices labeled A, B, C, and D
3. Be challenging enough for the {difficulty} difficulty level.
4. Don't provide correct answer for this
5. Only give me question and its 4 options only"""

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            return "No MCQ generated. Unexpected response format."

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"
    


# Helper function to wrap text after 50 characters
def wrap_text(text, max_line_length=80):  # Increased to 80 for better readability
    return textwrap.fill(text, width=max_line_length)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
import os
from django.core.files import File
from django.shortcuts import render, get_object_or_404
from paper.models.teacher import Teacher
from paper.models import GeneratedPaper
import textwrap

PDF_STORAGE_PATH = "media/generated_papers/"

def generate_pdf(request):
    pdf_url = None

    if request.method == "POST":
        subject_name = request.POST.get("subject_name")
        marks = request.POST.get("marks")
        no_of_mcq = request.POST.get("no_of_mcqs")
        no_of_descriptive = request.POST.get("descriptive")
        difficulty = request.POST.get("difficulty")
        question_type = request.POST.get("question_type")
        total_marks = request.POST.get("total_marks", "70")  # default 70 if not given

        section2_questions = []
        section3_questions = []

        # Generate MCQs
        for _ in range(int(no_of_mcq)):
            q = generate_mcq(subject_name, request.POST.get("topics"), difficulty, question_type)
            if q:
                section2_questions.append(q)

        # Generate Descriptive (Case Study) questions
        for _ in range(int(no_of_descriptive)):
            q = generate_question(subject_name, request.POST.get("topics"), difficulty, question_type)
            if q:
                section3_questions.append(q)

        if not section2_questions and not section3_questions:
            return render(request, "generate_paper.html", {"error": "No questions generated."})

        teacher = get_object_or_404(Teacher, id=request.session.get('teacher'))

        # Ensure storage path exists
        if not os.path.exists(PDF_STORAGE_PATH):
            os.makedirs(PDF_STORAGE_PATH)

        pdf_filename = f"question_paper_{subject_name}.pdf".replace(" ", "_")
        pdf_path = os.path.join(PDF_STORAGE_PATH, pdf_filename)

        try:
            # Create PDF
            pdf = SimpleDocTemplate(
                pdf_path, 
                pagesize=letter,
                rightMargin=40, leftMargin=40,
                topMargin=100, bottomMargin=50
            )

            Story = []

            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize=11, leading=14))

            # Section - II: MCQs
            Story.append(Spacer(1, 12))
            Story.append(Paragraph("<b>Section - I: Multiple Choice Questions</b>", styles['Heading2']))
            Story.append(Spacer(1, 12))

            for idx, question in enumerate(section2_questions, 1):
                parts = question.split('\n')
                question_text = parts[0]
                options = parts[1:] if len(parts) > 1 else []

                Story.append(Paragraph(f"{idx}. {question_text}", styles['Justify']))
                Story.append(Spacer(1, 6))

                for opt in options:
                    Story.append(Paragraph(opt.strip(), styles['Justify']))
                    Story.append(Spacer(1, 3))

                Story.append(Spacer(1, 10))

            # Section - III: Descriptive
            if section3_questions:
                Story.append(PageBreak())
                Story.append(Spacer(1, 12))
                Story.append(Paragraph("<b>Section - II: Descriptive / Case Study-Based Questions</b>", styles['Heading2']))
                Story.append(Spacer(1, 12))

                for idx, question in enumerate(section3_questions, 1):
                    Story.append(Paragraph(f"{idx}. {question}", styles['Justify']))
                    Story.append(Spacer(1, 15))

            # Header/Footer function
            def header_footer(canvas, doc):
                canvas.saveState()
                
                # Header
                canvas.setFont('Helvetica-Bold', 14)
                canvas.drawCentredString(letter[0]/2.0, letter[1]-30, "CHARUSAT University")

                canvas.setFont('Helvetica', 11)
                canvas.drawCentredString(letter[0]/2.0, letter[1]-50, f"Subject: {subject_name}  Total Marks: {marks}")

                # Draw horizontal line below header
                canvas.setLineWidth(0.5)
                canvas.line(40, letter[1]-60, letter[0]-40, letter[1]-60)

                canvas.restoreState()

            # Build PDF
            pdf.build(Story, onFirstPage=header_footer, onLaterPages=header_footer)

        except Exception as e:
            print(f"Error generating PDF: {e}")
            return render(request, "generate_paper.html", {"error": "Error generating PDF."})

        with open(pdf_path, "rb") as f:
            generated_paper = GeneratedPaper.objects.create(
                teacher=teacher,
                title=f"Question Paper - {subject_name}",
                pdf_file=File(f, name=pdf_filename)
            )

        pdf_url = generated_paper.pdf_file.url

        return render(request, "generate_paper.html", {"pdf_url": pdf_url, "teacher": teacher})

    else:
        teacher = get_object_or_404(Teacher, id=request.session.get('teacher'))
        return render(request, "generate_paper.html", {"teacher": teacher})
