Easily generate a simple project gallery on github pages from a list of other github repositories.

Live Demo: https://cscanlin.github.io/

Inspired by: https://github.com/lthr/github-gallery

## Using this Repository

### Setup

*For all of the following commands, replace `USERNAME` with your own username*

First create a new repository called `USERNAME.github.io`

#### Clone, Rename and Install Requirements

    git clone https://github.com/cscanlin/pages_project_gallery
    mv pages_project_gallery USERNAME.github.io
    cd USERNAME.github.io
    pip install -r requirements.txt

#### Installing geckodriver

Download geckodriver from here: https://github.com/mozilla/geckodriver/releases. Then unzip it and move the extracted executable to `~/.local/bin`. Here are some sample commands, but this can easily be done from the finder as well:

    tar -zxf ~/Downloads/geckodriver-v0.14.0-macos.tar.gz
    mv geckodriver ~/.local/bin/geckodriver

Finally, make sure `~/.local/bin` is in your path:

    echo "export PATH=\"~/.local/bin:\$PATH\"" >> ~/.bash_profile

#### Update Configuration

1. In `_config.yml`, change `title` to match the new name of your new repository/directory

2. Change the repositories in `repositories.yml` to your own selections. `screenshot_target` is optional for each.

### Generating Screenshots & Repo Data (Requires Python 3 and geckodriver)

    python generate_screenshots.py

This script uses selenium's python bindings and the Firefox geckodriver to grab screenshots from the website listed on each repository (unless otherwise specified). Also grabs all publicly available repo data about each repository, which is stored in `_data/repo_data.yml` and is accessible in your jekyll layout as an array with `site.data.repo_data`

### Deployment

First make sure the remote matches your repo:

    git remote set-url origin https://github.com/USERNAME/USERNAME.github.io.git

Then simply push to your master branch on github:

    git push origin master

#### Running Your Pages Site Locally (Requires Ruby)

https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/
