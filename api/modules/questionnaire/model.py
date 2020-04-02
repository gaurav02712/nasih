from werkzeug.datastructures import FileStorage
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
    option_icon = db.Column(db.String(100), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class QuestionModel(BaseModel):
    __tablename__ = 'question'
    title = db.Column(db.String(100), nullable=True)
    question = db.Column(db.String(250), nullable=False)
    question_html = db.Column(db.String(250), nullable=True)
    options = db.relationship(QOptionsModel, uselist=True, lazy=True)
    is_single_choice = db.Column(db.Boolean, default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def get_parser_create_new_question(cls):
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('title', required=False, type=str)
        parser.add_argument('question', required=True, type=str)
        parser.add_argument('question_html', required=False, type=str)
        parser.add_argument('option', required=True, action='append')
        # parser.add_argument('option_icon_name', required=True, action='append')
        parser.add_argument('option_icons', required=True, type=FileStorage, location='files', action='append',
                            help='''option_icons length should be same as option list''')
        parser.add_argument('is_single_choice', required=True, type=bool, default=False)
        return parser
