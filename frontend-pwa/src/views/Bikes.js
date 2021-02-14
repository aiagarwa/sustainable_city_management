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
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
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
  Form,
  Label,
  Input,
} from "reactstrap";
import L from "leaflet";
import 'leaflet/dist/leaflet.css';

import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow
});

L.Marker.prototype.options.icon = DefaultIcon;

class Bikes extends React.Component {
  componentDidMount() {
    axios
      .get("/bikestands_details/?type=locations")
      .then((res) => {
        console.log(res.data);
        const { markers } = this.state;

        const bikeStations = res.data.DATA.RESULT;

        for (const station of Object.keys(bikeStations)) {
          markers.push({
            position: [bikeStations[station].LATITUDE, bikeStations[station].LONGITUDE],
            content: station
          });
        }

        markers.sort((a, b) => (a.content > b.content) ? 1 : ((b.content > a.content) ? -1 : 0))

        this.setState({ markers });
      });

    axios
      .get("/bikestands_graph/?location_based=no&days_historic=5")
      .then((res) => {

        const x = Object.keys(res.data.DATA.RESULT.ALL_LOCATIONS.IN_USE);
        const y = Object.values(res.data.DATA.RESULT.ALL_LOCATIONS.IN_USE);

        this.setState({
          options: {
            xaxis: {
              categories: x
            },
            annotations: {
              xaxis: [
                {
                  x: x[x.length-1],
                  borderColor: '#00E396',
                  label: {
                    borderColor: '#00E396',
                    orientation: 'horizontal',
                    text: 'Prediction'
                  }
                }
              ]
            }
          },
          series: [{
            name: "Bikes in use",
            data: y
          }]
        })
      });
  }

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
    };
  }

  render() {
    return (
      <>
        <div className="content">
          <Row>
            <Col md="12">
              <Card>
                <CardHeader>Open Street Maps</CardHeader>
                <CardBody>
                  <div
                    className="leaflet-container"
                  >
                    <MapContainer style={{ width: '100%', height: '600px' }} center={[53.34, -6.28]} zoom={12} scrollWheelZoom={false}>
                      <TileLayer
                        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                      />
                      {this.state.markers.map(({ position, content }, idx) =>
                        <Marker key={`marker-${idx}`} position={position}>
                          <Popup>
                            <span>{content}</span>
                          </Popup>
                        </Marker>
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
                  <CardTitle tag="h5">Bikes Usage</CardTitle>
                  <p className="card-category">
                    Evolution of bikes usage over time
                  </p>
                </CardHeader>
                <CardBody>

                  <FormGroup row>
                    <Col sm={12} md={4}>
                      <Label>Bike station selection</Label>
                      <Input type="select" name="select">
                        <option>All</option>
                        {this.state.markers.map(({ position, content }, index) =>
                          <option key={index}>{content}</option>)}
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
