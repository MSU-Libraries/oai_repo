"""
Config file for OAI repository
"""
import json

class OAIConfig:
    """
    """
    def __init__(self, filepath: str = None):
        self.filepath: str = filepath
        self.name: str = 'Example OAI-PMH Repository'
        self.baseurl: str = 'http://oai.example.edu'
        self.admin_email: str = 'admin@oai.example.edu'
        self.metadata_formats: dict = {}
        if self.filepath:
            self.load_file(self.filepath)

    def load_file(self, filepath):
        """
        """
        self.filepath = filepath
        try:
            with open(self.filepath, 'r', encoding='utf8') as fileh:
                config = json.load(fileh)
            self.name = config.get('name', self.name)
            self.baseurl = config.get('baseurl', self.baseurl)
            self.admin_email = config.get('admin-email', self.admin_email)
            self.metadata_formats = config.get('metadata-formats', self.metadata_formats)
        except FileNotFoundError as exc:
            #TODO
            raise exc
        except json.JSONDecodeError as exc:
            #TODO
            raise exc
