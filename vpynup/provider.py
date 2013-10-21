import sys
from boto import ec2 as cloudapi
from boto import exception as cloudexception


def cloud_connect(**kwargs):
    conn = None

    try:
        if 'aws_access_key_id' in kwargs and 'aws_secret_access_key':
            conn = cloudapi.connection.EC2Connection(**kwargs)
        else:
            sys.stderr.write("Failed to connect to cloud provider: "
                             "check credentials\n")
    except cloudexception.NoAuthHandlerFound as e:
        sys.stderr.write("Failed to connect to cloud provider: "
                         "{0}\n".format(e.message))

    return conn


def create_instance(conn, instance_params):
    _instance = None
    _image_id = instance_params['image_id']
    _key_name = instance_params['key_name']

    _reservations = conn.run_instances(image_id=_image_id,
                                       key_name=_key_name,
                                       security_groups=['sgvpn'],
                                       instance_type='t1.micro')

    if(_reservations and (len(_reservations.instances) == 1)):
        _instance = _reservations.instances.pop()
    else:
        sys.stderr.write("Some parameters are not correctly set, "
                         "please check your json config file or "
                         "instance could not be started\n")
    return _instance


def start_instance(conn, instance_id=None):
    _instance = None
    if instance_id:
        ilist = conn.start_instances(instance_ids=[instance_id])
    else:
        sys.stderr.write("Cannot sart instance: no valid id provided")

    if len(ilist) != 1:
        sys.stderr.write("Cannot sart instance: no valid id provided")
    else:
        _instance = ilist.pop()
    return _instance


def stop_instance(conn, instance_id=None, force=False):
    rval = False
    if instance_id:
        ilist = conn.stop_instances(instance_ids=[instance_id], force=force)
    else:
        sys.stderr.write("Cannot stop instance: no valid id provided")

    if len(ilist) != 1:
        sys.stderr.write("Cannot stop instance: no valid id provided")
    else:
        rval = True
    return rval


def reboot_instance(conn, instance_id=None, force=False):
    rval = False
    if instance_id:
        ilist = conn.reboot_instances(instance_ids=[instance_id], force=force)
    else:
        sys.stderr.write("Cannot reboot instance: no valid id provided")

    if len(ilist) != 1:
        sys.stderr.write("Cannot reboot instance: no valid id provided")
    else:
        rval = True
    return rval


def terminate_instance(conn, instance_id):
    rval = False
    _instances_terminated = conn.terminate_instances(instance_ids=[instance_id])

    if(_instances_terminated and (len(_instances_terminated) == 1)):
        rval = True
    else:
        sys.stderr.write("Stopping the instance failed: "
                         "check your aws management console\n")
    return rval
