''' Resource objects '''

from twisted.internet import defer
from txccb.client import client


class Resource(object):
    _data = None

    def __init__(self):
        if self._data:
            for k, v in self._data.iteritems():
                setattr(self, k, v)

    def _set_data(self, data):
        for k, v in data.iteritems():
            setattr(self, k, v)


class Individual(Resource):

    def __init__(self):
        self._data = {
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
    def search(cls, **fields):
        res = yield client._request("individual_search", params=fields)
        tlist = res.find('individuals')
        tlist = tlist.findall('individual')
        out = []
        for i in tlist:
            row = cls()
            row._set_data({elem.tag: elem.text for elem in i})
            out.append(row)
        defer.returnValue(out)

    @classmethod
    @defer.inlineCallbacks
    def find(cls, individual_id):
        fields = {"individual_id": individual_id}
        res = yield client._request("individual_search", params=fields)
        defer.returnValue(res)


class Gift(Resource):
    def __init__(self):
        self._data = {
            "coa_category_id": None,
            "individual_id": None,
            "amount": None,
            "name": None,
            "merchant_transaction_id": None,
            "merchant_authorization_code": None,
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
