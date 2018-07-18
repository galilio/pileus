#-*- encoding: utf-8

from datetime import datetime
from decimal import Decimal

import json

class _Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        elif isinstance(o, datetime):
            return datetime.strftime('%Y-%m-%d %H%M%S')
        
        return super(_Encoder, self).default(o)

