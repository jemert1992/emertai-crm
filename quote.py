from flask import Blueprint, jsonify, request
from src.models.quote import Quote, QuoteItem, db
from datetime import datetime
from decimal import Decimal

quote_bp = Blueprint('quote', __name__)

@quote_bp.route('/quotes', methods=['GET'])
def get_quotes():
    status = request.args.get('status')
    client_id = request.args.get('client_id')
    
    query = Quote.query
    if status:
        query = query.filter_by(status=status)
    if client_id:
        query = query.filter_by(client_id=client_id)
    
    quotes = query.all()
    return jsonify([quote.to_dict() for quote in quotes])

@quote_bp.route('/quotes', methods=['POST'])
def create_quote():
    data = request.json
    quote = Quote(
        client_id=data['client_id'],
        project_id=data.get('project_id'),
        title=data['title'],
        description=data.get('description'),
        status=data.get('status', 'draft'),
        valid_until=datetime.fromisoformat(data['valid_until']).date() if data.get('valid_until') else None
    )
    db.session.add(quote)
    db.session.flush()  # Get the quote ID
    
    # Add quote items if provided
    if 'items' in data:
        total_amount = Decimal('0')
        for item_data in data['items']:
            item = QuoteItem(
                quote_id=quote.id,
                service_name=item_data['service_name'],
                description=item_data.get('description'),
                quantity=item_data.get('quantity', 1),
                unit_price=Decimal(str(item_data['unit_price'])),
                total_price=Decimal(str(item_data['quantity'] * item_data['unit_price']))
            )
            total_amount += item.total_price
            db.session.add(item)
        
        quote.total_amount = total_amount
    
    db.session.commit()
    return jsonify(quote.to_dict()), 201

@quote_bp.route('/quotes/<int:quote_id>', methods=['GET'])
def get_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    return jsonify(quote.to_dict())

@quote_bp.route('/quotes/<int:quote_id>', methods=['PUT'])
def update_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    data = request.json
    
    quote.title = data.get('title', quote.title)
    quote.description = data.get('description', quote.description)
    quote.status = data.get('status', quote.status)
    
    if data.get('valid_until'):
        quote.valid_until = datetime.fromisoformat(data['valid_until']).date()
    
    db.session.commit()
    return jsonify(quote.to_dict())

@quote_bp.route('/quotes/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    db.session.delete(quote)
    db.session.commit()
    return '', 204

@quote_bp.route('/quotes/<int:quote_id>/items', methods=['POST'])
def add_quote_item(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    data = request.json
    
    item = QuoteItem(
        quote_id=quote_id,
        service_name=data['service_name'],
        description=data.get('description'),
        quantity=data.get('quantity', 1),
        unit_price=Decimal(str(data['unit_price'])),
        total_price=Decimal(str(data['quantity'] * data['unit_price']))
    )
    db.session.add(item)
    
    # Update quote total
    quote.total_amount = sum(item.total_price for item in quote.items) + item.total_price
    
    db.session.commit()
    return jsonify(item.to_dict()), 201

@quote_bp.route('/quotes/<int:quote_id>/items/<int:item_id>', methods=['PUT'])
def update_quote_item(quote_id, item_id):
    quote = Quote.query.get_or_404(quote_id)
    item = QuoteItem.query.get_or_404(item_id)
    data = request.json
    
    item.service_name = data.get('service_name', item.service_name)
    item.description = data.get('description', item.description)
    item.quantity = data.get('quantity', item.quantity)
    item.unit_price = Decimal(str(data.get('unit_price', item.unit_price)))
    item.total_price = item.quantity * item.unit_price
    
    # Update quote total
    quote.total_amount = sum(i.total_price for i in quote.items)
    
    db.session.commit()
    return jsonify(item.to_dict())

@quote_bp.route('/quotes/<int:quote_id>/items/<int:item_id>', methods=['DELETE'])
def delete_quote_item(quote_id, item_id):
    quote = Quote.query.get_or_404(quote_id)
    item = QuoteItem.query.get_or_404(item_id)
    
    db.session.delete(item)
    
    # Update quote total
    quote.total_amount = sum(i.total_price for i in quote.items if i.id != item_id)
    
    db.session.commit()
    return '', 204

@quote_bp.route('/quotes/<int:quote_id>/send', methods=['POST'])
def send_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    quote.status = 'sent'
    db.session.commit()
    return jsonify({'message': 'Quote sent successfully', 'quote': quote.to_dict()})

