<p align="center"><img src="https://github.com/gavin-bauer/spacex-dashboard/blob/master/img/header.png"></p>


<p align="center">
  <img src="https://github.com/gavin-bauer/spacex-dashboard/blob/master/img/demo.gif?raw=1" hspace="4">
</p>

<p align="center">
  <img alt="GitHub" src="https://img.shields.io/github/license/gavin-bauer/spacex-dashboard">
</p>

---

**Explore SpaceX Missions** is a web app that lets users engage with SpaceX’s past missions data interactively, through sections ranging from _launches, payloads to landings._

Part of the author's portfolio, Explore SpaceX Missions is an end-to-end Data Science & Analytics project -- from retrieving the data & web scraping, ETL, data analysis & visualization to deploying a web app.

<br/>

## The project

#### Retrieving the data & web scrapping
- The data was retrieved from [r/SpaceX](https://github.com/r-spacex/SpaceX-API)’s API, using the requests python library.
- Additional data regarding rockets was scrapped from [Wikipedia](https://www.wikipedia.org/), also using requests.

#### Data analysis & visualization
- ETL required custom functions, as extracting the rows proved laborious due to the data being deeply nested in .json and .html files. 
- Data analysis and visualization was performed using Python's [Numpy](https://numpy.org/), [Pandas](https://pandas.pydata.org/) and [Matplotlib](https://matplotlib.org/) libraries.

#### Presenting the findings

The findings were presented as a web app in the form of a [streamlit](https://www.streamlit.io/) and hosted on [Heroku](https://dashboard.heroku.com/login).

<br/>

## Installation

#### Downloading & editing the web app

1. Clone the repository with the 'clone' command, or just download the zip.

```
$ git clone git@github.com:https://github.com/gavin-bauer/spacex-dashboard.git
```

2. Install the requirements

3. Download or Open your IDE (i.e. [Atom](https://atom.io/)) and start editing the file app.py.

#### Running the app locally

*cd* to the spacex-dashboard repo and run the following command.

```
$ streamlit run app.py
```

#### Deployment

1. Sign up for a [Heroku](https://dashboard.heroku.com/login) account.
2. Create a new Web App on Heroku and grant Heroku permission to access the GitHub repository containing the project.
3. On the deployment screen, pick a name for the web app.
4. Choose the *Manual deploy*. Select the branch to deploy and deploy. The web app will begin building and should be live in a few minutes at the URL displayed in the Heroku dashboard, under the *Settings* tab.

<br/>

## Built with

* [Python](https://www.python.org/) - Programming language
* [Numpy](https://numpy.org/), [Pandas](https://pandas.pydata.org/) & [Matplotlib](https://matplotlib.org/) - Data centric Python packages
* [Streamlit](https://www.streamlit.io/) - Create data apps quickly and simply
* [Atom](https://atom.io/) - Text editor
* [Heroku](https://render.com/) - Cloud platform to host web apps

## Author

* **Gavin Bauer** - Data Analyst of 5+ years experience | Current: 🦉[@KeringGroup](https://www.kering.com/) | Past: ⚡[@Total](https://www.total.com/en), 🌱[@YvesRocherFR](https://groupe-rocher.com/en)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgements
* [SpaceX](https://www.spacex.com/) for providing the media
* [r/SpaceX](https://github.com/r-spacex/SpaceX-API) & [Wikipedia](https://www.wikipedia.org/) for providing the datasets
* [Streamlit](https://www.streamlit.io/) for providing a simple library to create dashboards
