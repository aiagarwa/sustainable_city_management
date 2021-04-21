import React from "react";
import axios from "axios";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { Card, CardTitle, CardHeader, CardBody, Row, Col, Table } from "reactstrap";
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
  async componentDidMount() {
    if (localStorage.getItem("emergency_services_health") != null) {
      const markers_health = JSON.parse(
        localStorage.getItem("emergency_services_health")
      );
      this.setState({ markers_health: markers_health });
    }
    if (localStorage.getItem("emergency_services_fire") != null) {
      const markers_fireStations = JSON.parse(
        localStorage.getItem("emergency_services_fire")
      );
      this.setState({ markers_fireStations: markers_fireStations });
    }
    if (localStorage.getItem("emergency_services_garda") != null) {
      const markers_garda = JSON.parse(
        localStorage.getItem("emergency_services_garda")
      );
      this.setState({ markers_garda: markers_garda });
    }
    if (localStorage.getItem("emergency_services_hospitals") != null) {
      const markers_hospital = JSON.parse(
        localStorage.getItem("emergency_services_hospitals")
      );
      this.setState({ markers_hospital: markers_hospital });
    }

    axios
      .get("/main/health_centers/")
      .then(async (res) => {
        let results = res.data.DATA.RESULT;
        console.log(results);

        const markers_health = [];

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

        localStorage.setItem(
          "emergency_services_health",
          JSON.stringify(markers_health)
        );
        this.setState({
          markers_health: markers_health ,
          graphLoading: false
        });
      })
      .catch((err) => {
        console.log(err);
        if (localStorage.getItem("emergency_services_health") != null) {
          const markers_health = JSON.parse(
            localStorage.getItem("emergency_services_health")
          );
          this.setState({ markers_health: markers_health });
          this.setState({ displayMap: "none" });
          this.setState({
            displayList: "block",
            graphLoading: false
          });
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

        localStorage.setItem(
          "emergency_services_garda",
          JSON.stringify(markers_garda)
        );
        this.setState({ markers_garda: markers_garda });
      })
      .catch((err) => {
        console.log(err);
        if (localStorage.getItem("emergency_services_garda") != null) {
          const markers_garda = JSON.parse(
            localStorage.getItem("emergency_services_garda")
          );
          this.setState({ markers_garda: markers_garda });
          this.setState({ displayMap: "none" });
          this.setState({ displayList: "block" });
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

        localStorage.setItem(
          "emergency_services_hospitals",
          JSON.stringify(markers_hospital)
        );
        this.setState({ markers_hospital: markers_hospital });
      })
      .catch((err) => {
        console.log(err);
        if (localStorage.getItem("emergency_services_hospitals") != null) {
          const markers_hospital = JSON.parse(
            localStorage.getItem("emergency_services_hospitals")
          );
          this.setState({ markers_hospital: markers_hospital });
          this.setState({ displayMap: "none" });
          this.setState({ displayList: "block" });
        }
      });

    axios
      .get("/main/fire_stations/")
      .then(async (res) => {
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

        localStorage.setItem(
          "emergency_services_fire",
          JSON.stringify(markers_fireStations)
        );
        this.setState({ markers_fireStations: markers_fireStations });
      })
      .catch((err) => {
        console.log(err);
        if (localStorage.getItem("emergency_services_fire") != null) {
          const markers_fireStations = JSON.parse(
            localStorage.getItem("emergency_services_fire")
          );
          this.setState({ markers_fireStations: markers_fireStations });
          this.setState({ displayMap: "none" });
          this.setState({ displayList: "block" });
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
      displayMap: "block",
      displayList: "none",
      graphLoading: true
    };
  }

  render() {
    return (
      <>
        <div className="content">
          <Row style={{ display: this.state.displayMap }}>
            <Col>
              <Card>
                <CardHeader>
                  <CardTitle tag="h5">
                    Emergency Services in Dublin{" "}
                    <i
                      style={{
                        display: this.state.graphLoading
                          ? "inline-block"
                          : "none",
                      }}
                      className="fas fa-sync-alt fa-spin fa-1x fa-fw"
                    ></i>
                  </CardTitle>
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

          <Row style={{ display: this.state.displayList }}>
            <Col md="12">
              <Card>
                <CardHeader>
                  <CardTitle tag="h5">Emergency Services in Dublin</CardTitle>
                </CardHeader>
                <CardBody className="card-class">
                  <Table>
                    <tbody>
                    {this.state.markers_hospital.map(
                        (hospitalCenters, idx) => (
                          <tr key={idx}>
                          <td>
                            <b>{'HOSPITALS'}</b>
                          </td>
                          <td>{"Name: " + hospitalCenters.hospitalCentersName}</td>
                          <td>{"Address: " + hospitalCenters.hospitalCentersAddress }</td>
                        </tr>
                        )
                      )}

                      {/** GARDA */}
                      {this.state.markers_garda.map((gardaStations, idx) => (
                        <tr key={idx}>
                          <td>
                            <b>{'Public Protection Service'}</b>
                          </td>
                          <td>{"Name: " + gardaStations.GardaStationsName}</td>
                          <td>{"Address: " + gardaStations.GardaStationsAddress}</td>
                          <td>{"Contact: " + gardaStations.GardaStationsPhone}</td>
                        </tr>
                      ))}

                      {/**HOSPITALS */}
                      {this.state.markers_health.map((healthCenter, idx) => (
                        <tr key={idx}>
                          <td>
                            <b>{'HEALTH CENTERS'}</b>
                          </td>
                          <td>{"Name: " + healthCenter.HealthCenterName}</td>
                          <td>{"Address: " + healthCenter.HealthCenterAddress}</td>
                          <td>{"Contact: " + healthCenter.HealthCenterPhone}</td>
                        </tr>
                      ))}

                      {/** FIRE */}
                      {this.state.markers_fireStations.map(
                        (fireStations, idx) => (
                          <tr key={idx}>
                            <td>
                              <b>{'FIRE STATIONS'}</b>
                            </td>
                            <td>{"Name: " + fireStations.fireStationsName}</td>
                            <td>{"Address: " + fireStations.fireStationsAddress}</td>
                            <td>{"Contact: " + fireStations.fireStationsPhone}</td>
                          </tr>
                        )
                      )}
                    </tbody>
                  </Table>
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
