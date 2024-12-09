from flask import Blueprint, request, jsonify
from models import db, User, Book, BorrowRequest, BorrowHistory
from flask_jwt_extended import jwt_required, create_access_token
from datetime import datetime

api_bp = Blueprint('api', __name__)

# Librarian APIs
@api_bp.route('/api/librarian/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    new_user = User(email=data['email'], password=data['password'], is_librarian=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User  created successfully."}), 201

@api_bp.route('/api/librarian/borrow-requests', methods=['GET'])
@jwt_required()
def view_borrow_requests():
    requests = BorrowRequest.query.all()
    return jsonify([{
        "id": req.id,
        "user_id": req.user_id,
        "book_id": req.book_id,
        "start_date": req.start_date,
        "end_date": req.end_date,
        "status": req.status
    } for req in requests]), 200

@api_bp.route('/api/librarian/borrow-requests/<int:request_id>', methods=['PUT'])
@jwt_required()
def update_borrow_request(request_id):
    data = request.get_json()
    req = BorrowRequest.query.get(request_id)
    if req:
        req.status = data['status']
        db.session.commit()
        return jsonify({"message": "Request updated successfully."}), 200
    return jsonify({"message": "Request not found."}), 404

@api_bp.route('/api/librarian/users/<int:user_id>/borrow-history', methods=['GET'])
@jwt_required()
def user_borrow_history(user_id):
    history = BorrowHistory.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "book_id": hist.book_id,
        "start_date": hist.start_date,
        "end_date": hist.end_date
    } for hist in history]), 200

# Library User APIs
@api_bp.route('/api/books', methods=['GET'])
@jwt_required()
def get_books():
 ```python
    books = Book.query.all()
    return jsonify([{
        "id": book.id,
        "title": book.title,
        "author": book.author
    } for book in books]), 200

@api_bp.route('/api/borrow-requests', methods=['POST'])
@jwt_required()
def submit_borrow_request():
    data = request.get_json()
    new_request = BorrowRequest(
        user_id=data['user_id'],
        book_id=data['book_id'],
        start_date=data['start_date'],
        end_date=data['end_date']
    )
    db.session.add(new_request)
    db.session.commit()
    return jsonify({"message": "Borrow request submitted."}), 201

@api_bp.route('/api/users/<int:user_id>/borrow-history', methods=['GET'])
@jwt_required()
def personal_borrow_history(user_id):
    history = BorrowHistory.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "book_id": hist.book_id,
        "start_date": hist.start_date,
        "end_date": hist.end_date
    } for hist in history]), 200