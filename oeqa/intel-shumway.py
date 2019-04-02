# Copyright (C) 2014 Intel Corporation
#
# Released under the MIT license (see COPYING.MIT)

# This module adds support to testimage.bbclass to deploy images and run
# tests on a Intelshumway (original "white" or Black models). The device must
# be set up as per README.hardware and the master image should be deployed
# onto the card so that it boots into it by default. For booting into the
# image under test we interact with u-boot over serial, so for the
# Intelshumway Black you will need an additional TTL serial cable since a
# serial interface isn't automatically provided over the USB connection as
# it is on the original Intelshumway ("white") version. The separate ext3
# partition that will contain the image to be tested must be labelled
# "testrootfs" so that the deployment code below can find it.
#
# NOTE: for the Intelshumway "white" (original version) you may need to use
# a script which handles the serial device disappearing on power down, such
# as scripts/contrib/serdevtry in OE-Core.

import os
import bb
import time
import subprocess
import sys
cpwd=os.getcwd()
sys.path.append("/buildarea1/lyang0/intel-x86-64-test/layers/oe-core/meta/lib/oeqa/controllers/")
import pexpect

import oeqa.utils.sshcontrol as sshcontrol
from oeqa.controllers.masterimage import MasterImageHardwareTarget


class IntelshumwayTarget(MasterImageHardwareTarget):



    def __init__(self, d):
        super(IntelshumwayTarget, self).__init__(d)

        self.deploy_cmds = [
                '/folk/vlm/commandline/vlmTool copyFile -s amazon -t 22025  -k /folk/lyang0/kernel',
                '/folk/vlm/commandline/vlmTool copyFile -s amazon -t 22025  -r /folk/lyang0/rootfs',
                ]


        if not self.serialcontrol_cmd:
            bb.fatal("This TEST_TARGET needs a TEST_SERIALCONTROL_CMD defined in local.conf.")



    def deploy(self):
        super(MasterImageHardwareTarget, self).deploy()
        self.master = sshcontrol.SSHControl(ip=self.ip, logfile=self.sshlog, timeout=600, port=self.port)
        for cmd in self.deploy_cmds:
            os.system(cmd)

    def _deploy(self):
        pass

    def power_cycle(self):
        if self.powercontrol_cmd:
            os.system(self.powercontrol_cmd)


    #fix me which is in  masteriamge.py mismatched with ./classes/testimage.bbclass
    def start(self, extra_bootparams=None):
        bb.plain("%s - boot test image on target" % self.pn)
        self._start()
        # set the ssh object for the target/test image
        self.connection = sshcontrol.SSHControl(self.ip, logfile=self.sshlog, port=self.port)
        bb.plain("%s - start running tests" % self.pn)

            
    def _start(self):
        self.power_cycle()
        #try:
        #    serialconn = pexpect.spawn(self.serialcontrol_cmd)
        #    serialconn.timeout=900
        #    serialconn.expect("login:",timeout=500)
        #    serialconn.sendline("root")
        #    serialconn.expect("root\@.*#")
        #    serialconn.close()
        #except pexpect.ExceptionPexpect as e:
        #    bb.fatal('Serial interaction failed: %s' % str(e))

        #self.power_cycle(self.master)
        # there are better ways than a timeout but this should work for now
        time.sleep(180)


    #def start(self, extra_bootparams=None):
    #    bb.plain("%s - boot test image on target" % self.pn)
    #    self._start()
    #    # set the ssh object for the target/test image
    #    self.connection = sshcontrol.SSHControl(self.ip, logfile=self.sshlog, port=self.port)
    #    bb.plain("%s - start running tests" % self.pn)

    def stop(self):
        bb.plain("stop target")
        self.power_cycle()
    #def _wait_until_booted(self):
    #    try:
    #        bb.fatal(self.serialcontrol_cmd)
    #        serialconn = pexpect.spawn(self.serialcontrol_cmd)
    #        serialconn.expect("login:", timeout=600)
    #        serialconn.close()
    #    except pexpect.ExceptionPexpect as e:
    #        bb.fatal('Serial interaction failed: %s' % str(e))
