def export_excel(rows, path):
    from openpyxl import Workbook
    wb=Workbook(); ws=wb.active; ws.title="Timetable"
    ws.append(["Course ID","Course","Teacher","Day","Time","Room"])
    for r in rows: ws.append([r["course_id"],r["course_name"],r["teacher"],r["day"],r["time"],r["room"]])
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width=min(max(len(str(x.value or "")) for x in col)+2,35)
    wb.save(path)

def export_pdf(rows, path):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import landscape,A4
    from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph,Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    data=[["Course ID","Course","Teacher","Day","Time","Room"]]
    data += [[r["course_id"],r["course_name"],r["teacher"],r["day"],r["time"],r["room"]] for r in rows]
    t=Table(data,repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.darkblue),("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),.5,colors.grey),("ALIGN",(0,0),(-1,-1),"CENTER"),("FONTSIZE",(0,0),(-1,-1),8)]))
    s=getSampleStyleSheet(); doc=SimpleDocTemplate(str(path),pagesize=landscape(A4))
    doc.build([Paragraph("Smart Timetable",s["Title"]),Spacer(1,10),t])
