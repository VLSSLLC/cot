# September 2016, Glenn F. Matthews
# Copyright (c) 2013-2016 the COT project developers.
# See the COPYRIGHT.txt file at the top-level directory of this distribution
# and at https://github.com/glennmatthews/cot/blob/master/COPYRIGHT.txt.
#
# This file is part of the Common OVF Tool (COT) project.
# It is subject to the license terms in the LICENSE.txt file found in the
# top-level directory of this distribution and at
# https://github.com/glennmatthews/cot/blob/master/LICENSE.txt. No part
# of COT, including this file, may be copied, modified, propagated, or
# distributed except according to the terms contained in the LICENSE.txt file.

"""Package describing the Cisco IOSv virtual router platform."""

import logging

from COT.platforms.generic import GenericPlatform
from COT.data_validation import (
    ValueTooLowError, ValueTooHighError, validate_int,
)

logger = logging.getLogger(__name__)


class IOSv(GenericPlatform):
    """Platform-specific logic for Cisco IOSv."""

    PLATFORM_NAME = "Cisco IOSv"

    CONFIG_TEXT_FILE = 'ios_config.txt'
    LITERAL_CLI_STRING = None
    # IOSv has no CD-ROM driver so bootstrap configs must be provided on disk.
    BOOTSTRAP_DISK_TYPE = 'harddisk'
    SUPPORTED_NIC_TYPES = ["E1000"]

    @classmethod
    def guess_nic_name(cls, nic_number):
        """GigabitEthernet0/0, GigabitEthernet0/1, etc."""
        return "GigabitEthernet0/" + str(nic_number - 1)

    @classmethod
    def validate_cpu_count(cls, cpus):
        """IOSv only supports a single CPU."""
        validate_int(cpus, 1, 1, "CPUs")

    @classmethod
    def validate_memory_amount(cls, mebibytes):
        """IOSv has minimum 192 MiB (with minimal feature set), max 3 GiB."""
        if mebibytes < 192:
            raise ValueTooLowError("RAM", str(mebibytes) + " MiB", "192 MiB")
        elif mebibytes < 384:
            # Warn but allow
            logger.warning("Less than 384MiB of RAM may not be sufficient "
                           "for some IOSv feature sets")
        elif mebibytes > 3072:
            raise ValueTooHighError("RAM", str(mebibytes) + " MiB", "3 GiB")

    @classmethod
    def validate_nic_count(cls, count):
        """IOSv supports up to 16 NICs."""
        validate_int(count, 0, 16, "NICs")

    @classmethod
    def validate_serial_count(cls, count):
        """IOSv requires 1-2 serial ports."""
        validate_int(count, 1, 2, "serial ports")
