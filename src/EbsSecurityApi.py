import requests
import json
import uuid


class EbsSecurityApi:
    """
    API class for "EBS Security" interface used by Android app with the same name.
    Used by various security agencies in Poland like Juwentus
    """

    def __init__(self, server_address: str):
        """
        Init EBS Security API class
        :param server_address: Address of server (ex: ac-ebs.juwentus.pl/ava)
        """
        self.server_address = 'https://' + server_address.replace("/ava", "")  # the same logic as per mobile app
        self.token = None
        self.uuid = str(uuid.uuid1())  # seems to be required to be something

    def login(self, email, pin):
        """
        Log in to server. User needs firstly to register via Android app with email and password/pin
        :param email: User email
        :param pin: User pin/password
        """
        data = {
            'user_mail': email,
            'user_code': pin,
            'uniq_id': self.uuid,
            'get_logo': 0,
        }
        response_data = self.query('/ava/user-login', data)
        self.token = response_data['user']['token']

    def query(self, url, data):
        """
        Query an API. Raise an error in case of failure.
        :param url: Postfix to server address, ex: '/ava/user-login'
        :param data: Dictionary with query data..
        :return: Result of the query in dict format
        """
        response = requests.post(self.server_address + url, json=data)
        if response.status_code != 200:  # OK
            raise Exception(f"Incorrect response code, expected 200, got {response.status_code}")
        response_data = json.loads(response.content)
        if response_data['status_code'] != 0:
            raise Exception(f"Incorrect status code, expected 0, got {response_data['status_code']} with message: {response_data['status_message']}")
        return response_data

    def query_auth(self, url, data):
        """
        Query an API. Add authentication data. Raise an error in case of failure.
        :param url: Postfix to server address, ex: '/ava/user-login'
        :param data: Dictionary with query data..
        :return: Result of the query in dict format
        """
        if self.token is None:
            raise Exception("No token is available. Please provide a token or log in.")
        data['user_token'] = self.token
        data['uniq_id'] = self.uuid
        return self.query(url, data)

    def check_update(self):
        """
        Check update API command query
        :return: 'object' entry of response data.
        """
        response_data = self.query_auth('/ava/check-update', dict())
        return response_data['objects']

    def full_update(self, objects):
        """
        Full update API command query
        :param objects: List of object IDs to be queried. IDs can be obtained from 'check_update' function.
        :return:  'full_objects' entry of response data.
        """
        response_data = self.query_auth('/ava/full-update', {'objects': objects})
        return response_data['full_objects']

    def set_partition_state(self, id, state):
        """
        Set partition state. In case of failure, error will be raised.
        :param id: ID of partition. Can be obtained from 'full_update' function.
        :param state: Values accepted by API:
            DISARM = 0
            ARM = 1
            PARTIAL_ARM = 2
            NIGHT_MODE = 3
        """
        data = {
            'partition': id,
            'state': state
        }
        self.query_auth('/ava/set-partition', data)
