import treq
from xml.etree import cElementTree as et
from twisted.internet import defer
from txccb import errors


class CCBClient(object):
    config = None

    def __init__(self, config):
        self.config = config

    def _request(self, service, method='GET', params=None):
        ''' Make the actual request '''
        if not self.config:
            raise errors.CCBError('Internal Error: No CCB configuration')
        if not params:
            params = {}
        params['srv'] = service
        auth = (self.config.username, self.config.password)
        d = treq.request(method, self.config.url, params=params, auth=auth)
        d.addCallback(self._get_content, params["srv"])
        return d

    def _get_content(self, res, srv=None):
        ''' Get the content from the response '''
        d = treq.content(res)
        d.addCallback(self._parse_response, srv)
        return d

    def _parse_response(self, response, srv=None):
        ''' Parse the XML response from the server '''
        try:
            content = et.fromstring(response)
        except et.ParseError:
            raise errors.CCBError('Internal Error')
        response = content.find('response')
        if response.find('errors'):
            error = response.find('errors')[0]
            raise errors.CCBError(error.text, error.get('number'))
        return response

    @defer.inlineCallbacks
    def transaction_detail_type_list(self):
        ''' Get list of accounts '''
        res = yield self._request('transaction_detail_type_list')
        tlist = res.find('transaction_detail_types')
        out = []
        for i in tlist:
            row = {'id': i.get('id')}
            parent = i.find('parent')
            row['parent'] = parent.get('id', None)
            row['name'] = i.find('name').text
            campuses = []
            for j in i.find('campuses'):
                campuses.append({'id': j.get('id'), 'name': j.text})
            row['campuses'] = campuses

            out.append(row)

        defer.returnValue(out)


client = CCBClient(None)
