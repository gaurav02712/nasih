from marshmallow import fields
from api.config.initialization import ma
from api.modules.questionnaire.model import QOptionsModel, QuestionModel, UserQAnswerModel


class QOptionsSchema(ma.ModelSchema):
    class Meta:
        model = QOptionsModel
        include_fk = True
        exclude = model.baseExcluded()


class QuestionSchema(ma.ModelSchema):
    options = fields.Nested(QOptionsSchema, many=True, dump_only=True)

    class Meta:
        model = QuestionModel
        include_fk = True
        exclude = model.baseExcluded()


class UserQAnswerSchema(ma.ModelSchema):
    question = fields.Nested(QuestionSchema, many=True, dump_only=True)

    class Meta:
        model = UserQAnswerModel
        include_fk = True
        exclude = model.baseExcluded()
