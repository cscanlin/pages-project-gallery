'use strict'

const Nightmare = require('nightmare')
const yaml = require('js-yaml')
const fs = require('fs')
const url = require('url')
require('isomorphic-fetch')

const INIT_TIME = new Date().toISOString().split('.')[0]

const config = yaml.safeLoad(fs.readFileSync('./_config.yml', 'utf8'))

class Repository {

  constructor(repo_data, screenshot_target) {
    this.screenshot_target = screenshot_target ? screenshot_target : repo_data.homepage
    this.screenshot = null
    Object.keys(repo_data).forEach(key => {
      this[key] = repo_data[key]
    })
  }

  static retrieve_from_url(repo_url, screenshot_target) {
    const full_api_path = `https://api.github.com/repos${url.parse(repo_url).pathname}`
    return new Promise((resolve, reject) => {
      fetch(full_api_path).then(response => {
        return response.json()
      }).then(repo_data => {
        resolve(new Repository(repo_data, screenshot_target))
      }).catch(reject)
    })
  }

  static parse_data_from_url(repo_url, screenshot_target) {
    const repo_data = {
      name: repo_url.split('/').reverse()[0],
      html_url: repo_url,
    }
    repo_data.homepage = `https://cscanlin.github.io/${repo_data.name}`
    return new Repository(repo_data, screenshot_target)
  }

  screenshot_filename() {
    return `${this.name}_${INIT_TIME}.png`
  }
}

class Screenshotter {
  constructor(repositories) {
    this.repositories = repositories
  }

  clear_screenshot_directory() {
    fs.readdir(config.screenshot_directory, (err, file_names) => {
      file_names.forEach(file_name => {
        if (file_name !== '.keep') {
          fs.unlinkSync(config.screenshot_directory + '/' +file_name)
        }
      })
    })
  }

  capture_screenshots() {
    // https://github.com/rosshinkley/nightmare-examples/blob/master/docs/common-pitfalls/async-operations-loops.md
    const nightmare = Nightmare({ show: true })
    nightmare.viewport(config.screenshot_width, config.screenshot_height)
    this.repositories.reduce((accumulator, repo) => {
      return accumulator.then(results => {
        return nightmare.goto(repo.screenshot_target)
          .screenshot(`${config.screenshot_directory}/${repo.screenshot_filename()}`)
          .then(function(result){
            console.log(`Finished: ${repo.name}`)
            results.push(result)
            return results
          })
      })
    }, Promise.resolve([])).then(results => {
        nightmare.end().then(() => {
          console.log('All finished!')
        })
    })
  }

  dump_repo_data() {
    fs.writeFileSync('_data/repo_data.yml', yaml.safeDump(this.repositories), 'utf8')
    console.log('Finsihed Dumping Data')
  }

  run() {
    this.clear_screenshot_directory()
    this.capture_screenshots()
    this.dump_repo_data()
  }

}

Promise.all(config.repositories.map(repo => {
  return Repository.retrieve_from_url(repo.repo_url, repo.screenshot_target)
})).then((repositories) => new Screenshotter(repositories).run())