#!/usr/bin/env python
import sys
import os
import time
import json
from fabric.api import execute as fabric_run
from vpynup import provider
from vpynup import fabricant


def _load_config(config_path=None):
    dict_config = None
    if config_path:
        try:
            with open(config_path) as jsonfd:
                dict_config = json.load(jsonfd)
        except Exception as e:
            sys.stderr.write("json config loading failed:"
                             " {0}\n".format(e.message))
            sys.exit(1)
    else:
        sys.stderr.write("No config file provided or the file "
                         "could not be found\n")
        sys.exit(1)

    if not __validate_config(dict_config):
        sys.stderr.write("Json config is not valid: some attributes "
                         "are missing. Please check vpin documentation\n")
        sys.exit(1)

    return dict_config

def __validate_config(dict_config):
    rval = False

    if(dict_config and 'provider' in dict_config and
       'auth' in dict_config['provider'] and
       'instance' in dict_config['provider']):
        rval = True

    return rval

def init():
    rval = True
    _cwd = os.getcwd()

    _sdict = ({"provider": {
                   "name": "aws",
                   "auth": {
                       "aws_access_key_id": "",
                       "aws_secret_access_key": ""
                   },
                   "instance": {
                       "image_id": "ami-c30360aa",
                       "key_name": "",
                       "key_path": ""
                   }
                 }
              })

    _aws_access_key_id = raw_input('enter/copy your amazon access key id: ')
    _aws_secret_access_key = raw_input('enter/copy your amazon secret access id: ')
    _aws_sshkey_name = raw_input('enter the name of your amazon ssh key: ')
    _aws_sshkey_path = raw_input('enter the path to the corresponding private key (.pem file): ')

    if '' not in [ _aws_access_key_id, _aws_secret_access_key, _aws_sshkey_name, _aws_sshkey_path ]:
        _sdict['provider']['auth']['aws_access_key_id'] = _aws_access_key_id
        _sdict['provider']['auth']['aws_secret_access_key'] = _aws_secret_access_key
        _sdict['provider']['instance']['key_name'] = _aws_sshkey_name
        _sdict['provider']['instance']['key_path'] = _aws_sshkey_path

        try:
            _fname = "{0}/{1}".format(_cwd, "vpinup.json")
            with open(_fname, 'w') as jfd:
                json.dump(_sdict, jfd, indent=4)
        except IOError as e:
            sys.stderr.write("File {0} creation failed: {1}".format(_fname, e.strerror))
            rval = False

#            _env_dir = "{0}/{1}".format(_cwd, ".vpinup/")
#            if not os.path.exists(_env_dir):
#                try:
#                    os.mkdir(_env_dir)
#                except OSError as e:
#                    sys.stderr.write("Environement directory creation failed: {0}".format(e.strerror))
#                    rval = False
    else:
        sys.stderr.write("Not all required parameters have been provided.\n")
        rval = False
    return rval

def up():
    _r = start()
    if _r is not None:
        print gate_hostname()
        provision()

    return _r

def start(wait=True):
    _cwd = os.getcwd()
    _config_file = "{0}/{1}".format(_cwd), "vpinup.json"
    _configdict = _load_config(_config_file)
    _auth_params = _config_dict['provider']['auth']
    _instance_params = _config_dict['provider']['instance']
    
    _instance = None
    conn = provider.cloud_connect(**_auth_params)

    if conn is not None:
        _instance = provider.start_instance(conn, _instance_params)
   
    if _instance is not None:
        _istatus = 'pending'
        while(_istatus != 'running' and wait):
            _istatus = gate_status()
            sys.stdout.write("Wait until instance is running. Status is: {0}\n".format(_istatus))
            time.sleep(5)
        instance = _instance
    return _instance


def provision():
    pass
 #       fabric_run(fabricant.provision(gate_hostname(), self.instance_params['key_path']))

def stop():
    _instance = None

    _auth_params = LOLOLOLOL

    conn = provider.cloud_connect(**_auth_params)
    if conn is None:
        conn = provider.cloud_connect(**_auth_params)
    if conn and _instance is not None:
        provider.terminate_instance(conn, _instance.id)

def gate_status(instance):
    rval = 'halted'
    if instance:
        instance.update()
        rval = instance.status
    return rval

def gate_hostname(instance):
    instance.update()
    return instance.public_dns_name

def save(instance):
    _cwd = os.getcwd()
    _config_file = "{0}/{1}".format(_cwd), "vpinup.json"
    if os.path.exists(_config_file):
        with open(_config_file) as jfd:
            jdict = json.load(jfd)

        if self.instance:
            jdict['provider']['instance']['instance_id'] = _instance.id
            jdict['provider']['instance']['instance_status'] = _instance.status

        with open(_config_file, "w") as jfd:
            json.dump(jdict, jfd)
    else:
        sys.stderr.write("Session could not be save")

