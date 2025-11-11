# Minecraft Backup
A Minecraft backup script using RCON and thinning backups.

---

To get started, copy config.yaml.sample into config.yaml if you want to use a template.

```
cp config.yaml.sample config.yaml
```

To run, use uv.

```
uv run minecraft-backup.py
```


## Config File Parameters

| Parameter | Type | Explanation |
| --- | --- | --- |
| `minecraft_location` 			| String 		| Location of your Minecraft server directory |
| `backup_location` 			| String 		| Location where backups will be copied to |
| `backup_folders` 				| String Array	| Folders (and probably files) in `minecraft_location` to back up |
| `silent` 						| Boolean		| If backup messages should be broadcast to the server |
| `rcon_ip` 					| String		| IP of Minecraft's RCON instance, should be `localhost` by default |
| `rcon_port` 					| Integer		| Port of Minecraft's RCON instance, should be `25575` by default |
| `rcon_password` 				| String		| Password of Minecraft's RCON instance, set in server.properties |
| `retention` 					| Dict			| Used to set how many backups for each thinning period to retain.  To not backup a period set to `0`.  All keys *must* be present. |
