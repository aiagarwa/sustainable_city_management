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

class Buses extends React.Component {
  setBusesGraph(x, y) {
    console.log(x, y);
    this.setState({
      options: {
        xaxis: {
          categories: x,
        },
        annotations: {
          xaxis: [
            {
              x: x[x.length - 1],
              borderColor: "#00E396",
              label: {
                borderColor: "#00E396",
                orientation: "horizontal",
                text: "Prediction",
              },
            },
          ],
        },
      },
      series: [
        {
          name: "Buses in use",
          data: y,
        },
      ],
      graphLoading: false,
    });
  }

  async getLiveValues() {
    try {
      const res = await axios.get(
        "http://127.0.0.1:8000/main/bikestands_details/?type=live"
      );
      const bikeStationsLive = res.data.DATA.RESULT;
      return bikeStationsLive;
    } catch (e) {
      console.log(e);
    }
  }

  componentDidMount() {
    this.setState({ graphLoading: true });
    axios
      .get("http://127.0.0.1:8000/main/bikestands_details/?type=locations")
      .then(async (res) => {
        console.log(res.data);
        const { markers } = this.state;

        const bikeStations = res.data.DATA.RESULT;
        const bikeLiveData = await this.getLiveValues();

        for (const station of Object.keys(bikeStations)) {
          const totalStands = bikeLiveData.hasOwnProperty(station)
            ? bikeLiveData[station].TOTAL_STANDS
            : "No Data";
          const bikesInUse = bikeLiveData.hasOwnProperty(station)
            ? bikeLiveData[station].IN_USE
            : "No Data";

          let markerColor = "grey";
          if (
            typeof totalStands === "number" &&
            typeof bikesInUse === "number"
          ) {
            const ratioInUse = Math.ceil((bikesInUse / totalStands) * 4) / 4;
            markerColor = `rgb(${ratioInUse * 255}, ${
              (1 - ratioInUse) * 200 + 50
            }, ${(1 - ratioInUse) * 80})`;
          }

          markers.push({
            position: [
              bikeStations[station].LATITUDE,
              bikeStations[station].LONGITUDE,
            ],
            content: station,
            totalStands: totalStands,
            inUse: bikesInUse,
            icon: L.divIcon({
              className: "custom-pin",
              iconAnchor: [0, 24],
              labelAnchor: [-6, 0],
              popupAnchor: [0, -36],
              html: `<i class="fa fa-map-marker-alt fa-3x" style="color:${markerColor};"></i>`,
            }),
          });
        }

        markers.sort((a, b) =>
          a.content > b.content ? 1 : b.content > a.content ? -1 : 0
        );
        localStorage.setItem("bikestands_stations", JSON.stringify(markers));

        this.setState({ markers });
      })
      .catch((err) => {
        console.log(err);
        if (localStorage.getItem("bikestands_stations") != null) {
          const markers = JSON.parse(
            localStorage.getItem("bikestands_stations")
          );
          this.setState({ markers });
        }
      });

    axios
      .get(
        "http://127.0.0.1:8000/main/bikestands_graph/?location_based=no&days_historic=5"
      )
      .then((res) => {
        console.log(res.data);
        const x = Object.keys(res.data.DATA.RESULT.ALL_LOCATIONS.IN_USE);
        const y = Object.values(res.data.DATA.RESULT.ALL_LOCATIONS.IN_USE);

        localStorage.setItem("bikestands_graph_x", JSON.stringify(x));
        localStorage.setItem("bikestands_graph_y", JSON.stringify(y));
        this.setBusesGraph(x, y);
      })
      .catch((err) => {
        alert("Offline");
        console.log(err);
        const x = JSON.parse(localStorage.getItem("bikestands_graph_x"));
        const y = JSON.parse(localStorage.getItem("bikestands_graph_y"));

        if (x && y) {
          this.setBusesGraph(x, y);
        }
      });
  }

  onChangeBikeStation = (e) => {
    this.setState({ graphLoading: true });
    const station = e.target.value;
    axios
      .get(
        "http://127.0.0.1:8000/main/bikestands_graph/?location_based=yes&days_historic=5"
      )
      .then((res) => {
        this.setState({ bikeStationSelection: station });
        const x = Object.keys(res.data.DATA.RESULT[station].IN_USE);
        const y = Object.values(res.data.DATA.RESULT[station].IN_USE);
        this.setBusesGraph(x, y);
      })
      .catch((err) => {
        console.log(err);
        this.setState({ graphLoading: false });
      });
  };

  constructor(props) {
    super(props);

    this.state = {
      markers: [],
      options: {
        chart: {
          id: "basic-bar",
        },
      },
      series: [],
      bikeStationSelection: "ALL",
      graphLoading: true,
    };
  }

  render() {
    return (
      <>
        <div className="content">
          <Row>
            <Col md="12">
              <Card>
                <CardHeader>Buses Availability</CardHeader>
                <CardBody>
                  <div className="leaflet-container">
                    <MapContainer
                      style={{ width: "100%", height: "600px" }}
                      center={[53.345, -6.26]}
                      zoom={13}
                      scrollWheelZoom={false}
                    >
                      <TileLayer
                        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                      />
                      {this.state.markers.map(
                        (
                          { position, content, totalStands, inUse, icon },
                          idx
                        ) => (
                          <Marker
                            key={`marker-${idx}`}
                            position={position}
                            icon={icon}
                          >
                            <Popup>
                              <p>
                                <b>{content}</b>
                              </p>
                              <p>{"Total Stands: " + totalStands}</p>
                              <p>{"Buses in use: " + inUse}</p>
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
          <Row>
            <Col md="12">
              <Card className="card-chart">
                <CardHeader>
                  <CardTitle tag="h5">
                    Buses Usage{" "}
                    <i
                      style={{
                        display: this.state.graphLoading
                          ? "inline-block"
                          : "none",
                      }}
                      className="fas fa-sync-alt fa-spin fa-1x fa-fw"
                    ></i>
                  </CardTitle>
                  <p className="card-category">
                    Evolution of Buses usage over time
                  </p>
                </CardHeader>
                <CardBody>
                  <FormGroup row>
                    <Col sm={12} md={4}>
                      <Label>Bike station selection</Label>
                      <Input
                        type="select"
                        name="select"
                        onChange={this.onChangeBikeStation}
                        value={this.state.bikeStationSelection}
                      >
                        <option>ALL</option>
                        {this.state.markers.map(
                          ({ position, content }, index) => (
                            <option key={index}>{content}</option>
                          )
                        )}
                      </Input>
                    </Col>
                  </FormGroup>

                  <div className="mixed-chart">
                    <Chart
                      options={this.state.options}
                      series={this.state.series}
                      type="line"
                      height="250"
                    />
                  </div>
                </CardBody>
                <CardFooter>
                  {/* <div className="chart-legend">
                      <i className="fa fa-circle text-info" /> Tesla Model S{" "}
                      <i className="fa fa-circle text-warning" /> BMW 5 Series
                    </div> */}
                  <hr />
                  <div className="card-stats">
                    <i className="fa fa-check" /> Data information certified
                  </div>
                </CardFooter>
              </Card>
            </Col>
          </Row>
        </div>
      </>
    );
  }
}

export default Buses;