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

class Footfall extends React.Component {
  getFootfallCoordinates() {}
  catch(e) {
    console.log(e);
  }

  componentDidMount() {
    axios.get("http://127.0.0.1:8000/main/footfall_overall/").then(
      async (res) => {
        console.log(res.data);
        let { markers } = this.state;

        const areaLocations = res.data.DATA.RESULT;

        let locations = []
        for (const location of Object.keys(areaLocations)) {
          locations.push(location)
          const footfallCounts = areaLocations[location].Footfall;
          const footfall_LAT = areaLocations[location].Lat;
          const footfall_LON = areaLocations[location].Lon;

          // Add markers
          markers.push({
            position: [
              areaLocations[location].Lat,
              areaLocations[location].Lon,
            ],
            // locations: areaLocation,
            areaName: location,
            FootfallCounts: footfallCounts,

            icon: {
              className: "custom-pin",
              iconAnchor: [0, 24],
              labelAnchor: [-6, 0],
              popupAnchor: [0, -36],
              html: `<i class="fas fa-shoe-prints fa-2x" style="color:black;"></i>`,
            },
          });

          this.setState({
            markers: markers,
            locations: locations
          });
        }
      }
    );
  }

  setFootfallGraph(x, y) {
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
          name: "Footfalls",
          data: y,
        },
      ],
      graphLoading: false,
    });
  }

  onChangeFootfallLocation = (e) => {
    const location = e.target.value;
    this.setState({ graphLoading: true });
    this.setState({ footfallLocationSelected: location });

    if(location == "Not Selected") {
      const x = [];
      const y = [];
      this.setFootfallGraph(x, y);
      return;
    }

    axios.get(
        "http://127.0.0.1:8000/main/footfall_datebased/?days_interval=6&location=" + location
      )
      .then((res) => {
        let result = res.data.DATA.RESULT
        const x = Object.keys(result[location]);
        const y = Object.values(result[location]);
        this.setFootfallGraph(x, y)
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
      footfallLocationSelected: "",
      locations: []
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
                  <CardTitle tag="h5">Footfalls in Dublin</CardTitle>
                </CardHeader>
                <CardBody>
                  <div className="leaflet-container">
                    <MapContainer
                      style={{ width: "100%", height: "600px" }}
                      center={[53.345, -6.26]}
                      zoom={15}
                      scrollWheelZoom={false}
                    >
                      <TileLayer
                        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                      />
                      {this.state.markers.map(
                        (
                          { position, name, FootfallCounts, areaName, icon },
                          idx
                        ) => (
                          <Marker
                            key={`marker-${idx}`}
                            position={position}
                            icon={L.divIcon(icon)}
                          >
                            <Popup>
                              <p>
                                <b>{name}</b>
                              </p>
                              <p>{"Area: " + areaName}</p>
                              <p>{"Footfall Counts: " + FootfallCounts}</p>
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
                    Footfall History{" "}
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
                    Evolution of footfalls over time
                  </p>
                </CardHeader>
                <CardBody>
                  <FormGroup row>
                    <Col sm={12} md={4}>
                      <Label>Footfall location selection</Label>
                      <Input
                        type="select"
                        name="select"
                        onChange={this.onChangeFootfallLocation}
                        value={this.state.footfallLocationSelected}
                      >
                        <option>Not Selected</option>
                        {this.state.locations.map(
                          ((location, index) => (
                            <option key={index}>{location}</option>
                          )
                        ))}
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

export default Footfall;
