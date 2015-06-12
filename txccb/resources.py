''' Resource objects '''

from twisted.internet import defer
from txccb.client import client as txclient


class Resource(object):
    _data = None

    def __init__(self, client=None):
        if self._data is None:
            self._data = {}
        if client is None:
            self.client = txclient
        else:
            self.client = client

    def _set_data(self, data):
        for k, v in data.iteritems():
            if k in self._data:
                self._data[k] = v

    def __getattr__(self, key):
        if key in self._data:
            return self._data[key]
        raise AttributeError(key)

    def __iter__(self):
        return self._data.iteritems()

    @classmethod
    def _parse(cls, response):
        data = {}
        if response.keys():
            for k in response.keys():
                data[k] = response.get(k)
        for elem in response:
            key = elem.tag
            if elem.keys():
                val = {}
                for k in elem.keys():
                    val[k] = elem.get(k)
                val['value'] = elem.text
            elif len(elem):
                val = []
                for i in elem:
                    val.append(cls._parse(i))
            else:
                val = elem.text
            data[key] = val
        return data


class Individual(Resource):

    def __init__(self):
        self._data = {
            'id': None,
            'sync_id': None,
            'other_id': None,
            'giving_number': None,
            'campus': None,
            'family': None,
            'family_image': None,
            'family_position': None,
            'family_members': None,
            'first_name': None,
            'last_name': None,
            'middle_name': None,
            'legal_first_name': None,
            'full_name': None,
            'salutation': None,
            'suffix': None,
            'image': None,
            'email': None,
            'allergies': None,
            'addresses': None,
            'phones': None,
            'mobile_carrier': None,
            'gender': None,
            'marital_status': None,
            'birthday': None,
            'emergency_contact_name': None,
            'anniversary': None,
            'baptized': None,
            'deceased': None,
            'membership_type': None,
            'membership_date': None,
            'membership_end': None,
            'receive_email_from_church': None,
            'default_new_group_messages': None,
            'default_new_group_comments': None,
            'default_new_group_digest': None,
            'default_new_group_sms': None,
            'privacy_settings': None,
            'active': None,
            'creator': None,
            'modifier': None,
            'created': None,
            'modified': None,
            'user_defined_text_fields': None,
            'user_defined_date_fields': None,
            'user_defined_pulldown_fields': None
        }

        Resource.__init__(self)

    @classmethod
    @defer.inlineCallbacks
    def search(cls, client=None, **fields):
        if not client:
            client = txclient
        res = yield client._request("individual_search", params=fields)
        tlist = res.find('individuals')
        tlist = tlist.findall('individual')
        out = []
        for i in tlist:
            row = cls()
            data = cls._parse(i)
            row._set_data(data)
            out.append(row)
        defer.returnValue(out)

    @classmethod
    @defer.inlineCallbacks
    def find(cls, individual_id, client=None):
        if not client:
            client = txclient
        fields = {"individual_id": individual_id}
        res = yield client._request("individual_search", params=fields)
        # XXX Do stuff here
        defer.returnValue(res)


class Gift(Resource):
    def __init__(self):
        self._data = {
            "id": None,
            "gift_id": None,
            "coa_category_id": None,
            "individual_id": None,
            "amount": None,
            "name": None,
            "merchant_transaction_id": None,
            "merchant_authorization_code": None,
            "merchant_process_date": None,
            "merchant_notes": None,
            "first_name": None,
            "last_name": None,
            "street_address": None,
            "city": None,
            "state": None,
            "zip": None,
            "email": None,
            "phone": None,
            "campus_id": None,
            "payment_method_type": None
        }

        Resource.__init__(self)

    @classmethod
    def create(cls, client=None, **fields):
        if not client:
            client = txclient
        for i in ["coa_category_id", "individual_id", "amount"]:
            if i not in fields:
                raise KeyError("Missing requried key: {}".format(i))

        d = client._request("online_giving_insert_gift", params=fields)

        def _after(res):
            tlist = res.find('items')
            tlist = tlist.findall('item')
            out = []
            for i in tlist:
                row = cls()
                data = cls._parse(i)
                row._set_data(data)
                out.append(row)
            return out

        d.addCallback(_after)
        return d


class TransactionDetailType(Resource):

    def __init__(self):
        self._data = {
            "id": None,
            "name": None,
            "cash_bank_account": None,
            "account_number": None,
            "tax_deductible": None,
            "online_giving_enabled": None,
            "pledge_goal": None,
            "parent": None,
            "campuses": None
        }

        Resource.__init__(self)

    @classmethod
    @defer.inlineCallbacks
    def get_list(cls, client=None):
        if not client:
            client = txclient
        res = yield client._request("transaction_detail_type_list")
        tlist = res.find("transaction_detail_types")
        tlist = tlist.findall("transaction_detail_type")
        out = []
        for i in tlist:
            row = cls()
            data = cls._parse(i)
            row._set_data(data)
            out.append(row)
        defer.returnValue(out)
