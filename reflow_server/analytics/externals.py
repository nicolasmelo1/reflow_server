from django.conf import settings

from reflow_server.core import externals

class ReflowExternal(externals.External):
    host = settings.FRONT_END_APP_HOST
    secure = False

    def create_new_record(
        self, company_name, closing_forecast, value, responsible, 
        status, contact_name, contact_email, contact_phone, market, next_follow_up, 
        partner='', plan='Starter', number_of_users=1
    ):  
        response = self.post(
            url='/api/v0/MQ.844j2Nsnc4mtUDjF7LKkWRqC8BQ/negocios', 
            data={
                "Informações Gerais": {
                    "Nome da Empresa": company_name,
                    "Previsão de Fechamento": closing_forecast,
                    "Responsável": responsible,
                    "Status": status,
                    "Parceiro": partner
                },
                "Informações Adicionais": {
                    "Nome do Contato": contact_name,
                    "Email": contact_email,
                    "Telefone": contact_phone,
                    "Mercado": market,
                    "Próximo follow-up": next_follow_up
                },
                "Valores": {
                    "Valor do Setup": value,
                    "Setup com Desconto": 0,
                    "Plano": plan,
                    "Número de usuários": number_of_users
                }
            },
            headers={
                'Authorization': f'Bearer f7aee1dd-6044-47ae-8981-fc967ffd2962'
            }
        )
        print('BREAKPOINT')
        print(response.content)