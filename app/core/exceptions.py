class AppException(Exception):
    status_code: int = 500
    detail: str = "Erro interno"

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.__class__.detail
        super().__init__(self.detail)


class NotFoundException(AppException):
    status_code = 404
    detail = "Recurso não encontrado"


class ConflictException(AppException):
    status_code = 409
    detail = "Recurso já existe"


class BusinessRuleException(AppException):
    status_code = 422
    detail = "Regra de negócio violada"