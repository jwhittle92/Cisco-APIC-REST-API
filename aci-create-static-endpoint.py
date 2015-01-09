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
Simple application to statically connect an EPG to a specific interface using
a specific VLAN.  It then assigns a static Endpoint to that EPG on the
specified interface.

It logs in to the APIC and will create the tenant, application profile,
and EPG if they do not exist already.  It then connects it to the specified
interface using the VLAN encapsulation specified.  The static endpoint will
use this encapsulation.

Before running, please make sure that the credentials.py
file has the URL, LOGIN, and PASSWORD set for your APIC environment.
"""
import acitoolkit.acitoolkit as ACI
import credentials

# Define static values to pass (edit these if you wish to set differently)
TENANT_NAME = 'cisco'
APP_NAME = 'fancyapp'
EPG_NAME = 'redis'
INTERFACE = {'type': 'eth',
             'pod': '1', 'node': '101', 'module': '1', 'port': '35'}
VLAN = {'name': 'vlan5',
        'encap_type': 'vlan',
        'encap_id': '5'}

# Login to the APIC
# session = ACI.Session(credentials.URL, credentials.LOGIN, credentials.PASSWORD)

url = 'https://10.75.44.208:443'
login = 'admin'
password = 'cisco123'

session = ACI.Session(url, login, password)

resp = session.login()
if not resp.ok:
    print '%% Could not login to APIC'

# Create the Tenant, App Profile, and EPG
tenant = ACI.Tenant(TENANT_NAME)
app = ACI.AppProfile(APP_NAME, tenant)
epg = ACI.EPG(EPG_NAME, app)

# Create the physical interface object
intf = ACI.Interface(INTERFACE['type'],
                     INTERFACE['pod'],
                     INTERFACE['node'],
                     INTERFACE['module'],
                     INTERFACE['port'])

# Create a VLAN interface and attach to the physical interface
vlan_intf = ACI.L2Interface(VLAN['name'], VLAN['encap_type'], VLAN['encap_id'])
vlan_intf.attach(intf)

# Attach the EPG to the VLAN interface
epg.attach(vlan_intf)

# Create the Endpoint
mac = '00:50:56:11:22:33'
ip = '10.10.5.5'
ep = ACI.Endpoint(name=mac,
                  parent=epg)
ep.mac = mac
ep.ip = ip

# Assign it to the L2Interface
ep.attach(vlan_intf)

print 'JSON to be pushed:', tenant.get_json()

# Push it all to the APIC
resp = session.push_to_apic(tenant.get_url(),
                            tenant.get_json())
if not resp.ok:
    print '%% Error: Could not push configuration to APIC'
    print resp.text
