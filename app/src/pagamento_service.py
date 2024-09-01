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
            payload_pedido = json.dumps(pedido)
            self.lambda_client.invoke(FunctionName="notifica-pagamentos", InvocationType="Event", Payload=payload_pedido)
            self.sqs_client.send_message(self.url_notificacao_pagamento, payload_pedido)
        
        return sucesso_pagamento
