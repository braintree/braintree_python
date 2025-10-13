from datetime import datetime

class TransactionUsBankAccountRequest(object):
    def __init__(self, parent):
        self.parent = parent
        self._ach_mandate_text = None
        self._ach_mandate_accepted_at = None

    def ach_mandate_text(self, ach_mandate_text):
        self._ach_mandate_text = ach_mandate_text
        return self

    def ach_mandate_accepted_at(self, ach_mandate_accepted_at):
        self._ach_mandate_accepted_at = ach_mandate_accepted_at
        return self

    def done(self):
        return self.parent

    def to_param_dict(self):
        params = {}
        if self._ach_mandate_text is not None:
            params["ach_mandate_text"] = self._ach_mandate_text
        if self._ach_mandate_accepted_at is not None:
            if isinstance(self._ach_mandate_accepted_at, datetime):
                params["ach_mandate_accepted_at"] = self._ach_mandate_accepted_at.isoformat()
            else:
                params["ach_mandate_accepted_at"] = self._ach_mandate_accepted_at
        return params