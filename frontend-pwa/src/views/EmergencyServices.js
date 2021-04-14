/*!

=========================================================
* Paper Dashboard React - v1.2.0
=========================================================

* Product Page: https://www.creative-tim.com/product/paper-dashboard-react
* Copyright 2020 Creative Tim (https://www.creative-tim.com)

* Licensed under MIT (https://github.com/creativetimofficial/paper-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React from "react";
import axios from "axios";
// react plugin used to create google maps
import Chart from "react-apexcharts";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
// reactstrap components
import {
  Card,
  CardTitle,
  CardFooter,
  CardHeader,
  CardBody,
  Row,
  Col,
  FormGroup,
  Label,
  Input,
  Table,
} from "reactstrap";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const iconDefault = L.divIcon({
  className: "custom-pin",
  iconAnchor: [0, 24],
  labelAnchor: [-6, 0],
  popupAnchor: [0, -36],
  html: `<i class="fa fa-map-marker-alt fa-3x" style="color:blue;"></i>`,
});

L.Marker.prototype.options.icon = iconDefault;

class EmergencyServices extends React.Component {
  catch(e) {
    console.log(e);
  }

  async componentDidMount() {
    axios
      .get("/main/health_centers/")
      .then(async (res) => {
        let results = res.data.DATA.RESULT;
        console.log(results);

        const markers_health = [];

        // const gardaStations = res.data.DATA.RESULT;
        const healthCentersLocations = res.data.DATA.RESULT;

        for (const locations of Object.keys(healthCentersLocations)) {
          const healthCentersName =
            healthCentersLocations[locations].CENTER_NAME;
          const healthCenters_LAT =
            healthCentersLocations[locations].CENTER_LAT;
          const healthCenters_LONG =
            healthCentersLocations[locations].CENTER_LONG;
          const healthCenters_ADDRESS =
            healthCentersLocations[locations].CENTER_ADDRESS;
          const healthCenters_PHONE =
            healthCentersLocations[locations].CENTER_PHONE;

          markers_health.push({
            position: [healthCenters_LAT, healthCenters_LONG],
            HealthCenterName: healthCentersName,
            HealthCenterAddress: healthCenters_ADDRESS,
            HealthCenterPhone: healthCenters_PHONE,

            icon: {
              className: "custom-pin",
              iconAnchor: [0, 24],
              labelAnchor: [-6, 0],
              popupAnchor: [0, -36],
              html: `<i class="fas fa-clinic-medical fa-2x" style="color:purple;"></i>`,
            },
          });
        }

        localStorage.setItem("emergency_services_health", JSON.stringify(markers_health));
        this.setState({ markers_health: markers_health });
      })
      .catch((err) => {
        console.log(err);
        if (localStorage.getItem("emergency_services_health") != null) {
          const markers_health = JSON.parse(localStorage.getItem("emergency_services_health"));
          this.setState({ markers_health: markers_health });
        }
      });

    axios
      .get("/main/garda_stations/")
      .then(async (res) => {
        let results = res.data.DATA.RESULT;
        console.log(results);
        const markers_garda = [];

        const gardaStations = res.data.DATA.RESULT;

        for (const locations of Object.keys(gardaStations)) {
          const gardaStationsName = gardaStations[locations].STATION_NAME;

          const gardaStations_LAT = gardaStations[locations].STATION_LAT;
          const gardaStations_LONG = gardaStations[locations].STATION_LON;

          const gardaStations_ADDRESS =
            gardaStations[locations].STATION_ADDRESS;
          const gardaStations_PHONE = gardaStations[locations].STATION_PHONE;

          // Add markers
          markers_garda.push({
            position: [gardaStations_LAT, gardaStations_LONG],
            GardaStationsName: gardaStationsName,
            GardaStationsAddress: gardaStations_ADDRESS,
            GardaStationsPhone: gardaStations_PHONE,

            icon: {
              className: "custom-pin",
              iconAnchor: [0, 24],
              labelAnchor: [-6, 0],
              popupAnchor: [0, -36],
              html: `<i class="fas fa-star fa-2x" style="color:#ffe100;"></i>`,
            },
          });
        }

        localStorage.setItem("emergency_services_garda", JSON.stringify(markers_garda));
        this.setState({ markers_garda: markers_garda });
      })
      .catch((err) => {
        console.log(err);
        if (localStorage.getItem("emergency_services_garda") != null) {
          const markers_garda = JSON.parse(localStorage.getItem("emergency_services_garda"));
          this.setState({ markers_garda: markers_garda });
        }
      });

    axios
      .get("/main/hospital_centers/")
      .then(async (res) => {
        let results = res.data.DATA.RESULT;
        console.log(results);

        const markers_hospital = [];
        const hospitalCenters = res.data.DATA.RESULT;

        for (const locations of Object.keys(hospitalCenters)) {
          const hospitalCentersName = hospitalCenters[locations].CENTER_NAME;

          const hospitalCenters_LAT = hospitalCenters[locations].CENTER_LAT;
          const hospitalCenters_LONG = hospitalCenters[locations].CENTER_LONG;

          const hospitalCenters_ADDRESS =
            hospitalCenters[locations].CENTER_ADDRESS;

          // console.log(gardaStations);
          // console.log(locations);
          // console.log(hospitalCentersName);
          // console.log(hospitalCenters_LAT);
          // console.log(hospitalCenters_LONG);
          // console.log(hospitalCenters_ADDRESS);

          // Add markers

          markers_hospital.push({
            position: [hospitalCenters_LAT, hospitalCenters_LONG],
            hospitalCentersName: hospitalCentersName,
            hospitalCentersAddress: hospitalCenters_ADDRESS,

            icon: {
              className: "custom-pin",
              iconAnchor: [0, 24],
              labelAnchor: [-6, 0],
              popupAnchor: [0, -36],
              html: `<i class="far fa-hospital fa-2x" style="color:green;"></i>`,
            },
          });
        }

        localStorage.setItem("emergency_services_hospitals", JSON.stringify(markers_hospital));
        this.setState({ markers_hospital: markers_hospital });
      })
      .catch((err) => {
        console.log(err);
        if (localStorage.getItem("emergency_services_hospitals") != null) {
          const markers_hospital = JSON.parse(localStorage.getItem("emergency_services_hospitals"));
          this.setState({ markers_hospital: markers_hospital });
        }
      });

    axios.get("/main/fire_stations/").then(async (res) => {
      let results = res.data.DATA.RESULT;
      console.log(results);

      const markers_fireStations = [];
      const fireStations = res.data.DATA.RESULT;

      for (const locations of Object.keys(fireStations)) {
        const fireStationsName = fireStations[locations].STATION_NAME;

        const fireStations_LAT = fireStations[locations].STATION_LAT;
        const fireStations_LONG = fireStations[locations].STATION_LON;

        const fireStations_ADDRESS = fireStations[locations].STATION_ADDRESS;
        const fireStations_PHONE = fireStations[locations].STATION_PHONE;

        // console.log(gardaStations);
        // console.log(locations);
        // console.log(hospitalCentersName);
        // console.log(hospitalCenters_LAT);
        // console.log(hospitalCenters_LONG);
        // console.log(hospitalCenters_ADDRESS);

        // Add markers

        markers_fireStations.push({
          position: [fireStations_LAT, fireStations_LONG],
          fireStationsName: fireStationsName,
          fireStationsAddress: fireStations_ADDRESS,
          fireStationsPhone: fireStations_PHONE,

          icon: {
            className: "custom-pin",
            iconAnchor: [0, 24],
            labelAnchor: [-6, 0],
            popupAnchor: [0, -36],
            html: `<i class="fas fa-fire-extinguisher fa-2x" style="color:red;"></i>`,
          },
        });
      }

      localStorage.setItem("emergency_services_fire", JSON.stringify(markers_fireStations));
      this.setState({ markers_fireStations: markers_fireStations });
    })
    .catch((err) => {
      console.log(err);
      if (localStorage.getItem("emergency_services_fire") != null) {
        const markers_fireStations = JSON.parse(localStorage.getItem("emergency_services_fire"));
        this.setState({ markers_fireStations: markers_fireStations });
      }
    });
  }

  constructor(props) {
    super(props);

    this.state = {
      markers_health: [],
      markers_hospital: [],
      markers_garda: [],
      markers_fireStations: [],
    };
  }

  render() {
    return (
      <>
        <div className="content">
          <Row>
            <Col>
              <Card>
                <CardHeader>
                  <CardTitle tag="h5">Emergency Services in Dublin</CardTitle>
                </CardHeader>
                <CardBody>
                  <div className="leaflet-container">
                    <MapContainer
                      style={{ width: "100%", height: "600px" }}
                      center={[53.345, -6.26]}
                      zoom={11}
                      scrollWheelZoom={false}
                    >
                      <TileLayer
                        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                      />
                      {this.state.markers_hospital.map(
                        (hospitalCenters, idx) => (
                          <Marker
                            key={`marker-${idx}`}
                            position={hospitalCenters.position}
                            icon={L.divIcon(hospitalCenters.icon)}
                          >
                            <Popup>
                              <p>
                                <b>{"HOSPITALS"}</b>
                              </p>
                              <p>
                                {"Name: " + hospitalCenters.hospitalCentersName}
                              </p>
                              <p>
                                {"Address: " +
                                  hospitalCenters.hospitalCentersAddress}
                              </p>
                            </Popup>
                          </Marker>
                        )
                      )}

                      {/** GARDA */}
                      {this.state.markers_garda.map((gardaStations, idx) => (
                        <Marker
                          key={`marker-${idx}`}
                          position={gardaStations.position}
                          icon={L.divIcon(gardaStations.icon)}
                        >
                          <Popup>
                            <p>
                              <b>{"Public Protection Service"}</b>
                            </p>
                            <p>{"Name: " + gardaStations.GardaStationsName}</p>
                            <p>
                              {"Address: " + gardaStations.GardaStationsAddress}
                            </p>
                            <p>
                              {"Contact: " + gardaStations.GardaStationsPhone}
                            </p>
                          </Popup>
                        </Marker>
                      ))}

                      {/**HOSPITALS */}

                      {this.state.markers_health.map((healthCenter, idx) => (
                        <Marker
                          key={`marker-${idx}`}
                          position={healthCenter.position}
                          icon={L.divIcon(healthCenter.icon)}
                        >
                          <Popup>
                            <p>
                              <b>{"HEALTH CENTERS"}</b>
                            </p>
                            <p>{"Name: " + healthCenter.HealthCenterName}</p>
                            <p>
                              {"Address: " + healthCenter.HealthCenterAddress}
                            </p>
                            <p>
                              {"Contact: " + healthCenter.HealthCenterPhone}
                            </p>
                          </Popup>
                        </Marker>
                      ))}

                      {/** FIRE */}
                      {this.state.markers_fireStations.map(
                        (fireStations, idx) => (
                          <Marker
                            key={`marker-${idx}`}
                            position={fireStations.position}
                            icon={L.divIcon(fireStations.icon)}
                          >
                            <Popup>
                              <p>
                                <b>{"FIRE STATIONS"}</b>
                              </p>
                              <p>{"Name: " + fireStations.fireStationsName}</p>
                              <p>
                                {"Address: " + fireStations.fireStationsAddress}
                              </p>
                              <p>
                                {"Contact: " + fireStations.fireStationsPhone}
                              </p>
                            </Popup>
                          </Marker>
                        )
                      )}
                    </MapContainer>
                  </div>
                </CardBody>
              </Card>
            </Col>
          </Row>
        </div>
      </>
    );
  }
}

export default EmergencyServices;
