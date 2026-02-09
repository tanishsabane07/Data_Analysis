"""
PDF Report Generator for Equipment Data.
"""

from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime


def generate_equipment_report(dataset):
    """
    Generate a PDF report for the given dataset.
    
    Args:
        dataset: Dataset model instance with related records
        
    Returns:
        BytesIO buffer containing the PDF data
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1a365d')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.HexColor('#2d3748')
    )
    
    normal_style = styles['Normal']
    
    # Build document content
    story = []
    
    # Title
    story.append(Paragraph("Chemical Equipment Analysis Report", title_style))
    story.append(Spacer(1, 12))
    
    # File info
    story.append(Paragraph(f"<b>File:</b> {dataset.filename}", normal_style))
    story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    story.append(Paragraph(f"<b>Upload Date:</b> {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    story.append(Spacer(1, 20))
    
    # Summary Statistics Section
    story.append(Paragraph("Summary Statistics", heading_style))
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Equipment Count', str(dataset.total_count)],
        ['Average Flowrate', f"{dataset.avg_flowrate:.2f} L/min"],
        ['Average Pressure', f"{dataset.avg_pressure:.2f} bar"],
        ['Average Temperature', f"{dataset.avg_temperature:.2f} °C"],
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4299e1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 20))
    
    # Type Distribution Section
    story.append(Paragraph("Equipment Type Distribution", heading_style))
    
    type_data = [['Equipment Type', 'Count']]
    for eq_type, count in dataset.type_distribution.items():
        type_data.append([eq_type, str(count)])
    
    type_table = Table(type_data, colWidths=[3*inch, 2*inch])
    type_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#48bb78')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0fff4')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#c6f6d5')),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    story.append(type_table)
    story.append(Spacer(1, 20))
    
    # Equipment Data Table
    story.append(Paragraph("Equipment Records", heading_style))
    
    records = dataset.records.all()
    if records.exists():
        eq_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
        for record in records[:50]:  # Limit to 50 records for PDF
            eq_data.append([
                record.equipment_name,
                record.equipment_type,
                f"{record.flowrate:.1f}",
                f"{record.pressure:.1f}",
                f"{record.temperature:.1f}"
            ])
        
        # Add note if truncated
        if records.count() > 50:
            story.append(Paragraph(f"<i>Showing first 50 of {records.count()} records</i>", normal_style))
            story.append(Spacer(1, 10))
        
        eq_table = Table(eq_data, colWidths=[1.5*inch, 1.2*inch, 0.9*inch, 0.9*inch, 1*inch])
        eq_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#805ad5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#faf5ff')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e9d8fd')),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#faf5ff'), colors.white]),
        ]))
        story.append(eq_table)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
