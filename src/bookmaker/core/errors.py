class BookmakerError(Exception):
    """Tüm bookmaker hatalarının tabanı."""


class ConfigError(BookmakerError):
    """Yapılandırma hatası."""


class ValidationError(BookmakerError):
    """Doğrulama hatası."""


class WorkspaceError(BookmakerError):
    """Çalışma alanı hatası."""


class PipelineError(BookmakerError):
    """Pipeline hatası."""
