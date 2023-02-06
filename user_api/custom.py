class SignatureVerificationError(Exception):
    """Custom exception class for signature verification failure"""
    pass

class OrderNotFoundError(Exception):
    """Custom exception class for order not found failure"""
    pass


class PaymentError(Exception):
    """Custom exception class for payment error"""
    pass

class PaymentCancelled(Exception):
    """Custom exception class for payment cancellation"""
    pass

class PaymentTimeout(Exception):
    """Custom exception class for payment timeout"""
    pass
    
