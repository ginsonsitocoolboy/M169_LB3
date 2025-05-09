import docker
from mcrouter import register_mapping
client = docker.from_env()
IMAGE = "itzg/minecraft-server"
BASE_PORT = 25566
def list_servers():
    containers = client.containers.list(all=True, filters={"ancestor": IMAGE})
    return [{"name": c.name, "status": c.status} for c in containers]
def create_server(name):
    port = BASE_PORT + len(list_servers())
    try:
        client.containers.run(
            IMAGE,
            name=name,
            environment={
                "EULA": "TRUE",
                "MOTD": f"{name}'s Minecraft Server",
                "DIFFICULTY": "normal",
                "ALLOW_NETHER": "true",
                "MODE": "0",
                "MAX_PLAYERS": "20"
            },
            ports={"25565/tcp": port},
            volumes={f"./{name}-data": {'bind': '/data', 'mode': 'rw'}},
            tty=True,
            stdin_open=True,
            detach=True,
            restart_policy={"Name": "unless-stopped"}
        )
        register_mapping(f"{name}.lowtaperfade.org", name)
        return {"status": "created", "name": name, "port": port}
    except Exception as e:
        return {"error": str(e)}
def start_server(name):
    try:
        container = client.containers.get(name)
        container.start()
        return {"status": "started", "name": name}
    except Exception as e:
        return {"error": str(e)}
def stop_server(name):
    try:
        container = client.containers.get(name)
        container.stop()
        return {"status": "stopped", "name": name}
    except Exception as e:
        return {"error": str(e)}
def delete_server(name):
    try:
        container = client.containers.get(name)
        container.remove(force=True)
        return {"status": "deleted", "name": name}
    except Exception as e:
        return {"error": str(e)}
