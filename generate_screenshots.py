import os
import logging
import requests
import yaml
from datetime import datetime
from selenium import webdriver
from urllib.parse import urlparse
import __main__

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

default_logger = logging.getLogger(__main__.__file__)

def get_log_handler():
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    return handler

class Repository(object):
    REPO_API_PATH = 'https://api.github.com/repos'

    def __init__(self, repo_data, screenshot_target=None):
        self.screenshot_target = screenshot_target if screenshot_target else repo_data['homepage']
        self.screenshot = None
        for k, v in repo_data.items():
            setattr(self, k, v)

    @classmethod
    def retrieve_from_url(cls, repo_url, screenshot_target=None):
        api_path = '{0}{1}'.format(Repository.REPO_API_PATH, urlparse(repo_url).path)
        repo_data = requests.get(api_path).json()
        return cls(repo_data, screenshot_target)

    @staticmethod
    def parse_data_from_url(repo_url):
        repo_data = {
            'name': repo_url.split('/')[-1],
            'html_url': repo_url,
        }
        repo_data['homepage'] = 'https://cscanlin.github.io/{}'.format(repo_data['name'])
        return repo_data

class Screenshotter(object):
    def __init__(self,
                 repositories,
                 width=1280,
                 height=800,
                 screenshot_directory=None,
                 screenshot_format='png',
                 data_dump_directory='_data',
                 logger=default_logger):
        self.repositories = repositories
        self.width = width
        self.height = height
        if screenshot_directory:
            self.screenshot_directory = screenshot_directory
        else:
            self.screenshot_directory = self.get_screenshot_dir_from_config()
        self.screenshot_format = screenshot_format
        self.data_dump_directory = data_dump_directory
        self.logger = logger
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(get_log_handler())
        self.driver = None
        self.init_time = datetime.utcnow().replace(microsecond=0).isoformat()

    def __enter__(self):
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(self.width, self.height)
        return self

    def __exit__(self, *args):
        self.driver.quit()

    @classmethod
    def from_file(cls, filename='repositories.yml'):
        with open(filename) as f:
            return cls([Repository.retrieve_from_url(**item) for item in yaml.load(f)])

    @staticmethod
    def get_screenshot_dir_from_config():
        with open('_config.yml') as f:
            return os.path.join(THIS_DIR, yaml.load(f)['screenshot_directory'][1:])

    def clear_screenshot_directory(self):
        for f in os.listdir(self.screenshot_directory):
            if not f.endswith('.keep'):
                os.remove(os.path.join(self.screenshot_directory, f))

    def capture_screenshot(self, repository):
        self.driver.get(repository.screenshot_target)
        self.logger.info('finished: {}'.format(repository.name))
        filename = self.screenshot_filename(repository)
        self.driver.save_screenshot(
            os.path.join(self.screenshot_directory, filename)
        )
        return filename

    def screenshot_filename(self, repository):
        return '{}_{}.{}'.format(
            repository.name,
            self.init_time,
            self.screenshot_format,
        )

    def run(self):
        self.clear_screenshot_directory()
        for repo in self.repositories:
            repo.screenshot = self.capture_screenshot(repo)
        self.logger.info('All finished!')

    def dump_repo_data(self):
        formatted_data = [repo.__dict__ for repo in self.repositories]
        export_path = os.path.join(self.data_dump_directory, 'repo_data.yml')
        with open(export_path, 'w') as ef:
            yaml.dump(formatted_data, ef, default_flow_style=False)
        self.logger.info('Finsihed Dumping')

if __name__ == '__main__':
    with Screenshotter.from_file('repositories.yml') as ss:
        ss.run()
        ss.dump_repo_data()

# Alternatively:
# repositories = [
#     Repository.retrieve_from_url(
#         repo_url='https://github.com/cscanlin/munger-builder',
#         screenshot_target='http://www.mungerbuilder.com/script_builder/pivot_builder/1',
#     )
#     Repository.retrieve_from_url('https://github.com/cscanlin/choice-optimizer')
#     Repository.retrieve_from_url('https://github.com/cscanlin/minesweeper')
#     Repository.retrieve_from_url('https://github.com/cscanlin/periodic-table-timeline')
# ]
# with Screenshotter(repositories) as ss:
#     ss.run()
#     ss.dump_repo_data()
