import getpass, os
from crontab import CronTab

def cron():
  #update crontab
  my_cron = CronTab(user=getpass.getuser())
  needs_cron_flag = True
  cron_cmd = 'bash '+os.getcwd()+'/cron.sh >> '+os.getcwd()+'/cron.log 2>&1'
  for job in my_cron:
    if job.comment == 'vanComputer':
      needs_cron_flag = False
      print('cron already exists')
      job.set_command(cron_cmd)
  if needs_cron_flag:
    print('creating new cron')
    job = my_cron.new(command=cron_cmd, comment='vanComputer')
  job.hour.every(1)
  job.minute.on(0)
  my_cron.write()

  response = ''
  for job in my_cron:
    response += str(job)
  print(response)
  return response
