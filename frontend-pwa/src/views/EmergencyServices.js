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
  getFootfallCoordinates() {}
  catch(e) {
    console.log(e);
  }

  componentDidMount() {
    axios.get("http://127.0.0.1:8000/main/health_centers/").then(async (res) => {
        let results = res.data.DATA.RESULT;
        console.log(results);
      }
    ).catch(error => {
      console.error(error);
    });
  }

  constructor(props) {
    super(props);

    this.state = {
      markers: [],
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
        </div>
      </>
    );
  }
}

export default EmergencyServices;
