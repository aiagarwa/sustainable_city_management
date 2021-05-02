import React from "react";
import axios from "axios";
// react plugin used to create google maps
import Chart from "react-apexcharts";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
// reactstrap components
import {
  Card,
  CardTitle,
  CardSubtitle,
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

class Bikes extends React.Component {
  setBikesGraph(x, y) {
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
          name: "Bikes in use",
          data: y,
        },
      ],
      graphLoading: false,
    });
  }

  async getLiveValues() {
    try {
      const res = await axios.get("/main/bikestands_details/?type=live");
      const bikeStationsLive = res.data.DATA.RESULT;
      return bikeStationsLive;
    } catch (e) {
      console.log(e);
    }
  }

  componentDidMount() {
    this.setState({ graphLoading: true });
    axios
      .get("/main/bikestands_details/?type=locations")
      .then(async (res) => {
        console.log(res.data);
        let { markers, recommendations } = this.state;

        const bikeStations = res.data.DATA.RESULT;
        const bikeLiveData = await this.getLiveValues();

        for (const station of Object.keys(bikeStations)) {
          const totalStands = bikeLiveData.hasOwnProperty(station)
            ? bikeLiveData[station].TOTAL_STANDS
            : "No Data";
          const bikesInUse = bikeLiveData.hasOwnProperty(station)
            ? bikeLiveData[station].IN_USE
            : "No Data";
          const ratioInUse = bikesInUse / totalStands;

          // Markers color
          let markerColor = "grey";
          if (
            typeof totalStands === "number" &&
            typeof bikesInUse === "number"
          ) {
            const rgbRatio = Math.ceil((bikesInUse / totalStands) * 4) / 4;
            markerColor = `rgb(${rgbRatio * 255}, ${
              (1 - rgbRatio) * 200 + 50
            }, ${(1 - rgbRatio) * 80})`;
          }

          // Add markers
          markers.push({
            position: [
              bikeStations[station].LATITUDE,
              bikeStations[station].LONGITUDE,
            ],
            content: station,
            totalStands: totalStands,
            inUse: bikesInUse,
            markerColor: markerColor,
            icon: {
              className: "custom-pin",
              iconAnchor: [0, 24],
              labelAnchor: [-6, 0],
              popupAnchor: [0, -36],
              html: `<i class="fa fa-map-marker-alt fa-3x" style="color:${markerColor};"></i>`,
            },
          });

          // Add recommendations
          if (ratioInUse >= 0.9) {
            recommendations.push({
              color: ratioInUse >= 0.95 ? "red" : "orange",
              percentageInUse: Math.trunc(ratioInUse * 100),
              station: station
            });
          }
        }

        // Sort markers (i.e. list of stations, alphabetically) & store them
        markers.sort((a, b) =>
          a.content > b.content ? 1 : b.content > a.content ? -1 : 0
        );
        localStorage.setItem("bikestands_stations", JSON.stringify(markers));

        // Sort recommendations by importance
        recommendations.sort((a, b) =>
          a.color === "red" ? -1 : b.color === "orange" ? 0 : 1
        );
        recommendations = recommendations.slice(0, 8);

        localStorage.setItem(
          "bikestands_recommendations",
          JSON.stringify(recommendations)
        );

        this.setState({ markers });
        this.setState({ recommendations });
        this.setState({ displayMap: "block" });
        this.setState({ displayList: "none" });
      })
      .catch((err) => {
        console.log(err);
        if (localStorage.getItem("bikestands_stations") != null) {
          const markers = JSON.parse(
            localStorage.getItem("bikestands_stations")
          );
          this.setState({ markers });
          this.setState({ displayMap: "none" });
          this.setState({ displayList: "block" });
        }

        if (localStorage.getItem("bikestands_recommendations") != null) {
          const recommendations = JSON.parse(
            localStorage.getItem("bikestands_recommendations")
          );
          this.setState({ recommendations });
        }
      });

    axios
      .get("/main/bikestands_graph/?location_based=no&days_historic=5")
      .then((res) => {
        console.log(res.data);
        const x = Object.keys(res.data.DATA.RESULT.ALL_LOCATIONS.IN_USE);
        const y = Object.values(res.data.DATA.RESULT.ALL_LOCATIONS.IN_USE);

        localStorage.setItem("bikestands_graph_x", JSON.stringify(x));
        localStorage.setItem("bikestands_graph_y", JSON.stringify(y));
        this.setBikesGraph(x, y);
      })
      .catch((err) => {
        console.log(err);
        const x = JSON.parse(localStorage.getItem("bikestands_graph_x"));
        const y = JSON.parse(localStorage.getItem("bikestands_graph_y"));

        if (x && y) {
          this.setBikesGraph(x, y);
        }
      });
  }

  onChangeBikeStation = (e) => {
    this.selectBikeStation(e.target.value);
  };

  onClickBikeStation = (e) => {
    e.preventDefault();
    console.log(e.target.innerText);
    this.selectBikeStation(e.target.innerText);
    document.getElementById("chart-bikes-usage").scrollIntoView({behavior: "smooth", block: "end"});
  }
  
  selectBikeStation = (station) => {
    this.setState({ graphLoading: true });
    axios
      .get("/main/bikestands_graph/?location_based=yes&days_historic=5")
      .then((res) => {
        this.setState({ bikeStationSelection: station });
        const x = Object.keys(res.data.DATA.RESULT[station].IN_USE);
        const y = Object.values(res.data.DATA.RESULT[station].IN_USE);
        this.setBikesGraph(x, y);
      })
      .catch((err) => {
        console.log(err);
        this.setState({ graphLoading: false });
      });
  }

  constructor(props) {
    super(props);

    this.state = {
      markers: [],
      recommendations: [],
      options: {
        chart: {
          id: "basic-bar",
        },
      },
      series: [],
      bikeStationSelection: "ALL",
      graphLoading: true,
      displayMap: "block",
      displayList: "none",
    };
  }

  render() {
    return (
      <>
        <div className="content">
          <Row>
            <Col md="9" style={{ display: this.state.displayMap }}>
              <Card>
                <CardHeader>
                  <CardTitle tag="h5">
                    Bikes Usage{" "}
                    <i
                      style={{
                        display: this.state.graphLoading
                          ? "inline-block"
                          : "none",
                      }}
                      className="fas fa-sync-alt fa-spin fa-1x fa-fw"
                    ></i>
                    </CardTitle>
                  <CardSubtitle>Real-time</CardSubtitle>
                </CardHeader>
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
                            id={`marker-bike-station-${content}`}
                            key={`marker-${idx}`}
                            position={position}
                            icon={L.divIcon(icon)}
                          >
                            <Popup>
                              <p>
                                <b>{content}</b>
                              </p>
                              <p>{"Total Stands: " + totalStands}</p>
                              <p>{"Bikes in use: " + inUse}</p>
                            </Popup>
                          </Marker>
                        )
                      )}
                    </MapContainer>
                  </div>
                </CardBody>
              </Card>
            </Col>
            <Col md="9" style={{ display: this.state.displayList }}>
              <Card>
                <CardHeader>
                  <CardTitle tag="h5">Bikes Usage</CardTitle>
                </CardHeader>
                <CardBody className="card-class">
                  <Table>
                    <tbody>
                      {this.state.markers.map(
                        (
                          {
                            position,
                            content,
                            totalStands,
                            inUse,
                            markerColor,
                          },
                          idx
                        ) => (
                          <tr key={idx}>
                            <td>
                              <span
                                className="dot"
                                style={{ backgroundColor: markerColor }}
                              ></span>
                            </td>
                            <td>
                              <b>{content}</b>
                            </td>
                            <td>{" Bike Stands: " + totalStands}</td>
                            <td>{" In use: " + inUse}</td>
                          </tr>
                        )
                      )}
                    </tbody>
                  </Table>
                </CardBody>
              </Card>
            </Col>
            <Col md="3">
              <Card id="recommendations">
                <CardHeader>
                  <CardTitle tag="h5">Recommendations</CardTitle>
                  <CardSubtitle>Real-time</CardSubtitle>
                  <div style={{ opacity: 0.6 }}>
                    <p className="mb-0">
                      <span
                        className="dot mr-2"
                        style={{ backgroundColor: "red" }}
                      ></span>
                      Consider adding bikes
                    </p>
                    <p>
                      <span
                        className="dot mr-2"
                        style={{ backgroundColor: "orange" }}
                      ></span>
                      High bikes usage
                    </p>
                  </div>
                </CardHeader>
                <CardBody>
                  <Table>
                    <tbody>
                      {this.state.recommendations.map(
                        ({ color, percentageInUse, station }, key) => (
                          <tr key={key}>
                            <td>
                              <span
                                className="dot"
                                style={{ backgroundColor: color }}
                              ></span>
                            </td>
                            <td>{percentageInUse}% of bikes are used at <a href="#" onClick={this.onClickBikeStation}>{station}</a></td>
                          </tr>
                        )
                      )}
                    </tbody>
                  </Table>
                </CardBody>
              </Card>
            </Col>
          </Row>

          <Row id="chart-bikes-usage">
            <Col md="12">
              <Card className="card-chart">
                <CardHeader>
                  <CardTitle tag="h5">
                    Bikes Usage{" "}
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
                    Evolution of bikes usage over time and future predictions
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

export default Bikes;
