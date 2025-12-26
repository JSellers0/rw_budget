import os
import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger  # Add to requirements.txt

def setup_logging(app):
    """Configure application logging"""
    
    # Ensure log directory exists
    log_dir = app.config.get('LOG_DIR', '/app/logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Remove default handlers
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)
    
    # JSON formatter
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    
    # File handler
    file_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, 'app.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Console handler (for development)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG if app.debug else logging.INFO)
    
    # Add handlers
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
    
    # Disable Werkzeug's default logging
    logging.getLogger('werkzeug').setLevel(logging.WARNING)