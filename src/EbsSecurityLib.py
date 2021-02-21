from EbsSecurityApi import EbsSecurityApi


class EbsSecurityLib:
    """
    Class designed as high level handler of EBS Security API. Supports only one monitored object (yet).
    Functionality is limited to log in, get partition status or arm/disarm partition
    """
    def __init__(self, server_address, email, pin):
        """
        Init of EBS Security library.
        Will raise an error, if user can't be authenticated.
        :param server_address:  Address of server (ex: ac-ebs.juwentus.pl/ava)
        :param email: User email
        :param pin: User pin/password
        """
        self.api = EbsSecurityApi(server_address)
        self.api.login(email, pin)
        objects = self.api.check_update()
        if len(objects) > 1:
            raise Exception('Accounts with more than one object are not supported (yet)')
        self.obj_id = objects[0]['id']
        self.partitions = dict()
        self.update_partitions()

    def update_partitions(self):
        """
        Updates partition state. Will raise an error in case of failure.
        """
        full_info = self.api.full_update([self.obj_id])
        self.partitions = {
            o['nr']: {'id': o['id'], 'state': o['state'], 'name': o['name']}
            for o in full_info[0]['partitions']
        }

    def get_arm(self, partition_nr):
        """
        Get partition state.
        To get newest state, please call 'update_partitions' firstly to update local state of partitions.
        Will raise an error in case of failure.
        :param partition_nr: Number of partition, like 1 or 2.
        :return: True - partition is armed, False - partition is disarmed
        """
        if self.partitions[partition_nr]['state']:
            return True
        else:
            return False

    def set_arm(self, partition_nr, arm):
        """
        Set partition state. Will raise an error in case of failure.
        :param partition_nr: Number of partition, like 1 or 2.
        :param arm: True - arm partition, False - disarm partition
        """
        if arm:
            new_state = 1
        else:
            new_state = 0
        self.api.set_partition_state(self.partitions[partition_nr]['id'], new_state)
        self.update_partitions()
