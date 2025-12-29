from factory import Factory

factory = Factory()
client = factory.create_crowdin_client()

projs = client.projects.list_projects()