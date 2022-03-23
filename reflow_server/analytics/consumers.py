from asgiref.sync import sync_to_async

import json

class AnalyticsSurveyConsumer:
    async def after_connect(self):
        """
        This method runs when the user connects to the socket so we can run a special function for him, the login and the
        refresh token will probably won't work so we need this.
        """
        await self.verify_if_need_to_display_survey({'data': {'user_id': self.scope['user'].id}})

    async def verify_if_need_to_display_survey(self, event):
        pass
        """
        from reflow_server.analytics.services.survey import SurveyService
        survey_service = SurveyService(event['data']['user_id'])
        survey_id = await sync_to_async(survey_service.display_survey_id)()

        if survey_id != None:
            await self.send(text_data=json.dumps({
                'type': 'is_to_open_survey',
                'data': {
                    'survey_id': survey_id,
                    'user_id': event['data']['user_id'] 
                }
            }))
        """