#!/usr/bin/env python
# Copyright (c) 2014 Cisco Systems
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
"""
It logs in to the APIC and will create the tenant.
"""
import acitoolkit.acitoolkit as ACI
from acisampleslib import get_login_info


# Define static values to pass (edit these if you wish to set differently)

DEFAULT_TENANT_NAME = 'tenant_kit'

# Get all the arguments
description = 'It logs in to the APIC and will create the tenant.'
parser = get_login_info(description)
parser.add_argument('-t', '--tenant', help='The name of tenant', default=DEFAULT_TENANT_NAME)

args = parser.parse_args()

# Login to the APIC
#session = ACI.Session(args.url, args.login, args.password)

url = 'https://10.75.44.208:443'
login = 'admin'
password = 'cisco123'

session = ACI.Session(url, login, password)

resp = session.login()
if not resp.ok:
    print '%% Could not login to APIC'

# Create the Tenant, App Profile, and EPG
tenant = ACI.Tenant(args.tenant)

# Push it all to the APIC
resp = session.push_to_apic(tenant.get_url(),
                            tenant.get_json())
if not resp.ok:
    print '%% Error: Could not push configuration to APIC'
    print resp.text
