import os
import logging
import requests
import yaml
from datetime import datetime
from selenium import webdriver
from urllib.parse import urlparse
import argparse

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

with open(os.path.join(THIS_DIR, '_config.yml')) as f:
    CONFIG = yaml.load(f)

class Repository(object):
    REPO_API_PATH = 'https://api.github.com/repos'

    def __init__(self, repo_data, screenshot_target=None):
        for k, v in repo_data.items():
            setattr(self, k, v)
        if not repo_data['homepage'] and not screenshot_target:
            raise ValueError('Need screenshot_target or homepage for {}'.format(repo_data['name']))
        self.screenshot_target = screenshot_target if screenshot_target else self.homepage
        self.homepage = self.homepage if self.homepage else screenshot_target
        self.screenshot = None

    @classmethod
    def retrieve_from_url(cls, repo_url, screenshot_target=None):
        api_path = '{0}{1}'.format(Repository.REPO_API_PATH, urlparse(repo_url).path)
        req = requests.get(api_path)
        if req.status_code == 200:
            return cls(req.json(), screenshot_target)
        else:
            logging.error(req.json()['message'])
            raise ConnectionError(req.json()['message'])

    @classmethod
    def _parse_data_from_url(cls, repo_url, screenshot_target=None):
        repo_data = {
            'name': repo_url.rstrip('/').split('/')[-1],
            'html_url': repo_url,
        }
        repo_data['homepage'] = 'https://cscanlin.github.io/{}'.format(repo_data['name'])
        return cls(repo_data, screenshot_target)

    def __str__(self):
        return self.name

class Screenshotter(object):
    def __init__(self,
                 repositories,
                 width=CONFIG['screenshot_width'],
                 height=CONFIG['screenshot_height'],
                 screenshot_directory=CONFIG['screenshot_directory'],
                 data_dump_directory='_data',
                 driver_type=webdriver.Firefox):
        self.repositories = repositories
        self.width = width
        self.height = height
        self.screenshot_directory = screenshot_directory
        self.data_dump_directory = data_dump_directory
        self.driver = None
        self.driver_type = driver_type
        self.init_time = datetime.utcnow().replace(microsecond=0).isoformat()

    def __enter__(self):
        self.driver = self.driver_type()
        self.driver.set_window_size(self.width, self.height)
        return self

    def __exit__(self, *args):
        self.driver.quit()

    @classmethod
    def from_config(cls, conf=CONFIG, **kwargs):
        repositories = [Repository.retrieve_from_url(**item) for item in conf['repositories']]
        return cls(repositories, **kwargs)

    def clear_screenshot_directory(self):
        for f in os.listdir(self.screenshot_directory):
            if not f.endswith('.keep'):
                os.remove(os.path.join(self.screenshot_directory, f))

    def capture_screenshot(self, repository):
        self.driver.get(repository.screenshot_target)
        logging.info('finished: {}'.format(repository.name))
        filename = self.screenshot_filename(repository)
        self.driver.save_screenshot(
            os.path.join(self.screenshot_directory, filename)
        )
        return filename

    def screenshot_filename(self, repository):
        return '{}_{}.png'.format(repository.name, self.init_time)

    def run(self):
        self.clear_screenshot_directory()
        for repo in self.repositories:
            repo.screenshot = self.capture_screenshot(repo)
        logging.info('All finished!')

    def dump_repo_data(self):
        formatted_data = [repo.__dict__ for repo in self.repositories]
        export_path = os.path.join(self.data_dump_directory, 'repo_data.yml')
        with open(export_path, 'w') as ef:
            yaml.dump(formatted_data, ef, default_flow_style=False)
        logging.info('Finished Dumping')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--phantomjs', dest='phantomjs', action='store_true')
    driver_type = webdriver.PhantomJS if parser.parse_args().phantomjs else webdriver.Firefox
    with Screenshotter.from_config(driver_type=driver_type) as ss:
        ss.run()
        ss.dump_repo_data()
