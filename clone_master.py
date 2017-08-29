import json
import sys
import os
import jenkins
import xml.etree.ElementTree


def clone_job(server, old_name, new_name, new_branch):
  try:
    existing_job = server.get_job_config(new_name)
    server.build_job(existing_job)
    print("%s already exists")
    return
  except:
    pass

  print("creating new job %s" % new_name)
  my_job = server.get_job_config(old_name)
  et = xml.etree.ElementTree.fromstring(my_job)
  et.find('scm').find('branches').find('hudson.plugins.git.BranchSpec').find('name').text = new_branch
  reconfigure_xml = xml.etree.ElementTree.tostring(et)
  server.create_job(new_name, reconfigure_xml)
  server.enable_job(new_name)
  server.build_job(new_name)


def main(settings):
  server = jenkins.Jenkins(settings['server'], username=settings['username'], password=settings['password'])
  git_local_branch = os.environ['GIT_BRANCH'].split('/')[-1]
  clone_job(server,
            settings['master_job'],
            "%s_%s" % (settings['new_prefix'], git_local_branch),
            os.environ['GIT_BRANCH'])


if __name__ == "__main__":
  settings = json.loads(open(sys.argv[1]).read())
  main(settings)
