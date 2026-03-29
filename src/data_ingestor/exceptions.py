class BaseIngestorError(Exception):
    pass


class YearError(BaseIngestorError):
    pass


class HorspowerError(BaseIngestorError):
    pass


class VinError(BaseIngestorError):
    pass
