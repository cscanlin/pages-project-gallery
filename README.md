Easily generate a simple project gallery on github pages from a list of other github repositories.

Live Demo: https://cscanlin.github.io/

Based on: https://github.com/lthr/github-gallery

## Using this Repository

### Setup

First create a new repo called `USERNAME.github.io`

#### Clone and Install Requirements

  git clone https://github.com/cscanlin/pages_project_gallery
  mv pages_project_gallery USERNAME.github.io
  cd USERNAME.github.io
  pip install -r requirements.txt

#### Installing geckodriver

Download geckodriver from here: https://github.com/mozilla/geckodriver/releases
Then unzip, move it to `~/.local/bin` and make sure it's in your path:

  tar -zxf ~/Downloads/geckodriver-v0.14.0-macos.tar.gz
  mv geckodriver ~/.local/bin/geckodriver
  echo "export PATH=\"~/.local/bin:\$PATH\"" >> ~/.bash_profile

### Generating Screenshots & Repo Data (Requires Python 3 and geckodriver)

  python generate_screenshots.py

### Deployment

First make sure the remote matches your repo:

  git remote set-url origin https://github.com/USERNAME/USERNAME.github.io.git

Then simply push to your master branch on github:

  git push origin master

Simply push right to the master branch

In `_config.yml`, change `title` to match the new name of your directory

Change the repositories in `repositories.yml` to ones of your choice. `screenshot_target` is optional for each.


#### To Run Your Pages Site Locally (Requires Ruby)

https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/
