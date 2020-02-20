from api.common.base.model import BaseModel
from api.config.initialization import db
from flask_restplus import reqparse


class UserQAnswerModel(BaseModel):
    __tablename__ = 'user_question_releation'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey('question_option.id'), nullable=False)
    question = db.relationship('QuestionModel', uselist=True, lazy=True)

    @classmethod
    def get_parser_submit_qanswer(cls):
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('question_id', required=True, type=str)
        parser.add_argument('answer_id', required=True, type=str)
        return parser


class QOptionsModel(BaseModel):
    __tablename__ = 'question_option'
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    option = db.Column(db.String(80), nullable=False)
    option_icon_name = db.Column(db.String(45), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class QuestionModel(BaseModel):
    __tablename__ = 'question'
    question = db.Column(db.String(100), nullable=False)
    options = db.relationship(QOptionsModel, uselist=True, lazy=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def get_parser_create_new_question(cls):
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('question', required=True, type=str)
        parser.add_argument('option', required=True, action='append')
        parser.add_argument('option_icon_name', required=False, action='append')
        return parser
