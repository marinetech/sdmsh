"""Python app to operate few sdms."""

import ctypes
import socket
import array

# int   sdm_connect(char *ip, int port);
# int   sdm_send_cmd(int sockfd, int cmd_code, ...);
# int   sdm_extract_replay(char *buf, size_t len, sdm_pkt_t **cmd);
#
# void  smd_rcv_idle_state();

# struct sdm_pkt_t {
#     uint64_t magic;
#     uint8_t  cmd;
#     union {
#     struct {
#         uint16_t threshold;
#         uint8_t  gain_and_srclvl;
#     } __attribute__ ((packed));
#     struct {
#         uint16_t param;
#         uint8_t  dummy;
#     } __attribute__ ((packed));
#     char rx_len[3];
#     };
#     uint32_t data_len; /* in 16bit words */
#     uint16_t data[];
# }


class sdmControl:
    """Evologics SDM python wraper."""

    def __init__(self):
        """Constructor."""
        self.modems = []
        self.conn = {}
        self.sdm = ctypes.CDLL('sdm.so')
        self.SDM_PKG_MAGIC = 0x00000000ff7f0080

        self.SDM_CMD_STOP = 0
        self.SDM_CMD_TX = 1
        self.SDM_CMD_RX = 2
        self.SDM_CMD_REF = 3
        self.SDM_CMD_CONFIG = 4

        self.SDM_REPLAY_STOP = 0
        self.SDM_REPLAY_RX = 2
        self.SDM_REPLAY_BUSY = 254
        self.SDM_REPLAY_REPORT = 255

    def addModem(self, modemIP):
        """Add new modem tp the array."""
        self.modems.append(modemIP)
        print(self.modems)

    def removeModem(self, modemIP):
        """Remove modem from the array."""
        self.modems.remove(modemIP)
        print(self.modems)

    def ATP(self, modemIP):
        """Change the modem to physical mode."""
        sock = socket.create_connection((modemIP, 9200), 2)
        sock.send(b'AT?S\n')
        if (b'PHY' not in sock.recv(1024)):
            sock.send(b'ATP\n')
            sock.recv(1024)

    def connect(self):  # , modemIP):
        """Connect to the modem."""
        # print("self.modems : " + self.modems)
        for m in self.modems:
            print("m : " + str(m))
            self.conn[m] = self.sdm.sdm_connect(m, 4200)
            # print("modem : " + str(m) + "\tconn : " + str(self.conn[m]))
            # print(self.sdm.sdm_send_cmd(self.conn[m], self.SDM_CMD_STOP))
            # print(self.sdm.sdm_send_cmd(self.conn[m],
            #                             self.SDM_CMD_CONFIG,
            #                             300,
            #                             5,
            #                             3))
            # with open('/tmp/tx') as f:
            #     content = f.readlines()
            # # a = array.array("h", range(len(content)))
            # content = [bytes(x.strip()) for x in content]
            # print(content[:100])
            # print(self.sdm.sdm_load_samples('/tmp/tx', len(content)))
            # print(self.sdm.sdm_send_cmd(self.conn[m],
            #                             self.SDM_CMD_TX, content, 4))


s = sdmControl()
s.ATP("192.168.0.148")
s.addModem("192.168.0.148")
s.ATP("192.168.0.147")
s.addModem("192.168.0.147")
s.connect()
