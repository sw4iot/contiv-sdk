import json
import os

import requests
import urllib3

urllib3.disable_warnings()


class ContivSdk:

    @staticmethod
    def get_instance():
        """ Static access method.
        :rtype: ContivSdk
        :return: ContivSdk instance
        """
        return ContivSdk(host=os.environ.get('SW4IOT_CONTIV_HOST', 'contiv'),
                         port=os.environ.get('SW4IOT_CONTIV_PORT', '10000'),
                         user=os.environ.get('SW4IOT_CONTIV_USER', 'admin'),
                         password=os.environ.get('SW4IOT_CONTIV_PASSWORD', 'admin'))

    def __init__(self, host, port, user, password):
        self.base_url = 'https://{}:{}/api/v1'.format(host, port)
        self.user = user
        self.password = password
        #
        self.token = None
        self.login()

    def __headers(self, token=True):
        headers = {
            'Content-Type': 'application/json',
        }
        if token:
            headers['X-Auth-Token'] = self.token
        return headers

    def __post_request(self, url, data, token=True):
        """
        Post request

        :param url:
        :param data:
        :param token:
        :return:
        """
        return requests.post('{}/{}/'.format(self.base_url, url), json=data, headers=self.__headers(token),
                             verify=False)

    def __delete_request(self, url):
        """
        Delete request

        :param url:
        :return:
        """
        return requests.delete('{}/{}/'.format(self.base_url, url), headers=self.__headers(True), verify=False)

    def login(self):
        """
        Contiv login
        """
        r = self.__post_request('auth_proxy/login', data={
            "username": self.user,
            "password": self.password
        }, token=False)
        if r.status_code == requests.codes.ok:
            self.token = json.loads(r.content)['token']

    def post_tenant(self, tenant_name):
        """
        Create tenant

        :param tenant_name:
        :return:
        """
        r = self.__post_request('tenants/{}'.format(tenant_name), data={
            "key": tenant_name,
            "tenantName": tenant_name
        })
        return json.loads(r.content) if r.status_code == requests.codes.ok else None

    def delete_tenant(self, tenant_name):
        """
        Delete tenant

        :param tenant_name:
        :return:
        """
        r = self.__delete_request('tenants/{}'.format(tenant_name))
        return True if r.status_code == requests.codes.ok else None

    def post_network(self, tenant_name, encap, gateway, key, network_name, nw_type, subnet):
        """
        Create network

        :param tenant_name:
        :param encap:
        :param gateway:
        :param key:
        :param network_name:
        :param nw_type:
        :param subnet:
        :return:
        """
        r = self.__post_request('networks/{}:{}-net'.format(tenant_name, tenant_name), data={
            'encap': encap,
            'gateway': gateway,
            'key': key,
            'networkName': network_name,
            'nwType': nw_type,
            'subnet': subnet,
            'tenantName': tenant_name
        })
        return json.loads(r.content) if r.status_code == requests.codes.ok else None

    def delete_network(self, tenant_name):
        """
        Delete network

        :param tenant_name:
        :return:
        """
        r = self.__delete_request('networks/{}:{}-net'.format(tenant_name, tenant_name))
        return True if r.status_code == requests.codes.ok else None
