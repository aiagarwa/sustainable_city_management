# [Sustainable City Management](https://demos.creative-tim.com/paper-dashboard-react/#/dashboard) 

# Important notes
- Requires Node minimum version of 14.15.4 (LTS)
- Launch React:
    - `$> yarn install`
    - `$> yarn start`

![Dashboard Video](./src/assets/github/Media1.mp4)

The above inserted video gives a glimpse of our user interface dashboard developed for the completeion of Sustainable City Management Project. We made use of Paper Dashboard React which is a Bootstrap Admin Panel which combines soft colours with beautiful typography and spacious cards and graphics.

**Bootstrap 4 Support** Paper Dashboard React is built on top of the much awaited Bootstrap 4 and uses the most used react framework that implements the Bootstrap 4 components on react, reactstrap.  This made the layout responsive, so that it can adapt to all variations of screen resolution. 

**Example Pages** Our built dashboard main page consist of child pages corresponding to every functionality that we covered.
These functionality include,
1. Bike usage: This page provide informations regarding current bike usage at various bike stands in Dublin city. In addition, it provides recommendation and predictions for bike usage in upcoming days.
2. Bus info: This page provides bus timing and route informations on google maps.
3. Parkings: This page provides parking information like available spaces on google maps.
4. Emergency Services: This page provides the location and contact information of various public services like, Health Care, Garda, Fire Services and Hospitals on google maps.
5. Footfalls: This page provides live information of footfalls recorded over major crossing in the city of Dublin.    
6. Dashboard: This gives information like temperature forecast, humidity forecast and population corelation data. 

## Table of Contents

* [Versions](#versions)
* [Demo](#demo)
* [Quick Start](#quick-start)
* [Documentation](#documentation)
* [File Structure](#file-structure)
* [Browser Support](#browser-support)
* [Resources](#resources)
* [Reporting Issues](#reporting-issues)
* [Technical Support or Questions](#technical-support-or-questions)
* [Licensing](#licensing)
* [Useful Links](#useful-links)


## Versions

|Application Version | 
[<img src="./SCM_logo.png" width="60" height="60" />]Version :1.0[Final]

| HTML Used Version | React Used Version |
| --- | --- |
| [![Paper Dashboard 2 HTML](https://s3.amazonaws.com/creativetim_bucket/products/86/thumb/opt_pd2_thumbnail.jpg)](https://www.creative-tim.com/product/paper-dashboard-2) | [![Paper Dashboard React](https://s3.amazonaws.com/creativetim_bucket/products/98/thumb/opt_pd_react_thumbnail.jpg)](https://www.creative-tim.com/product/paper-dashboard-react) |

## Demo

| Dashboard | Bikes | Buses  | Parkings | Emergency Services | Footfalls |
| --- | --- | --- | --- | --- |
| [![Dashboard page](./src/assets/github/pic1.PNG)] | [![Bikes page](./src/assets/github/pic2.png)] | [![Buses page ](./src/assets/github/pic3.png)] | [![Parkings Page](./src/assets/github/pic4.png)] | [![Emergency Services page](./src/assets/github/pic5.png)] |  [![Footfalls Page](./src/assets/github/pic6.png)]

[View More(Live Demo)](https://)


## Quick start

Quick start options:

- `npm i paper-dashboard-react`
- Clone the repo: `git clone git@gitlab.scss.tcd.ie:fleschb/sustainable-city-management.git`.
- [Download from Github](https://gitlab.scss.tcd.ie/fleschb/sustainable-city-management/-/tree/dev/).
- Navigate to folder frontend-pwa.
- run yarn/npm install
- run yarn/npm start [To run the frontend server]


## Documentation
The documentation for the project is available at Google Drive [Link](https://drive.google.com/drive/folders/1I2l6W3_I7wzpv2OcQOL-1KvZzZpxgOUw?usp=sharing).


## File Structure

Within the download you'll find the following directories and files with frontend-pwa folder:

```
├── CHANGELOG.md
├── ISSUE_TEMPLATE.md
├── LICENSE.md
├── README.md
├── jsconfig.json
├── package.json
├── docs
│   └── documentation.html
├── public
│   ├── favicon.ico
│   ├── index.html
│   └── manifest.json
 |     |___ robot.txt
└── src
    ├── index.js
    ├── logo-white.svg
    ├── logo.svg
    ├── routes.js
     |___ service-worker.js
     |___ serviceWorkerRegistration.js
     |___ setupTests.js
    ├── components
    │   ├── FixedPlugin
    │   │   └── FixedPlugin.jsx
    │   ├── Footer
    │   │   └── Footer.jsx
    │   ├── Navbars
    │   │   └── DemoNavbar.jsx
    │   └── Sidebar
    │       └── Sidebar.jsx
    ├── layouts
    │   └── Admin.jsx
    ├── variables
    │   ├── charts.jsx
    │   ├── general.jsx
    │   └── icons.jsx
    ├── views
    │   ├── Dashboard.jsx
    │   ├── Bikes.jsx
    │   ├── Bikes.test.jsx
    │   ├── Buses.jsx
    │   ├── EmergencyServices.jsx
    │   ├── Footfalls.jsx
    │   ├── Icons.jsx
    │   └── Login.jsx
     |     |___ Map.jsx
     |     |___ Notifications.js
     |     |___ Parkings.js
     |     |___ Tables.js
     |     |___ User.js
    └── assets
        ├── css
        │   ├── paper-dashboard.css
        │   ├── paper-dashboard.css.map
        │   └── paper-dashboard.min.css
        ├── demo
        ├── fonts
        ├── github
        ├── img
        │   └── faces
        └── scss
            ├── paper-dashboard
            │   ├── cards
            │   ├── mixins
            │   ├── plugins
            │   └── react
            │       ├── custom
            │       └── react-differences.scss
            └── paper-dashboard.scss
```

## Browser Support

At present, we officially aim to support the last two versions of the following browsers:

<img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/chrome.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/firefox.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/edge.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/safari.png" width="64" height="64"> <img src="https://s3.

## Useful Links

Tutorials: <https://reactjs.org/>

