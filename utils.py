import csv
from flask import Response
from models import BorrowHistory

def generate_csv(user_id):
    history = BorrowHistory.query.filter_by(user_id=user_id).all()
    output = Response(content_type='text/csv')
    output.headers["Content-Disposition"] = "attachment; filename=borrow_history.csv"
    writer = csv.writer(output)
    writer.writerow(['Book ID', 'Start Date', 'End Date'])
    for record in history:
        writer.writerow([record.book_id, record.start_date, record.end_date])
    return output