Easily generate a simple project gallery on github pages from a list of other github repositories.

Live Demo: https://cscanlin.github.io/

Inspired by: https://github.com/lthr/github-gallery

## Using this Repository

Requires either Node and Nightmare.js OR Python 3 and a suitable selenium webdriver. Installation instructions for both are below, but currently Node is recommended.

Building and running the page locally requires Ruby and Jekyll.

Instructions below assume OS X and tested on Sierra, but should work on most setups.

### Setup

*For all of the following commands, replace `USERNAME` with your own github username*

First create a new repository called `USERNAME.github.io`

#### Clone, Rename and Install Requirements

    git clone https://github.com/cscanlin/pages_project_gallery
    mv pages_project_gallery USERNAME.github.io
    cd USERNAME.github.io
    npm install

#### Update Configuration

In `_config.yml`:

1. Change `title` to match the new name of your new repository/directory

2. Change `repositories` to your own selections. `screenshot_target` is optional for each.

### Generating Screenshots & Repo Data

    node site_builder_node.js

This script uses Nightmare.js to capture screenshots from the project website listed on each repository (unless otherwise specified), and stores them in `assets/images/screenshots`. It also grabs all publicly available repo data about each repository, which is stored in `_data/repo_data.yml` and is accessible in your jekyll templates as an array under `site.data.repo_data`.

### Deployment

First make sure the remote matches your repo:

    git remote set-url origin https://github.com/USERNAME/USERNAME.github.io.git

Then simply push to your master branch on github:

    git push origin master

### Running Your Pages Site Locally (Requires Ruby 2.1.0+)

Make sure bundler is installed, then install Jekyll and other dependencies from the GitHub Pages gem:

    gem install bundler
    bundle install

Then the following command will build and run your site locally at http://127.0.0.1:4000/:

    bundle exec jekyll serve

See more: https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/

### Shortcuts

The following npm scripts have been added for convenience:

    "scripts": {
      "run": "bundle exec jekyll serve",
      "build": "node site_builder_node.js",
      "deploy": "git push origin master"
    }

### Python instructions

#### Installing Python requirements

    pip install -r requirements.txt

##### Installing geckodriver

Download geckodriver from here: https://github.com/mozilla/geckodriver/releases. Then unzip it and move the extracted executable to `~/.local/bin`. Here are some sample commands, but this can easily be done from the finder as well:

    tar -zxf ~/Downloads/geckodriver-v0.14.0-macos.tar.gz
    mv geckodriver ~/.local/bin/geckodriver

Finally, make sure `~/.local/bin` is in your path:

    echo "export PATH=\"~/.local/bin:\$PATH\"" >> ~/.bash_profile

##### Installing PhantomJS

Alternatively, you can download PhantomJS and use the included ghostdriver instead. It's on npm which makes the install easier, but it currently lacks support for many es6 features which can make the screenshots render incorrectly (this should be significantly better in PhantomJS 2.5 which is currently in Beta as of 2016-03-07).

    sudo npm install -g phantomjs-prebuilt

#### Generating Screenshots & Repo Data with Python

    python site_builder_python.py

This script uses selenium's python bindings and the Firefox geckodriver (or PhantomJS ghostdriver) instead of Nightmare.js. If you want to run with the python binding to PhantomJS, this can easily be done with the `--phantomjs` command line flag.
