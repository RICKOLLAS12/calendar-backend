"""
Logging utilities for the Calendar Management application.
Provides centralized logging functions and patterns.
"""
import logging
import json
from functools import wraps
from django.conf import settings

# Get loggers for different components
api_logger = logging.getLogger('calendar_management.api')
auth_logger = logging.getLogger('authentification')
security_logger = logging.getLogger('django.security')

def log_api_request(view_func):
    """
    Decorator to log API requests
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = getattr(request, 'user', None)
        username = user.username if user and user.is_authenticated else 'Anonymous'

        api_logger.info(
            f"API Request: {request.method} {request.path} by {username} "
            f"from {get_client_ip(request)}"
        )

        try:
            response = view_func(request, *args, **kwargs)
            api_logger.info(
                f"API Response: {request.method} {request.path} - Status: {response.status_code}"
            )
            return response
        except Exception as e:
            api_logger.error(
                f"API Error: {request.method} {request.path} - {str(e)}",
                exc_info=True
            )
            raise

    return wrapper

def log_security_event(event_type, user=None, ip_address=None, details=None):
    """
    Log security-related events
    """
    message = f"SECURITY: {event_type}"
    if user:
        message += f" - User: {user}"
    if ip_address:
        message += f" - IP: {ip_address}"
    if details:
        message += f" - Details: {json.dumps(details)}"

    security_logger.info(message)

def log_user_action(user, action, resource=None, details=None):
    """
    Log user actions for audit trail
    """
    message = f"USER ACTION: {user.username} - {action}"
    if resource:
        message += f" - Resource: {resource}"
    if details:
        message += f" - Details: {json.dumps(details)}"

    auth_logger.info(message)

def get_client_ip(request):
    """
    Get client IP address from request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_performance(func_name, execution_time, user=None):
    """
    Log performance metrics
    """
    message = f"PERFORMANCE: {func_name} took {execution_time:.2f}s"
    if user:
        message += f" - User: {user}"

    logging.getLogger('calendar_management.performance').info(message)

class APILogger:
    """
    Advanced API logging utility
    """

    def __init__(self, logger_name='calendar_management.api'):
        self.logger = logging.getLogger(logger_name)

    def log_request(self, request, response=None, error=None):
        """Log API request with full details"""
        user = getattr(request, 'user', None)
        username = user.username if user and user.is_authenticated else 'Anonymous'
        ip = get_client_ip(request)

        log_data = {
            'method': request.method,
            'path': request.path,
            'user': username,
            'ip': ip,
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        }

        if response:
            log_data['status_code'] = response.status_code
            log_data['response_size'] = len(str(response.data)) if hasattr(response, 'data') else 0

        if error:
            log_data['error'] = str(error)
            self.logger.error(f"API Error: {json.dumps(log_data)}")
        else:
            self.logger.info(f"API Request: {json.dumps(log_data)}")

# Global API logger instance
api_logger_instance = APILogger()