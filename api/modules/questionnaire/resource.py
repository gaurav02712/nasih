from flask import request, g, current_app

from api.common import KMessages
from api.common.enums import RoleType
from api.config.initialization import api
from api.helpers.aws import AWSManager
from api.helpers.decorators import allow
from api.helpers.extension import Resource
from api.helpers.jwt_helper import jwt_required
from api.helpers.response import ApiResponse
from api.modules.questionnaire.model import QuestionModel, QOptionsModel, UserQAnswerModel
from api.modules.questionnaire.schema import QuestionSchema, UserQAnswerSchema
from api.modules.user.model import UserModel
from api.modules.user.schema import UserSchema

ns_questionnaire = api.namespace('questions', description='User Questionnaire Module')


class Question(Resource):
    # @ns_questionnaire.doc(params={'user_id': 'an Int value'})
    @ns_questionnaire.doc(security="Authorization")
    @jwt_required
    @allow([RoleType.SUPER_ADMIN])
    def get(self):
        """Get all questionnaire"""
        questions = QuestionModel().find_all()
        from api.modules.questionnaire.schema import QuestionSchema
        return ApiResponse.success(QuestionSchema(many=True).dump(questions), 200)

    create_question_parser = QuestionModel.get_parser_create_new_question()

    # @ns_questionnaire.doc(security="Authorization")
    # @jwt_required
    @ns_questionnaire.expect(create_question_parser)
    # @allow([RoleType.SUPER_ADMIN])
    def post(self):
        """add new questionnaire and options"""
        param_dict = self.create_question_parser.parse_args()
        question = QuestionModel(**{'question': param_dict['question']})
        option_icons = list(param_dict['option_icons'])

        for num, option in enumerate(param_dict['option']):
            option: QOptionsModel = QOptionsModel(**{'option': option})
            directory_path = current_app.config['QUESTION_ICONS_DIR']
            option.option_icon = AWSManager().updateImage(option_icons[num], directory_path)
            question.options.append(option)
        # TODO: Have to delete saved file if there will any expection while saving question
        question.save()
        return ApiResponse.success(QuestionSchema().dump(question), 200)

    @ns_questionnaire.doc(security="Authorization")
    @jwt_required
    @allow([RoleType.SUPER_ADMIN])
    def delete(self, question_id: int):
        """new questionnaire and options"""
        question = QuestionModel().get_by_id(question_id)
        question.delete()
        return ApiResponse.success(None, 200, message=KMessages.QUESTION_DELETED)


class UserQAnswer(Resource):
    @ns_questionnaire.doc(security="Authorization")
    @jwt_required
    def get(self):
        """get all submitted questionnaire by you"""
        questions = UserQAnswerModel.query.filter_by(user_id=g.user_id).all()
        return ApiResponse.success(UserQAnswerSchema(many=True).dump(questions), 200)

    submit_qanswer_parser = UserQAnswerModel.get_parser_submit_qanswer()

    @ns_questionnaire.doc(security="Authorization")
    @jwt_required
    @ns_questionnaire.expect(submit_qanswer_parser)
    def post(self):
        """submit new answer"""
        param_dict = self.submit_qanswer_parser.parse_args()
        param_dict['user_id'] = g.user_id
        user_answer = UserQAnswerModel(**param_dict)
        user_answer.save()
        return ApiResponse.success(None, 200, KMessages.DATA_SAVED)
