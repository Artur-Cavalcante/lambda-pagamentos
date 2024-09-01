from time import sleep
from aws_lambda_powertools import Logger

class GatewayService():
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
    
    def realizar_pagamento(self, info_pagamento: dict) -> bool:
        self.logger.info("Realizando pagamento no gateway.")
        sleep(2)
        self.logger.info("Pagamento processado com sucesso.")
        return True
