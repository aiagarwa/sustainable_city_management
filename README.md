
# Sustainable City Management
# Overview
This is an interesting project that we assigned to complete as a part of course module Advance Software Engineering. The aim of this project was to develop a dashboard based website covering all major functionalites of a city manager in his dialy routine work. So that, the city manager can collect, analyze and make decision based on the data displayed on the dashboard developed. 
# Pre-requisite Steps:
Clone the Gitlab repository:
```
git clone https://gitlab.scss.tcd.ie/fleschb/sustainable-city-management.git
```
The project has been tested with Python >= 3.6.
Requires Node minimum version of 14.15.4 (LTS).
## Quick start
Quick start local:
- From the project folder, navigate to folder sustainableCityManagement.
- run `pip install -r requirements.txt`
- run `python manage.py runserver --noreload` [To run the backend server]
- From the project folder, navigate to folder frontend-pwa.
- run `yarn install`
- run `yarn start` [To run the frontend development server]
or you can access the online version here:
[Online Version](https://ase.bfles.ch/)
# Sustainable City Management - Front End
![Dashboard Video](./frontend-pwa/src/assets/github/Media1.mp4)
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
* [Documentation Front_End](#documentation-frontend)
* [File Structure Front_End](#file-structure-frontend)
* [Browser Support](#browser-support)
* [Useful Links Front_End](#useful-links-frontend)
## Versions
|Application Version | 
| --- |
| [<img src="./frontend-pwa/SCM_logo.png" width="60" height="60" />] Version :1.0 |
| HTML Used Version | React Used Version |
| --- | --- |
| [![Paper Dashboard 2 HTML](https://s3.amazonaws.com/creativetim_bucket/products/86/thumb/opt_pd2_thumbnail.jpg)](https://www.creative-tim.com/product/paper-dashboard-2) | [![Paper Dashboard React](https://s3.amazonaws.com/creativetim_bucket/products/98/thumb/opt_pd_react_thumbnail.jpg)](https://www.creative-tim.com/product/paper-dashboard-react) |
## Demo
| Dashboard | Bikes | Buses  | Parkings | Emergency Services | Footfalls |
| --- | --- | --- | --- | --- | --- |
| [![Dashboard page](./frontend-pwa/src/assets/github/pic1.PNG)]() | [![Bikes page](./frontend-pwa/src/assets/github/pic2.PNG)]() | [![Buses page ](./frontend-pwa/src/assets/github/pic3.PNG)]() | [![Parkings Page](./frontend-pwa/src/assets/github/pic4.PNG)]() | [![Emergency Services page](./frontend-pwa/src/assets/github/pic5.PNG)]() |  [![Footfalls Page](./frontend-pwa/src/assets/github/pic6.PNG)]() |
[View More(Live Demo)](https://)
## Documentation Frontend
The documentation for the project is available at Google Drive [Link](https://drive.google.com/drive/folders/1I2l6W3_I7wzpv2OcQOL-1KvZzZpxgOUw?usp=sharing).
## File Structure Frontend
Within the repository, you'll find the following directories and files under frontend-pwa folder:
```
📦frontend-pwa
 ┣ 📂docs
 ┃ ┗ 📜documentation.html
 ┣ 📂public
 ┃ ┣ 📜favicon.ico
 ┃ ┣ 📜index.html
 ┃ ┣ 📜manifest.json
 ┃ ┗ 📜robots.txt
 ┣ 📂src
 ┃ ┣ 📂assets
 ┃ ┃ ┣ 📂css
 ┃ ┃ ┃ ┣ 📜paper-dashboard.css
 ┃ ┃ ┃ ┣ 📜paper-dashboard.css.map
 ┃ ┃ ┃ ┗ 📜paper-dashboard.min.css
 ┃ ┃ ┣ 📂demo
 ┃ ┃ ┃ ┗ 📜demo.css
 ┃ ┃ ┣ 📂fonts
 ┃ ┃ ┃ ┣ 📜nucleo-icons.eot
 ┃ ┃ ┃ ┣ 📜nucleo-icons.ttf
 ┃ ┃ ┃ ┣ 📜nucleo-icons.woff
 ┃ ┃ ┃ ┗ 📜nucleo-icons.woff2
 ┃ ┃ ┣ 📂github
 ┃ ┃ ┃ ┣ 📜Media1.mp4
 ┃ ┃ ┃ ┣ 📜paper-dashboard-react.gif
 ┃ ┃ ┃ ┣ 📜pic1.PNG
 ┃ ┃ ┃ ┣ 📜pic2.PNG
 ┃ ┃ ┃ ┣ 📜pic3.PNG
 ┃ ┃ ┃ ┣ 📜pic4.PNG
 ┃ ┃ ┃ ┣ 📜pic5.PNG
 ┃ ┃ ┃ ┗ 📜pic6.PNG
 ┃ ┃ ┣ 📂img
 ┃ ┃ ┃ ┣ 📂faces
 ┃ ┃ ┃ ┃ ┣ 📜ayo-ogunseinde-1.jpg
 ┃ ┃ ┃ ┃ ┣ 📜ayo-ogunseinde-2.jpg
 ┃ ┃ ┃ ┃ ┣ 📜clem-onojeghuo-1.jpg
 ┃ ┃ ┃ ┃ ┣ 📜clem-onojeghuo-2.jpg
 ┃ ┃ ┃ ┃ ┣ 📜clem-onojeghuo-3.jpg
 ┃ ┃ ┃ ┃ ┣ 📜clem-onojeghuo-4.jpg
 ┃ ┃ ┃ ┃ ┣ 📜erik-lucatero-1.jpg
 ┃ ┃ ┃ ┃ ┣ 📜erik-lucatero-2.jpg
 ┃ ┃ ┃ ┃ ┣ 📜joe-gardner-1.jpg
 ┃ ┃ ┃ ┃ ┣ 📜joe-gardner-2.jpg
 ┃ ┃ ┃ ┃ ┣ 📜kaci-baum-1.jpg
 ┃ ┃ ┃ ┃ ┗ 📜kaci-baum-2.jpg
 ┃ ┃ ┃ ┣ 📜apple-icon.png
 ┃ ┃ ┃ ┣ 📜bg5.jpg
 ┃ ┃ ┃ ┣ 📜damir-bosnjak.jpg
 ┃ ┃ ┃ ┣ 📜default-avatar.png
 ┃ ┃ ┃ ┣ 📜favicon.png
 ┃ ┃ ┃ ┣ 📜header.jpg
 ┃ ┃ ┃ ┣ 📜jan-sendereks.jpg
 ┃ ┃ ┃ ┣ 📜logo-small.png
 ┃ ┃ ┃ ┗ 📜mike.jpg
 ┃ ┃ ┗ 📂scss
 ┃ ┃ ┃ ┣ 📂paper-dashboard
 ┃ ┃ ┃ ┃ ┣ 📂cards
 ┃ ┃ ┃ ┃ ┃ ┣ 📜_card-chart.scss
 ┃ ┃ ┃ ┃ ┃ ┣ 📜_card-map.scss
 ┃ ┃ ┃ ┃ ┃ ┣ 📜_card-plain.scss
 ┃ ┃ ┃ ┃ ┃ ┣ 📜_card-stats.scss
 ┃ ┃ ┃ ┃ ┃ ┗ 📜_card-user.scss
 ┃ ┃ ┃ ┃ ┣ 📂mixins
 ┃ ┃ ┃ ┃ ┃ ┣ 📜_buttons.scss
 ┃ ┃ ┃ ┃ ┃ ┣ 📜_cards.scss
 ┃ ┃ ┃ ┃ ┃ ┣ 📜_dropdown.scss
 ┃ ┃ ┃ ┃ ┃ ┣ 📜_inputs.scss
 ┃ ┃ ┃ ┃ ┃ ┣ 📜_page-header.scss
 ┃ ┃ ┃ ┃ ┃ ┣ 📜_transparency.scss
 ┃ ┃ ┃ ┃ ┃ ┗ 📜_vendor-prefixes.scss
 ┃ ┃ ┃ ┃ ┣ 📂plugins
 ┃ ┃ ┃ ┃ ┃ ┣ 📜_plugin-animate-bootstrap-notify.scss
 ┃ ┃ ┃ ┃ ┃ ┗ 📜_plugin-perfect-scrollbar.scss
 ┃ ┃ ┃ ┃ ┣ 📂react
 ┃ ┃ ┃ ┃ ┃ ┣ 📂custom
 ┃ ┃ ┃ ┃ ┃ ┃ ┣ 📜_alerts.scss
 ┃ ┃ ┃ ┃ ┃ ┃ ┣ 📜_buttons.scss
 ┃ ┃ ┃ ┃ ┃ ┃ ┣ 📜_checkboxes-radio.scss
 ┃ ┃ ┃ ┃ ┃ ┃ ┣ 📜_dropdown.scss
 ┃ ┃ ┃ ┃ ┃ ┃ ┣ 📜_fixed-plugin.scss
 ┃ ┃ ┃ ┃ ┃ ┃ ┣ 📜_inputs.scss
 ┃ ┃ ┃ ┃ ┃ ┃ ┣ 📜_navbar.scss
 ┃ ┃ ┃ ┃ ┃ ┃ ┣ 📜_nucleo-outline.scss
 ┃ ┃ ┃ ┃ ┃ ┃ ┣ 📜_responsive.scss
 ┃ ┃ ┃ ┃ ┃ ┃ ┗ 📜_typography.scss
 ┃ ┃ ┃ ┃ ┃ ┗ 📜react-differences.scss
 ┃ ┃ ┃ ┃ ┣ 📜_alerts.scss
 ┃ ┃ ┃ ┃ ┣ 📜_animated-buttons.scss
 ┃ ┃ ┃ ┃ ┣ 📜_buttons.scss
 ┃ ┃ ┃ ┃ ┣ 📜_cards.scss
 ┃ ┃ ┃ ┃ ┣ 📜_checkboxes-radio.scss
 ┃ ┃ ┃ ┃ ┣ 📜_dropdown.scss
 ┃ ┃ ┃ ┃ ┣ 📜_fixed-plugin.scss
 ┃ ┃ ┃ ┃ ┣ 📜_footers.scss
 ┃ ┃ ┃ ┃ ┣ 📜_images.scss
 ┃ ┃ ┃ ┃ ┣ 📜_inputs.scss
 ┃ ┃ ┃ ┃ ┣ 📜_misc.scss
 ┃ ┃ ┃ ┃ ┣ 📜_mixins.scss
 ┃ ┃ ┃ ┃ ┣ 📜_navbar.scss
 ┃ ┃ ┃ ┃ ┣ 📜_nucleo-outline.scss
 ┃ ┃ ┃ ┃ ┣ 📜_page-header.scss
 ┃ ┃ ┃ ┃ ┣ 📜_responsive.scss
 ┃ ┃ ┃ ┃ ┣ 📜_sidebar-and-main-panel.scss
 ┃ ┃ ┃ ┃ ┣ 📜_tables.scss
 ┃ ┃ ┃ ┃ ┣ 📜_typography.scss
 ┃ ┃ ┃ ┃ ┗ 📜_variables.scss
 ┃ ┃ ┃ ┗ 📜paper-dashboard.scss
 ┃ ┣ 📂components
 ┃ ┃ ┣ 📂FixedPlugin
 ┃ ┃ ┃ ┗ 📜FixedPlugin.js
 ┃ ┃ ┣ 📂Footer
 ┃ ┃ ┃ ┗ 📜Footer.js
 ┃ ┃ ┣ 📂Login
 ┃ ┃ ┃ ┣ 📜LoginButton.css
 ┃ ┃ ┃ ┣ 📜LoginButton.js
 ┃ ┃ ┃ ┣ 📜LogoutButton.css
 ┃ ┃ ┃ ┣ 📜LogoutButton.js
 ┃ ┃ ┃ ┣ 📜Profile.css
 ┃ ┃ ┃ ┗ 📜Profile.js
 ┃ ┃ ┣ 📂Navbars
 ┃ ┃ ┃ ┗ 📜DemoNavbar.js
 ┃ ┃ ┗ 📂Sidebar
 ┃ ┃ ┃ ┗ 📜Sidebar.js
 ┃ ┣ 📂layouts
 ┃ ┃ ┗ 📜Admin.js
 ┃ ┣ 📂variables
 ┃ ┃ ┣ 📜charts.js
 ┃ ┃ ┣ 📜general.js
 ┃ ┃ ┗ 📜icons.js
 ┃ ┣ 📂views
 ┃ ┃ ┣ 📜Bikes.js
 ┃ ┃ ┣ 📜Bikes.test.js
 ┃ ┃ ┣ 📜Buses.js
 ┃ ┃ ┣ 📜Dashboard.js
 ┃ ┃ ┣ 📜EmergencyServices.js
 ┃ ┃ ┣ 📜Footfall.js
 ┃ ┃ ┣ 📜Icons.js
 ┃ ┃ ┣ 📜Login.js
 ┃ ┃ ┣ 📜Map.js
 ┃ ┃ ┣ 📜Notifications.js
 ┃ ┃ ┣ 📜Parkings.js
 ┃ ┃ ┣ 📜Tables.js
 ┃ ┃ ┗ 📜User.js
 ┃ ┣ 📜index.css
 ┃ ┣ 📜index.js
 ┃ ┣ 📜logo-white.svg
 ┃ ┣ 📜logo.svg
 ┃ ┣ 📜reportWebVitals.js
 ┃ ┣ 📜routes.js
 ┃ ┣ 📜service-worker.js
 ┃ ┣ 📜serviceWorkerRegistration.js
 ┃ ┗ 📜setupTests.js
 ┣ 📜.env
 ┣ 📜.env.production
 ┣ 📜.gitignore
 ┣ 📜Dockerfile
 ┣ 📜LICENSE.md
 ┣ 📜README.md
 ┣ 📜SCM_logo.png
 ┣ 📜TCD.jpg
 ┣ 📜gulpfile.js
 ┣ 📜jsconfig.json
 ┣ 📜package 2.json
 ┣ 📜package-lock.json
 ┣ 📜package.json
 ┣ 📜trinity-logo.jpg
 ┗ 📜yarn.lock
```
## Browser Support
At present, we officially aim to support the last two versions of the following browsers:
<img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/chrome.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/firefox.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/edge.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/safari.png" width="64" height="64">
## Useful Links [Frontend]
Tutorials: <https://reactjs.org/>
# [Sustainable City Management - Back End]
- For backend we made use of Django environmental framework and for Database 'MongoDB"
- Install MongoDb for your respective OS version from product website [Link](https://docs.mongodb.com/manual/installation/).
- Now navigate to folder sustainableCityManagement by
 - cd sustainableCityManagement
- run 'pip install -r requirements.txt' to download all the required dependencies for backend'
## Table of Contents
* [Storage](#storage)
* [RESTful API Links and its usage](#restful-api-links-and-its-usage)
* [Documentation Backend](#documentation-backend)
* [File Structure Backend](#file-structure-backend)
* [Test](#test)
* [Run Server](#run-server)
* [Useful Links Backend](#useful-links-backend)
## Storage
- To store the data one time on to the database server:
 - run  python manage.py runserver --noreload
 - Next we need to provided input 'Yes' for all storage related queries asked in the server.
 - This will create an instance on Mongo DB cluster under url: 127.0.01:27017
  
## RESTful API Links and its usage
- For Bike data:
 - Frontend URL: (http://localhost:3000/admin/bikes)
 - This will trigger four Get API function call at the backend:
 - Use  http://127.0.0.1:8000/main/bikestands_details/?type=historical&days_historic=5 for 5 day historical data.
 - Use  http://127.0.0.1:8000/main/bikestands_details/?type=locations for locations data.
 - Use http://127.0.0.1:8000/main/bikestands_graph/?location_based=no&days_historic=5 for getting the graph values (overall).
 - Use http://127.0.0.1:8000/main/bikestands_graph/?location_based=yes&days_historic=5 for getting the graph values (location based).
- For  Bus data:
 - Frontend URL: (http://localhost:3000/admin/buses)
 - This will trigger four Get API function call to the backend and third party service provider:
 - `https://api.openrouteservice.org/v2/directions/driving-hgv?api_key=${apiKey}&start=${start_destination&end=end_destination} for getting all possible bus routes.
 - http://127.0.0.1:8000/main/busstop_locations/ for getting all longitude and latitude locations for each bust stops
 - http://127.0.0.1:8000/main/busstop_timings/ for getting timings of each bus in a particular route.
 -  http://127.0.0.1:8000/main/bustrip_paths/ for getting paths for each bus trip from source to destination.
- For  Bashboard data:
 - Frontend URL: (http://localhost:3000/admin/dashboard)
 - This will trigger four Get API function call to the backend and third party service provider:
 - https://api.openweathermap.org/data/2.5/air_pollution?lat=53.3498&lon=-6.2603&appid=d50542e129f589c12a362e67f91906fe for getting air ppollution data for dublin city.
 - https://api.openweathermap.org/data/2.5/weather?q=Dublin&units=metric&appid=d50542e129f589c12a362e67f91906fe for getting weather data.
 - http://127.0.0.1:8000/mainweather_forecast/ for getting weather forecast for upcoming ten days. 
 -  http://127.0.0.1:8000/main/ireland_population/ for getting change in ireland population.
- For  Emergency data:
 - Frontend URL: (http://localhost:3000/admin/emergency)
 - This will trigger four Get API function call to the backend
 - Use  http://127.0.0.1:8000/main/health_centers/ for collecting health center location data.
 - Use  http://127.0.0.1:8000/main/garda_stations/ for collecting garda station information and location data.
 - Use  http://127.0.0.1:8000/main/hospital_centers/ for collecting hospital center information and location data.
 - Use  http://127.0.0.1:8000/main/fire_stations/ for collecting fire station basic information and location data.
- For  Parkings data:
 - Frontend URL: (http://localhost:3000/admin/parking)
 - This will trigger four Get API function call to the backend
 - Use  http://127.0.0.1:8000/main/parkings_availability/ for collecting available parking spaces within dublin city.
 - Use  http://127.0.0.1:8000/main/parks_parkings/ for collecting available parking spaces near parks.
 - Use  http://127.0.0.1:8000/main/beaches_parkings/ for collecting available parking spaces neae beaches.
 - Use  http://127.0.0.1:8000/main/playing_pitches_parkings/ for collecting available parking space near playing pitches.
- For  Parkings data:
 - Frontend URL: (http://localhost:3000/admin/footfalls)
 - This will trigger four Get API function call to the backend
 - Use  http://127.0.0.1:8000/main/footfall_overall/ for collecting live footfalls around major streets in dublin.
 - Use  http://127.0.0.1:8000footfall_datebased/?days_interval=6&location="name" for collecting predicted footfall for next six days.
## Documentation Backend
- The documentation for the project is available at Google Drive [Link](https://drive.google.com/drive/folders/1I2l6W3_I7wzpv2OcQOL-1KvZzZpxgOUw?usp=sharing).
## File Structure Backend
Within the repository, you'll find the following directories and files under sustainableCityManagement folder:
```
📦sustainableCityManagement 
 ┣ 📂config 
 ┃ ┣ 📜dev.env 
 ┃ ┗ 📜prod.env 
 ┣ 📂main_project 
 ┃ ┣ 📂Bike_API 
 ┃ ┃ ┣ 📂views_bike_api 
 ┃ ┃ ┃ ┣ 📜graph_bike_data.py 
 ┃ ┃ ┃ ┗ 📜show_bike_data.py 
 ┃ ┃ ┣ 📜bike_collections_db.py 
 ┃ ┃ ┣ 📜fetch_bikeapi.py 
 ┃ ┃ ┣ 📜graphvalues_bike.py 
 ┃ ┃ ┣ 📜store_bikedata_to_database.py 
 ┃ ┃ ┗ 📜store_processed_bikedata_to_db.py 
 ┃ ┣ 📂Bus_API 
 ┃ ┃ ┣ 📂resources 
 ┃ ┃ ┃ ┣ 📜routes.csv 
 ┃ ┃ ┃ ┣ 📜stop_times.csv 
 ┃ ┃ ┃ ┣ 📜stop_times_test.csv 
 ┃ ┃ ┃ ┣ 📜stops.csv 
 ┃ ┃ ┃ ┣ 📜trips.csv 
 ┃ ┃ ┃ ┣ 📜trips_paths.json 
 ┃ ┃ ┃ ┗ 📜trips_test.csv 
 ┃ ┃ ┣ 📂views_bus_api 
 ┃ ┃ ┃ ┣ 📜show_bus_delays.py 
 ┃ ┃ ┃ ┣ 📜show_bus_info.py 
 ┃ ┃ ┃ ┣ 📜show_bus_paths.py 
 ┃ ┃ ┃ ┗ 📜show_bus_stops.py 
 ┃ ┃ ┣ 📜bus_collections_db.py 
 ┃ ┃ ┣ 📜fetch_busapi.py 
 ┃ ┃ ┣ 📜process_bus_delays.py 
 ┃ ┃ ┗ 📜store_bus_routes_data_in_database.py 
 ┃ ┣ 📂Config 
 ┃ ┃ ┣ 📜config.yaml 
 ┃ ┃ ┗ 📜config_handler.py 
 ┃ ┣ 📂Emergency_Service_API 
 ┃ ┃ ┣ 📂resources 
 ┃ ┃ ┃ ┣ 📜fcc_fire_stations_dublin.csv 
 ┃ ┃ ┃ ┣ 📜fcc_health_centers_dublin.csv 
 ┃ ┃ ┃ ┣ 📜garda_stations_dublin.csv 
 ┃ ┃ ┃ ┗ 📜list_of_hospitals_in_ireland.csv 
 ┃ ┃ ┣ 📂views_emergency_service_api 
 ┃ ┃ ┃ ┗ 📜show_emergency_service_data.py 
 ┃ ┃ ┣ 📜fetch_emergency_service.py 
 ┃ ┃ ┗ 📜store_emergency_service_data_in_database.py 
 ┃ ┣ 📂Footfall_API 
 ┃ ┃ ┣ 📂resources 
 ┃ ┃ ┃ ┣ 📜footfall_locations.json 
 ┃ ┃ ┃ ┗ 📜pedestrian_footfall.csv 
 ┃ ┃ ┣ 📂views_footfall_api 
 ┃ ┃ ┃ ┗ 📜show_footfall_data.py 
 ┃ ┃ ┣ 📜fetch_footfallapi.py 
 ┃ ┃ ┣ 📜footfall_collections_db.py 
 ┃ ┃ ┗ 📜store_footfall_data_in_database.py 
 ┃ ┣ 📂Logs 
 ┃ ┃ ┗ 📜service_logs.py 
 ┃ ┣ 📂ML_models 
 ┃ ┃ ┣ 📜bikes_usage_prediction.py 
 ┃ ┃ ┗ 📜footfall_prediction.py 
 ┃ ┣ 📂Parkings_API 
 ┃ ┃ ┣ 📂views_parkings_api 
 ┃ ┃ ┃ ┣ 📜show_parkings_availability.py 
 ┃ ┃ ┃ ┗ 📜show_parkings_locations.py 
 ┃ ┃ ┣ 📜fetch_parkingsapi.py 
 ┃ ┃ ┣ 📜parkings_collections_db.py 
 ┃ ┃ ┗ 📜store_parkingsdata_to_database.py 
 ┃ ┣ 📂Parkings_Recreational_Places_API 
 ┃ ┃ ┣ 📂resources 
 ┃ ┃ ┃ ┣ 📜Beaches.csv 
 ┃ ┃ ┃ ┣ 📜Cinemas.csv 
 ┃ ┃ ┃ ┣ 📜Parks.csv 
 ┃ ┃ ┃ ┣ 📜PlayingPitches.csv 
 ┃ ┃ ┃ ┗ 📜disabledparkings.csv 
 ┃ ┃ ┣ 📂views_rec_places_api 
 ┃ ┃ ┃ ┗ 📜show_rec_places_parkings.py 
 ┃ ┃ ┣ 📜recreational_places_parkings_collections_db.py 
 ┃ ┃ ┗ 📜store_recreational_locations_in_db.py 
 ┃ ┣ 📂Population_API 
 ┃ ┃ ┣ 📂resources 
 ┃ ┃ ┃ ┣ 📜dublin_population.csv 
 ┃ ┃ ┃ ┗ 📜ireland_population.csv 
 ┃ ┃ ┣ 📜store_population.py 
 ┃ ┃ ┗ 📜views_population.py 
 ┃ ┣ 📂Weather_API 
 ┃ ┃ ┣ 📂views_weather_api 
 ┃ ┃ ┃ ┗ 📜show_weather.py 
 ┃ ┃ ┗ 📜weather_call.py 
 ┃ ┣ 📂migrations 
 ┃ ┃ ┗ 📜__init__.py 
 ┃ ┣ 📜.gitignore 
 ┃ ┣ 📜__init__.py 
 ┃ ┣ 📜admin.py 
 ┃ ┣ 📜apps.py 
 ┃ ┗ 📜urls.py 
 ┣ 📂sustainableCityManagement 
 ┃ ┣ 📜.gitignore 
 ┃ ┣ 📜__init__.py 
 ┃ ┣ 📜settings.py 
 ┃ ┣ 📜urls.py 
 ┃ ┗ 📜wsgi.py 
 ┣ 📂tests 
 ┃ ┣ 📂Bike_API 
 ┃ ┃ ┣ 📂views_bike_api 
 ┃ ┃ ┃ ┣ 📜test_graph_bike_data.py 
 ┃ ┃ ┃ ┗ 📜test_show_bike_data.py 
 ┃ ┃ ┣ 📜test_fetch_bikeapi.py 
 ┃ ┃ ┣ 📜test_graphvalues_bike.py 
 ┃ ┃ ┣ 📜test_store_bikedata_to_database.py 
 ┃ ┃ ┗ 📜test_store_processed_bikedata_to_db.py 
 ┃ ┣ 📂Bus_API 
 ┃ ┃ ┣ 📂views_bus_api 
 ┃ ┃ ┃ ┣ 📜test_show_bus_data.py 
 ┃ ┃ ┃ ┗ 📜test_show_bus_delays.py 
 ┃ ┃ ┣ 📜test_fetch_busapi.py 
 ┃ ┃ ┣ 📜test_process_bus_delays.py 
 ┃ ┃ ┗ 📜test_store_bus_routes_in_db.py 
 ┃ ┣ 📂Emergency_Service_API 
 ┃ ┃ ┣ 📂views_emergency_service_api 
 ┃ ┃ ┃ ┗ 📜test_show_emergency_service_data.py 
 ┃ ┃ ┣ 📜test_fetch_emergency_service.py 
 ┃ ┃ ┗ 📜test_store_emergency_service_data_in_database.py 
 ┃ ┣ 📂Footfall_API 
 ┃ ┃ ┣ 📂views_footfall_api 
 ┃ ┃ ┃ ┗ 📜test_show_footfall_data.py 
 ┃ ┃ ┣ 📜test_fetch_footfallapi.py 
 ┃ ┃ ┗ 📜test_store_footfall_data_in_database.py 
 ┃ ┣ 📂ML_Models 
 ┃ ┃ ┣ 📜test_bikes_uasge_prediction.py 
 ┃ ┃ ┗ 📜test_footfall_prediction.py 
 ┃ ┣ 📂Parkings_API 
 ┃ ┃ ┣ 📂views_parkings_api 
 ┃ ┃ ┃ ┣ 📜test_show_parkings_availability.py 
 ┃ ┃ ┃ ┗ 📜test_show_parkings_locations.py 
 ┃ ┃ ┣ 📜test_fetch_parkingsapi.py 
 ┃ ┃ ┗ 📜test_store_parkingsdata_to_database.py 
 ┃ ┣ 📂Parkings_Recreational_Places_API 
 ┃ ┃ ┗ 📜test_store_recreational_locations_in_db.py 
 ┃ ┣ 📂Population_API 
 ┃ ┃ ┣ 📜test_store_population.py 
 ┃ ┃ ┗ 📜test_views_population.py 
 ┃ ┗ 📜__init__.py 
 ┣ 📜Dockerfile 
 ┣ 📜Pipfile 
 ┣ 📜Pipfile.lock 
 ┣ 📜db.sqlite3 
 ┣ 📜manage.py 
 ┣ 📜requirements.txt 
 ┗ 📜runserver_init.py
```
## Test
- To test the code and its functionality
 - run `python manage.py tests test`
 - It will run all the test cases created and output the results.
## Run Server
- cd sustainableCityManagement
- run  python manage.py runserver --noreload
## Useful Links Backend
Tutorials: <https://docs.djangoproject.com/en/3.2/>
