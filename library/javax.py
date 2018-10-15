#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2014, Timothy Appnel <tim@appnel.com>
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = \
    '''
---
module: javax
short_description: A module for executing an arbitrary java class or jar in a cleaner, more Ansible-like way.
description:
    - It is very easy and relatively straight-forward to run a basic Java applications in Ansible using the command or shell modules. Things get complicated and messy pretty quickly when your application needs various options like max heap size or thread stack and has extensive number of class paths and systems properties all being defined on the command line. The javax module helps bring some sanity and readability back to these situations by giving you human-readable argument names and native data structure values to running a Java application from your playbook.
options:
    jar:
        required: false
        description:
        - The JAR file that contains the Java class you want to run. Required if the 
          C(javaclass) option is omitted.
    javaclass:
        required: false
        description:
        - The main Java class to run. Required if the C(jar) option is omitted.
    properties:
        required: false
        description:
        - A dict of key value pairs representing system properties to pass the java 
          application being run. This is the equivalent of the C(-D) commandline 
          option. 
    classpath:
        required: false
        description:
        - A list of file system paths the JVM should search to find any 
          dependencies. The module will take the list and properly concatenate the
          list of values. The equivalent of the C(-classpath) or C(-cp) commandline 
          option.
    init_heap_size:
        required: false
        description:
        - Sets initial Java heap size for the application. Equivalent of the C(-Xms) 
          'non-stndard' commandline option.  
    max_heap_size:
        required: false
        description:
        - Sets maximum Java heap size for the application. Equivalent of the C(-Xmx) 
          'non-stndard' commandline option.  
    thread_stack:
        required: false
        description:
        - Sets java thread stack size for the application. Equivalent of the C(-Xss) 
          'non-stndard' commandline option.  
    executable:
        required: false
        default: java
        description:
        - Path to java JVM to use. If not supplied,
          the normal mechanism for resolving binary paths will be used.    
    java_opts:
        required: false
        description:
        - Specify additional java options not supported by this module by passing 
          in a list of strings.
    java_args:
        required: false
        description:
        - Specify a list of strings to be passed as parameters to the java application.
author: Timothy Appnel
'''

EXAMPLES = '''
javax: javaclass='MyMainClass' init_heap_size=1024m max_heap_size=2048m
args:
  properties:
    Name: Foo
    Hello: World
  classpath:
    - /path/to/some.jar
  java_opts:
    - '-XX:MaxPermSize=512m'
    - '-XX:+HeapDumpOnOutOfMemoryError'
'''

# verbose if debugging on?
# Xprof if debugging on?
# support if module.check_mode:
# http://docs.oracle.com/javase/7/docs/technotes/tools/windows/java.html
# -Xms1024m -Xmx2048m -XX:MaxPermSize=512m -XX:+HeapDumpOnOutOfMemoryError

def main():
    module = AnsibleModule(argument_spec=dict(
        init_heap_size=dict(default=None),
        max_heap_size=dict(default=None),
        thread_stack=dict(default=None),
        classpath=dict(type='list'),
        properties=dict(type='dict'),
        java_opts=dict(type='list'),
        java_args=dict(type='list'),
        executable=dict(default='java'),
        jar=dict(default=None),
        javaclass=dict(default=None),
        ), supports_check_mode=False)

    init_heap_size = module.params['init_heap_size'] # + Xms alias
    max_heap_size = module.params['max_heap_size'] # + Xmx alias
    thread_stack = module.params['thread_stack'] # + Xms alias
    classpath = module.params['classpath'] # + cp alias
    properties = module.params['properties']
    java_opts = module.params['java_opts']
    java_args = module.params['java_args']
    java = module.params['executable']
    jar = module.params['jar']
    javaclass = module.params['javaclass'] # + class alias

    if not jar and not javaclass: # jar or class is required, but not both
        return module.fail_json(msg='Must specify a "jar" or "javaclass"',
                                changed=False)
    elif jar and javaclass:
        return module.fail_json(msg='Cannot specify a "jar" and "javaclass"'
                                , changed=False)

    changed = True
    cmd = ''
    if init_heap_size:
        cmd = cmd + ' -Xms%s' % init_heap_size
    if max_heap_size:
        cmd = cmd + ' -Xmx%s' % max_heap_size
    if thread_stack:
        cmd = cmd + ' -Xss%s' % thread_stack
    if classpath:
        cmd = cmd + ' -classpath "' + ';'.join(classpath) + '"'
    if properties:
        for (k, v) in properties.items():
            if ' ' in v:
                v = '"' + v + '"'
            cmd = cmd + ' -D%s=%s' % (k, v)
    if java_opts:
        cmd = cmd + ' ' + ' '.join(java_opts)
    if jar:
        cmd = ' '.join([java, cmd, '-jar %s' % jar])
    else:
        cmd = ' '.join([java, cmd, javaclass])
    if java_args:
        cmd = cmd + ' ' + ' '.join(java_args)

    cmdstr = cmd
    (rc, out, err) = module.run_command(cmd)
    if rc:
        return module.fail_json(msg=err, rc=rc, cmd=cmdstr)
    else:
        return module.exit_json(changed=changed, msg=out, rc=rc,
                                cmd=cmdstr)

# import module snippets

from ansible.module_utils.basic import *

main()

