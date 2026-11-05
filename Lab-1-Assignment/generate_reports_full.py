#!/usr/bin/env python3
"""
generate_reports_full.py
Complete Report and Submission Generator for DevOps Lab 1
Generates:
  1. Q1_Record_All_Commands.md & .pdf
  2. Q2_CICD_Workflow_Report.md & .pdf
  3. Q3_Automated_Deployment_Jenkins.md & .pdf
  4. Q4_Install_Configure_Git_Jenkins.md & .pdf
  5. Q5_Git_Version_Control_Setup.md & .pdf
  6. Q6_Basic_Jenkins_CICD_Pipeline.md & .pdf
  7. Q7_Jenkinsfile_Pipeline_Stages.md & .pdf
  8. DevOps_Lab1_Comprehensive_Submission_Report.md & .pdf
  9. DevOps_Lab1_Complete_Submission_Bundle.zip
"""

import os
import sys
import zipfile
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

SUBMISSIONS_DIR = os.path.join(os.getcwd(), "submissions")
os.makedirs(SUBMISSIONS_DIR, exist_ok=True)

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont('Helvetica-Bold', 8)
        self.setFillColor(colors.HexColor('#0284c7'))
        # Top Header
        self.drawString(36, 762, 'LAB 1: DEVOPS FOUNDATIONS & CONTINUOUS INTEGRATION')
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#64748b'))
        self.drawRightString(576, 762, 'Academic Submission Report')
        self.setStrokeColor(colors.HexColor('#cbd5e1'))
        self.setLineWidth(0.5)
        self.line(36, 756, 576, 756)

        # Bottom Footer
        self.line(36, 36, 576, 36)
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#64748b'))
        self.drawString(36, 24, 'Student: Manya Juneja | manyajuneja03@gmail.com')
        self.drawRightString(576, 24, f'Page {self._pageNumber} of {page_count}')
        self.restoreState()


def get_styles():
    base = getSampleStyleSheet()
    styles = {
        'DocTitle': ParagraphStyle(
            'DocTitle', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=18, leading=22,
            textColor=colors.HexColor('#0f172a'), spaceAfter=4
        ),
        'DocSubtitle': ParagraphStyle(
            'DocSubtitle', parent=base['Normal'],
            fontName='Helvetica', fontSize=10, leading=14,
            textColor=colors.HexColor('#475569'), spaceAfter=10
        ),
        'MetaBox': ParagraphStyle(
            'MetaBox', parent=base['Normal'],
            fontName='Helvetica', fontSize=8, leading=11.5,
            textColor=colors.HexColor('#334155'),
        ),
        'H1': ParagraphStyle(
            'H1', parent=base['Heading1'],
            fontName='Helvetica-Bold', fontSize=12, leading=16,
            textColor=colors.HexColor('#0369a1'), spaceBefore=10, spaceAfter=5,
            keepWithNext=True
        ),
        'H2': ParagraphStyle(
            'H2', parent=base['Heading2'],
            fontName='Helvetica-Bold', fontSize=10, leading=14,
            textColor=colors.HexColor('#0f172a'), spaceBefore=8, spaceAfter=4,
            keepWithNext=True
        ),
        'Body': ParagraphStyle(
            'Body', parent=base['Normal'],
            fontName='Helvetica', fontSize=8.5, leading=12,
            textColor=colors.HexColor('#1e293b'), spaceAfter=5
        ),
        'BodyBold': ParagraphStyle(
            'BodyBold', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8.5, leading=12,
            textColor=colors.HexColor('#0f172a'), spaceAfter=3
        ),
        'Bullet': ParagraphStyle(
            'Bullet', parent=base['Normal'],
            fontName='Helvetica', fontSize=8.5, leading=12,
            textColor=colors.HexColor('#1e293b'), leftIndent=12, firstLineIndent=-8,
            spaceAfter=2
        ),
        'CodeText': ParagraphStyle(
            'CodeText', parent=base['Normal'],
            fontName='Courier', fontSize=7.5, leading=9.5,
            textColor=colors.HexColor('#e2e8f0'),
        ),
        'TableHeader': ParagraphStyle(
            'TableHeader', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8, leading=10,
            textColor=colors.white
        ),
        'TableCell': ParagraphStyle(
            'TableCell', parent=base['Normal'],
            fontName='Helvetica', fontSize=7.5, leading=10,
            textColor=colors.HexColor('#1e293b')
        ),
        'TableCellBold': ParagraphStyle(
            'TableCellBold', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=7.5, leading=10,
            textColor=colors.HexColor('#0f172a')
        ),
        'CalloutText': ParagraphStyle(
            'CalloutText', parent=base['Normal'],
            fontName='Helvetica', fontSize=8, leading=11,
            textColor=colors.HexColor('#166534')
        )
    }
    return styles

def create_code_block(code_str, styles, width=540):
    p = Preformatted(code_str.strip(), styles['CodeText'])
    t = Table([[p]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0f172a')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#334155')),
    ]))
    return t

def create_callout(text, styles, width=540, bg='#ecfdf5', border='#10b981', title='OBSERVATION / KEY TAKEAWAY'):
    content = Paragraph(f"<b>{title}:</b> {text}", styles['CalloutText'])
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(bg)),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor(border)),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t

def create_metadata_banner(question_num, title, marks, styles, width=540):
    data = [
        [
            Paragraph(f"<b>Course Lab:</b> DevOps Lab 1 (CI/CD)", styles['MetaBox']),
            Paragraph(f"<b>Assessment:</b> Question {question_num} ({marks} Marks)", styles['MetaBox']),
            Paragraph(f"<b>Student:</b> Manya Juneja", styles['MetaBox'])
        ],
        [
            Paragraph(f"<b>Component:</b> {title}", styles['MetaBox']),
            Paragraph(f"<b>Status:</b> Fully Completed & Verified", styles['MetaBox']),
            Paragraph(f"<b>Email:</b> manyajuneja03@gmail.com", styles['MetaBox'])
        ]
    ]
    t = Table(data, colWidths=[180, 180, 180])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    return t

def build_pdf(filename, story):
    filepath = os.path.join(SUBMISSIONS_DIR, filename)
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated PDF: {filepath}")
    return filepath

print("Report generator baseline ready.")

