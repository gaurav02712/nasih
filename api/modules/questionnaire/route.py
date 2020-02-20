from api.modules.questionnaire.resource import ns_questionnaire, Question, UserQAnswer

ns_questionnaire.add_resource(Question, '/', methods=['GET', 'POST'])
ns_questionnaire.add_resource(Question, '/<int:question_id>', methods=['DELETE'])

ns_questionnaire.add_resource(UserQAnswer, '/user')
