#!/usr/bin/env python

# Copyright (c) 2022 Project CHIP Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple hexmerge script for combining the MCUBoot image and App

This script provides a basic utility to combine the OAD application binary file with the MCUBoot hex file. The output is a combined hex file that can be programmed on the target and run.

Run with:
    python oad_merge_tool.py <App hex (CC13x4)> <MCUBoot (CC13x4) hex> <output>
"""

import sys

import intelhex

oad_bin_file = sys.argv[1]
mcuboot_hex_file = sys.argv[2]
combined_hex = sys.argv[3]

# merge binary executable with bim hex file
ota_image = intelhex.IntelHex()
if (oad_bin_file.endswith('hex')):
    ota_image.fromfile(oad_bin_file, format='hex')

else:
    ota_image.fromfile(oad_bin_file, format='bin')

mcuboot_hex = intelhex.IntelHex()
mcuboot_hex.fromfile(mcuboot_hex_file, format='hex')

# MCUBoot image has a very large address range due to the CCFG - we can allow the Matter Image to overlap with the MCUBoot image
ota_image.merge(mcuboot_hex, overlap='ignore')

ota_image.tofile(combined_hex, format='hex')
