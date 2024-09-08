import os
import json
import boto3
from aws_lambda_powertools import Logger

from src.services.gateway_service import GatewayService

class PagamentoService():
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self.gateway_service = GatewayService(self.logger)
        self.sqs_client = boto3.client("sqs")
        self.lambda_client = boto3.client("lambda")
        self.url_notificacao_pagamento = os.environ["url_notificacao_pagamento"]
    
    def processar_pagamento(self, pedido: dict) -> bool:
        itens = pedido["itens"]
        total_pedido = 0.0
        for item in itens:
            total_pedido += item["valor"]
        
        sucesso_pagamento = self.gateway_service.realizar_pagamento({
            "id_cliente": pedido["id_cliente"],
            "total_pedido": total_pedido
        })
        
        if sucesso_pagamento:
            pedido["total_pedido"] = total_pedido
            self.confirmar_pagamento(pedido)
            self.sqs_client.send_message(QueueUrl=self.url_notificacao_pagamento, MessageBody=json.dumps(pedido))
        
        return sucesso_pagamento
    
    def confirmar_pagamento(self, pedido: dict):
        event = {
            "httpMethod": "PUT",
            "path": "/confirmar_pagamento",
            "body": json.dumps(pedido)
        }
        print(event)
        self.lambda_client.invoke(FunctionName="api-pedidos", InvocationType="Event", Payload=json.dumps(event))
