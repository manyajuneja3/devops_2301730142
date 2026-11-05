"""
DevOps Lab 2 - Submission Document Generator
Builds 9 publication-grade PDFs for Lab 2 Containerization & Kubernetes Orchestration
Student: Manya Juneja (Roll No: 2301730142)
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

STUDENT_NAME = "Manya Juneja"
STUDENT_ROLL = "2301730142"
STUDENT_EMAIL = "manyajuneja03@gmail.com"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Header (pages after first page)
        if self._pageNumber > 1:
            self.drawString(36, 758, f"DevOps Lab 2 | Student: {STUDENT_NAME} (Roll: {STUDENT_ROLL})")
            self.drawRightString(576, 758, "Lab Submission Record")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 752, 576, 752)
        
        # Footer
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(36, 25, f"Candidate: {STUDENT_NAME} | Roll No: {STUDENT_ROLL} | Email: {STUDENT_EMAIL}")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 25, page_str)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 35, 576, 35)
        self.restoreState()

def get_report_styles():
    styles = getSampleStyleSheet()
    
    # Custom color palette
    c_primary = colors.HexColor("#0F2942")     # Deep Navy
    c_secondary = colors.HexColor("#1E40AF")   # Royal Blue
    c_dark = colors.HexColor("#1E293B")        # Slate Dark
    
    styles.add(ParagraphStyle(
        name='DocTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_primary,
        spaceAfter=4
    ))
    
    styles.add(ParagraphStyle(
        name='DocSubTitle',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=c_secondary,
        spaceAfter=8
    ))
    
    styles.add(ParagraphStyle(
        name='MetaLabel',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#334155")
    ))
    
    styles.add(ParagraphStyle(
        name='MetaVal',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0F172A")
    ))
    
    styles.add(ParagraphStyle(
        name='SectionHeading',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='SubSectionHeading',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_secondary,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='BodyCustom',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='BodyCustomBold',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=c_dark,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name='TerminalText',
        fontName='Courier',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#38BDF8")
    ))

    styles.add(ParagraphStyle(
        name='CodeText',
        fontName='Courier',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#F1F5F9")
    ))

    styles.add(ParagraphStyle(
        name='CalloutText',
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#0C4A6E")
    ))

    styles.add(ParagraphStyle(
        name='CalloutBold',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#0369A1")
    ))

    styles.add(ParagraphStyle(
        name='TableHead',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    ))

    styles.add(ParagraphStyle(
        name='TableCell',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#1E293B")
    ))

    styles.add(ParagraphStyle(
        name='TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#0F172A")
    ))

    return styles

def make_terminal_box(command_str, output_str, styles):
    content = []
    if command_str:
        cmd_p = Paragraph(f"<font color='#4ADE80'><b>$ {command_str}</b></font>", styles['TerminalText'])
        content.append(cmd_p)
    if output_str:
        if command_str:
            content.append(Spacer(1, 3))
        # escape angle brackets for reportlab XML
        safe_out = output_str.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        out_p = Paragraph(f"<font color='#CBD5E1'>{safe_out}</font>", styles['TerminalText'])
        content.append(out_p)
        
    t = Table([[content]], colWidths=[540])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#334155")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t

def make_code_box(code_str, language, styles):
    safe_code = code_str.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    p = Paragraph(safe_code, styles['CodeText'])
    
    header_p = Paragraph(f"<font color='#94A3B8'><b>// File: {language} | Candidate: {STUDENT_NAME} ({STUDENT_ROLL})</b></font>", styles['CodeText'])
    
    t = Table([[header_p], [p]], colWidths=[540])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#0F172A")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#334155")),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.HexColor("#334155")),
    ]))
    return t

def make_callout(title, body, styles, alert_type="note"):
    bg = colors.HexColor("#F0F9FF")
    border = colors.HexColor("#0284C7")
    title_color = "#0369A1"
    if alert_type == "success":
        bg = colors.HexColor("#ECFDF5")
        border = colors.HexColor("#059669")
        title_color = "#047857"
    elif alert_type == "warning":
        bg = colors.HexColor("#FFFBEB")
        border = colors.HexColor("#D97706")
        title_color = "#B45309"
        
    p_title = Paragraph(f"<font color='{title_color}'><b>{title}</b></font>", styles['CalloutBold'])
    p_body = Paragraph(body, styles['CalloutText'])
    
    t = Table([[p_title], [p_body]], colWidths=[540])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('BOX', (0,0), (-1,-1), 1, border),
    ]))
    return t

def make_meta_header(q_num, q_title, marks, styles):
    table_data = [
        [
            Paragraph("<b>STUDENT NAME:</b>", styles['MetaLabel']),
            Paragraph(f"<b>{STUDENT_NAME}</b>", styles['MetaVal']),
            Paragraph("<b>ROLL NUMBER:</b>", styles['MetaLabel']),
            Paragraph(f"<b>{STUDENT_ROLL}</b>", styles['MetaVal'])
        ],
        [
            Paragraph("<b>EMAIL ADDRESS:</b>", styles['MetaLabel']),
            Paragraph(STUDENT_EMAIL, styles['MetaVal']),
            Paragraph("<b>ASSESSMENT:</b>", styles['MetaLabel']),
            Paragraph(f"Question {q_num} ({marks} Marks)", styles['MetaVal'])
        ],
        [
            Paragraph("<b>COURSE / LAB:</b>", styles['MetaLabel']),
            Paragraph("DevOps Lab 2 (Containerization & K8s)", styles['MetaVal']),
            Paragraph("<b>ENVIRONMENT:</b>", styles['MetaLabel']),
            Paragraph("Docker 29 / Minikube v1.36 / kubectl", styles['MetaVal'])
        ]
    ]
    t = Table(table_data, colWidths=[105, 185, 100, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    return t

print("Generator core with student metadata loaded successfully.")
