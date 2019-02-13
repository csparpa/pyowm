class ConfigurationNotFoundError(Exception):
    """Raised when configuration source file is not available"""
    pass


class ConfigurationParseError(Exception):
    """Raised on failures in parsing configuration data"""
    pass
