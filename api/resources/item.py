from flask_restful import Resource, reqparse, abort, fields, marshal_with
from api import db 

class ItemModel(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  topic_id = db.Column(db.Integer, nullable=False)
  body = db.Column(db.Text, nullable=False)
  answer = db.Column(db.Text, nullable=False)
  
  def __repr__(self):
    return f"Item(body={body}, answer={answer})"

#if db does not exist yet, run server once then comment out the line below
# db.create_all()
item_put_args = reqparse.RequestParser()
item_put_args.add_argument("topic_id", type=int, help="Topic of item", required=True)
item_put_args.add_argument("body", type=str, help="Body of item", required=True)
item_put_args.add_argument("answer", type=str, help="Answer of item", required=True)

item_update_args = reqparse.RequestParser()
item_update_args.add_argument("topic_id", type=int, help="Topic of item", required=False)
item_update_args.add_argument("body", type=str, help="Body of item", required=False)
item_update_args.add_argument("answer", type=str, help="Answer of item", required=False)

resource_fields = {
  'id': fields.Integer,
  'topic_id': fields.Integer,
  'body': fields.String,
  'answer': fields.String,
}

class Item(Resource):
  @marshal_with(resource_fields)
  def get(self, item_id):
    item = ItemModel.query.filter_by(id=item_id).first_or_404()
    return item

  @marshal_with(resource_fields)
  def put(self, item_id):
    if ItemModel.query.get(item_id):
      abort(409, message="Item ID already taken")
    args = item_put_args.parse_args()
    item = ItemModel(id=item_id, topic_id=args['topic_id'], body=args['body'], answer=args['answer'])
    db.session.add(item)
    db.session.commit()
    return item, 201

  @marshal_with(resource_fields)
  def patch(self, item_id):
    if ItemModel.query.filter_by(id=item_id).first() is None:
      abort(404, message="Item does not exist")

    args = item_update_args.parse_args()
    item = ItemModel.query.filter_by(id=item_id).first_or_404()

    if args['topic_id']:
      setattr(item, 'topic_id', args['topic_id'])

    if args['body']:
      setattr(item, 'body', args['body'])

    if args['answer']:
      setattr(item, 'answer', args['answer'])

    db.session.commit()
    return item

  def delete(self, item_id):
    item = ItemModel.query.filter_by(id=item_id).first()
    if item is None:
      abort(404, message="Item does not exist")

    db.session.delete(item)
    db.session.commit()
    return '', 204