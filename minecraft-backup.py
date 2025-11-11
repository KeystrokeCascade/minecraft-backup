from yaml import safe_load
import os
from datetime import datetime
from mcipc.rcon.je import Client
from zipfile import ZipFile

def backup_period_exists(backups, period):
	backup = next((s[0:13] for s in backups if period in s), None)
	if not backup:
		return False

	time = datetime.strptime(backup, '%Y-%m-%d_%H')
	if period == 'yearly' and time.year == datetime.now().year:
		return True
	if period == 'monthly' and time.month == datetime.now().month:
		return True
	if period == 'weekly' and time.isocalendar().week == datetime.now().isocalendar().week:
		return True
	if period == 'daily' and time.day == datetime.now().day:
		return True
	if period == 'hourly' and time.hour == datetime.now().hour:
		return True
	return False

def main():
	with open('config.yaml', 'r', encoding='utf-8') as f:
		config = safe_load(f)

	# Determine type of backup
	os.makedirs(config['backup_location'], exist_ok=True)
	backups = os.listdir(config['backup_location'])
	backups.sort(reverse=True)

	backup_name = datetime.now().strftime("%Y-%m-%d_%H")
	for period in config['retention'].keys():
		if not backup_period_exists(backups, period) and config['retention'][period] > 0:
			backup_name += f'_{period}'
			break

	# Backup
	with Client(config['rcon_ip'], config['rcon_port'], passwd=config['rcon_password']) as client:
		if not config['silent']: client.say('Starting backup...')
		if not config['silent']: client.say('Saving chunks')

		client.save_off()
		client.save_all(True)

		if not config['silent']: client.say('Chunks saved')
		if not config['silent']: client.say('Copying files...')

		with ZipFile(os.path.join(config['backup_location'], f'{backup_name}.zip'), 'w') as zip:
			for f in config['backup_folders']:
				for root, dirs, files in os.walk(os.path.join(config['minecraft_location'], f)):
					for file in files:
						zip.write(os.path.join(root, file),
							os.path.relpath(os.path.join(root, file), config['minecraft_location']))

		client.save_on()

		if not config['silent']: client.say('Files copied')
		if not config['silent']: client.say('Backup complete!')

	print(f'Backed up {backup_name}.zip')

	# Delete older copies
	backups = os.listdir(config['backup_location'])
	backups.sort(reverse=True)

	delete_backups = []
	for period in config['retention'].keys():
		period_backups = [s for s in backups if period in s]
		if len(period_backups) > config['retention'][period]:
			delete_backups += period_backups[config['retention'][period]:]

	for backup in delete_backups:
		os.remove(os.path.join(config['backup_location'], backup)
		print(f'Deleted {backup}')

if __name__ == '__main__':
	main()
