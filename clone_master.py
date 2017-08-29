import json
import sys
import os
import jenkins
import xml.etree.ElementTree


def clone_job(server, old_name, new_name, new_branch):
  try:
    existing_job = server.get_job_config(new_name)
    server.build_job(new_name)
    return
  except:
    pass

  my_job = server.get_job_config(old_name)
  server.copy_job(old_name, new_name)
  et = xml.etree.ElementTree.fromstring(my_job)
  et.find('scm').find('branches').find('hudson.plugins.git.BranchSpec').find('name').text = new_branch
  reconfigure_xml = xml.etree.ElementTree.tostring(et)
  server.reconfig_job(new_name, reconfigure_xml)
  server.enable_job(new_name)
  server.build_job(new_name)


def main(settings):
  server = jenkins.Jenkins(settings['server'], username=settings['username'], password=settings['password'])
  clone_job(server,
            settings['master_job'],
            "%s_%s" % (settings['new_prefix'], os.environ['GIT_LOCAL_BRANCH']),
            os.environ['GIT_BRANCH'])


if __name__ == "__main__":
  settings = json.loads(open(sys.argv[1]).read())