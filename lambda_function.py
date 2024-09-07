import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import event_source, SQSEvent

from src.pagamento_service import PagamentoService

logger = Logger(service="pagamentos")
pagamento_service = PagamentoService(logger)

@event_source(data_class=SQSEvent)
def lambda_handler(event: SQSEvent, context) -> dict:
    try:
        for record in event.records: 
            logger.info(f"Event: {record.body}")
            pagamento_service.processar_pagamento(json.loads(record.body))

        return {
            "status_code": 200,
            "body": "Sucesso"
        }            
    except Exception as ex:
        logger.error(f"Erro ao processar pagamento: {ex}")
        return {
            "status_code": 500,
            "body": "Erro ao processar evento"
        }

# event = {
#     "Records": [
#         {
#             "body": {
#                 "id_pedido": 123,
#                 "id_cliente": 456,
#                 "email_cliente": "teste@mailinator.com",
#                 "itens": [
#                     {
#                         "nome": "hamburguer",
#                         "quantidade": 2,
#                         "valor": 40.0
#                     },
#                     {
#                         "nome": "refrigerante",
#                         "quantidade": 2,
#                         "valor": 8.50
#                     }
#                 ]
#             }
#         }
#     ]
# }

# try:
#     result = lambda_handler(event, None)
#     print(result)
# except Exception as e:
#     print(f"An error occurred: {str(e)}")
