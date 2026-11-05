#!/usr/bin/env python3
"""
DevOps Lab 1: DevOps Foundations & Continuous Integration
Report & Submission Generator
Author: Manya Juneja (manyajuneja03@gmail.com)
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
from reportlab.lib.units import inch

# Custom Numbered Canvas for professional header & footer with dynamic page counts
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


def get_custom_styles():
    base_styles = getSampleStyleSheet()

    styles = {
        'DocTitle': ParagraphStyle(
            'DocTitle',
            parent=base_styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=6
        ),
        'DocSubtitle': ParagraphStyle(
            'DocSubtitle',
            parent=base_styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            leading=15,
            textColor=colors.HexColor('#475569'),
            spaceAfter=14
        ),
        'MetaBox': ParagraphStyle(
            'MetaBox',
            parent=base_styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#334155'),
        ),
        'H1': ParagraphStyle(
            'H1',
            parent=base_styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#0369a1'),
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=True
        ),
        'H2': ParagraphStyle(
            'H2',
            parent=base_styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=15,
            textColor=colors.HexColor('#0f172a'),
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True
        ),
        'Body': ParagraphStyle(
            'Body',
            parent=base_styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=6
        ),
        'BodyBold': ParagraphStyle(
            'BodyBold',
            parent=base_styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=4
        ),
        'Bullet': ParagraphStyle(
            'Bullet',
            parent=base_styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#1e293b'),
            leftIndent=15,
            firstLineIndent=-10,
            spaceAfter=3
        ),
        'CodeText': ParagraphStyle(
            'CodeText',
            parent=base_styles['Normal'],
            fontName='Courier',
            fontSize=8,
            leading=10.5,
            textColor=colors.HexColor('#e2e8f0'),
        ),
        'CodeInline': ParagraphStyle(
            'CodeInline',
            parent=base_styles['Normal'],
            fontName='Courier-Bold',
            fontSize=8.5,
            textColor=colors.HexColor('#0284c7'),
        ),
        'TableHeader': ParagraphStyle(
            'TableHeader',
            parent=base_styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8.5,
            leading=11,
            textColor=colors.white,
            alignment=0
        ),
        'TableCell': ParagraphStyle(
            'TableCell',
            parent=base_styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=11,
            textColor=colors.HexColor('#1e293b')
        ),
        'TableCellBold': ParagraphStyle(
            'TableCellBold',
            parent=base_styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=11,
            textColor=colors.HexColor('#0f172a')
        ),
        'CalloutText': ParagraphStyle(
            'CalloutText',
            parent=base_styles['Normal'],
            fontName='Helvetica',
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor('#166534')
        )
    }
    return styles

def create_code_block(code_str, styles, width=540):
    lines = code_str.strip().split('\n')
    formatted = '\n'.join(lines)
    # Wrap in Table for background and padding
    p = Preformatted(formatted, styles['CodeText'])
    t = Table([[p]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0f172a')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#1e293b')),
    ]))
    return t

def create_callout(text, styles, width=540, bg='#ecfdf5', border='#10b981', title='OBSERVATION / KEY TAKEAWAY'):
    content = [
        Paragraph(f"<b>{title}:</b> {text}", styles['CalloutText'])
    ]
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(bg)),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor(border)),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
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
            Paragraph(f"<b>Topic:</b> {title}", styles['MetaBox']),
            Paragraph(f"<b>Status:</b> Completed & Verified", styles['MetaBox']),
            Paragraph(f"<b>Email:</b> manyajuneja03@gmail.com", styles['MetaBox'])
        ]
    ]
    t = Table(data, colWidths=[180, 180, 180])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t

print("Framework setup ready.")

