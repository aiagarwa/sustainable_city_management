import React from "react";
import axios from "axios";
// react plugin used to create google maps
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
// reactstrap components
import { Card, CardTitle, CardHeader, CardBody, Row, Col, Table } from "reactstrap";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const iconDefault = L.divIcon({
  className: "custom-pin",
  iconAnchor: [0, 24],
  labelAnchor: [-6, 0],
  popupAnchor: [0, -36],
  html: `<i class="fa fa-map-parking-alt fa-2x" style="color:#000000;"></i>`,
});

L.Marker.prototype.options.icon = iconDefault;

class Parkings extends React.Component {
  setParkingMarkers(parkings_coordinates_dictionary) {
    axios
      .get("/main/parkings_availability/")
      .then(async (res) => {
        let parkings_avaliabilities = res.data.DATA.RESULT[0].parkings;
        console.log(parkings_avaliabilities);

        const markers_parkings = [];

        for (let i = 0; i < parkings_avaliabilities.length; i++) {
          let parking_name = parkings_avaliabilities[i].name;

          // Add markers
          markers_parkings.push({
            name: parking_name,
            area: parkings_coordinates_dictionary[parking_name].area,
            position: [
              parkings_coordinates_dictionary[parking_name].lat,
              parkings_coordinates_dictionary[parking_name].lng,
            ],
            availableSpaces: parkings_avaliabilities[i].availableSpaces,
            icon: {
              className: "custom-pin",
              iconAnchor: [0, 24],
              labelAnchor: [-6, 0],
              popupAnchor: [0, -36],
              html: `<i class="fas fa-parking fa-2x" style="color:#000000;"></i>`,
            },
          });
        }

        localStorage.setItem(
          "parkings_availability",
          JSON.stringify(markers_parkings)
        );
        this.setState({
          markers_parkings,
          graphLoading: false
        });
      })
      .catch((err) => {
        console.error(err);
        if (localStorage.getItem("parkings_availability") != null) {
          const markers_parkings = JSON.parse(
            localStorage.getItem("parkings_availability")
          );
          this.setState({
            markers_parkings,
            graphLoading: false
          });
        }
      });

    axios
      .get("/main/cinema_parkings/")
      .then(async (res) => {
        let results = res.data.DATA.RESULT;
        console.log(results);
        const markers_movies = [];

        const movieParkings = res.data.DATA.RESULT;

        for (const locations of Object.keys(movieParkings)) {
          const movieParkingsName = movieParkings[locations].cinema_name;

          const movieParkings_LAT = movieParkings[locations].cinema_lat;
          const movieParkings_LONG = movieParkings[locations].cinema_lon;

          const movieParkings_ADDRESS = movieParkings[locations].cinema_address;

          // Add markers
          markers_movies.push({
            position: [movieParkings_LAT, movieParkings_LONG],
            MovieParkingsName: movieParkingsName,
            MovieParkingsAddress: movieParkings_ADDRESS,

            icon: {
              className: "custom-pin",
              iconAnchor: [0, 24],
              labelAnchor: [-6, 0],
              popupAnchor: [0, -36],
              html: `<i class="fas fa-parking fa-2x" style="color:#ff5100;"></i>`,
            },
          });
        }

        localStorage.setItem("parkings_movies", JSON.stringify(markers_movies));
        this.setState({ markers_movies: markers_movies });
      })
      .catch((err) => {
        console.log(err);
        if (localStorage.getItem("parkings_movies") != null) {
          const markers_movies = JSON.parse(
            localStorage.getItem("parkings_movies")
          );
          this.setState({ markers_movies: markers_movies });
        }
      });

    axios
      .get("/main/parks_parkings/")
      .then(async (res) => {
        let results = res.data.DATA.RESULT;
        console.log(results);
        const markers_parks = [];

        const parksParkings = res.data.DATA.RESULT;

        for (const locations of Object.keys(parksParkings)) {
          const parksParkingsName = parksParkings[locations].park_name;

          const parksParkings_LAT = parksParkings[locations].park_lat;
          const parksParkings_LONG = parksParkings[locations].park_lon;

          const parksParkings_ADDRESS = parksParkings[locations].park_address;

          // Add markers
          markers_parks.push({
            position: [parksParkings_LAT, parksParkings_LONG],
            ParksParkingsName: parksParkingsName,
            ParksParkingsAddress: parksParkings_ADDRESS,

            icon: {
              className: "custom-pin",
              iconAnchor: [0, 24],
              labelAnchor: [-6, 0],
              popupAnchor: [0, -36],
              html: `<i class="fas fa-parking fa-2x" style="color:#009dff;"></i>`,
            },
          });
        }

        localStorage.setItem("markers_parks", JSON.stringify(markers_parks));
        this.setState({ markers_parks: markers_parks });
      })
      .catch((err) => {
        console.log(err);
        if (localStorage.getItem("markers_parks") != null) {
          const markers_parks = JSON.parse(
            localStorage.getItem("markers_parks")
          );
          this.setState({ markers_parks: markers_parks });
        }
      });

    axios
      .get("/main/beaches_parkings/")
      .then(async (res) => {
        let results = res.data.DATA.RESULT;
        console.log(results);
        const markers_beaches = [];

        const beachesParkings = res.data.DATA.RESULT;

        for (const locations of Object.keys(beachesParkings)) {
          const beachesParkingsName = beachesParkings[locations].beach_name;

          const beachesParkings_LAT = beachesParkings[locations].beach_lat;
          const beachesParkings_LONG = beachesParkings[locations].beach_lon;

          // Add markers
          markers_beaches.push({
            position: [beachesParkings_LAT, beachesParkings_LONG],
            BeachesParkingsName: beachesParkingsName,

            icon: {
              className: "custom-pin",
              iconAnchor: [0, 24],
              labelAnchor: [-6, 0],
              popupAnchor: [0, -36],
              html: `<i class="fas fa-parking fa-2x" style="color:#00ff51;"></i>`,
            },
          });
        }

        localStorage.setItem(
          "markers_beaches",
          JSON.stringify(markers_beaches)
        );
        this.setState({ markers_beaches: markers_beaches });
      })
      .catch((err) => {
        console.log(err);
        if (localStorage.getItem("markers_beaches") != null) {
          const markers_beaches = JSON.parse(
            localStorage.getItem("markers_beaches")
          );
          this.setState({ markers_beaches: markers_beaches });
        }
      });

    axios
      .get("/main/playing_pitches_parkings/")
      .then(async (res) => {
        let results = res.data.DATA.RESULT;
        console.log(results);
        const markers_playingPitches = [];

        const playingPitchesParkings = res.data.DATA.RESULT;

        for (const locations of Object.keys(playingPitchesParkings)) {
          const playingPitches_ParkingsName =
            playingPitchesParkings[locations].facility_name;
          const playingPitches_ParkingsType =
            playingPitchesParkings[locations].facility_type;

          const playingPitches_Parkings_LAT =
            playingPitchesParkings[locations].facility_lat;
          const playingPitches_Parkings_LONG =
            playingPitchesParkings[locations].facility_lon;

          // Add markers
          markers_playingPitches.push({
            position: [
              playingPitches_Parkings_LAT,
              playingPitches_Parkings_LONG,
            ],
            playingPitchesParkingsName: playingPitches_ParkingsName,
            playingPitchesParkingsType: playingPitches_ParkingsType,

            icon: {
              className: "custom-pin",
              iconAnchor: [0, 24],
              labelAnchor: [-6, 0],
              popupAnchor: [0, -36],
              html: `<i class="fas fa-parking fa-2x" style="color:#d000ff;"></i>`,
            },
          });
        }

        localStorage.setItem(
          "markers_playingPitches",
          JSON.stringify(markers_playingPitches)
        );
        this.setState({ markers_playingPitches: markers_playingPitches });
      })
      .catch((err) => {
        console.log(err);
        if (localStorage.getItem("markers_playingPitches") != null) {
          const markers_playingPitches = JSON.parse(
            localStorage.getItem("markers_playingPitches")
          );
          this.setState({ markers_playingPitches: markers_playingPitches });
        }
      });
  }

  getParkingCoordinatesAndSetMarkers() {
    axios
      .get("/main/parkings_locations/")
      .then(async (res) => {
        const parkings_coordinates = res.data.DATA.RESULT;

        let parkings_coordinates_dictionary = {};

        for (let i = 0; i < parkings_coordinates.length; i++) {
          parkings_coordinates_dictionary[parkings_coordinates[i]["name"]] = {
            area: parkings_coordinates[i]["area"],
            lat: parkings_coordinates[i]["lat"],
            lng: parkings_coordinates[i]["lng"],
          };
        }

        localStorage.setItem(
          "parkings_locations",
          JSON.stringify(parkings_coordinates_dictionary)
        );
        this.setParkingMarkers(parkings_coordinates_dictionary);
      })
      .catch((err) => {
        console.error(err);
        if (localStorage.getItem("parkings_locations") != null) {
          const parkings_coordinates_dictionary = JSON.parse(
            localStorage.getItem("parkings_locations")
          );
          this.setState({ displayMap: "none" });
          this.setState({ displayList: "block" });

          if (localStorage.getItem("parkings_availability") != null) {
            const markers_parkings = JSON.parse(
              localStorage.getItem("parkings_availability")
            );
            this.setState({ markers_parkings });
          }

          if (localStorage.getItem("parkings_movies") != null) {
            const markers_movies = JSON.parse(
              localStorage.getItem("parkings_movies")
            );
            this.setState({ markers_movies: markers_movies });
          }

          if (localStorage.getItem("markers_parks") != null) {
            const markers_parks = JSON.parse(
              localStorage.getItem("markers_parks")
            );
            this.setState({ markers_parks: markers_parks });
          }

          if (localStorage.getItem("markers_beaches") != null) {
            const markers_beaches = JSON.parse(
              localStorage.getItem("markers_beaches")
            );
            this.setState({ markers_beaches: markers_beaches });
          }

          if (localStorage.getItem("markers_playingPitches") != null) {
            const markers_playingPitches = JSON.parse(
              localStorage.getItem("markers_playingPitches")
            );
            this.setState({ markers_playingPitches: markers_playingPitches });
          }
        }
      });
  }

  componentDidMount() {
    this.getParkingCoordinatesAndSetMarkers();
  }

  constructor(props) {
    super(props);

    this.state = {
      markers_parkings: [],
      markers_movies: [],
      markers_parks: [],
      markers_beaches: [],
      markers_playingPitches: [],
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
                    Parkings{" "}
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
                      center={[53.445, -6.28]}
                      zoom={11}
                      scrollWheelZoom={true}
                    >
                      <TileLayer
                        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                      />
                      {/** PARKINGS AVAILABILITY */}
                      {this.state.markers_parkings.map((parking_name, idx) => (
                        <Marker
                          key={`marker-${idx}`}
                          position={parking_name.position}
                          icon={L.divIcon(parking_name.icon)}
                        >
                          <Popup>
                            <p>
                              <b>{"PARKINGS AVAILABILITY"}</b>
                            </p>
                            <p>{"Area: " + parking_name.area}</p>
                            <p>
                              {"Available Spaces: " +
                                parking_name.availableSpaces}
                            </p>
                          </Popup>
                        </Marker>
                      ))}

                      {/** MOVIES PARKINGS */}
                      {this.state.markers_movies.map((movieParkings, idx) => (
                        <Marker
                          key={`marker-${idx}`}
                          position={movieParkings.position}
                          icon={L.divIcon(movieParkings.icon)}
                        >
                          <Popup>
                            <p>
                              <b>{"PARKINGS near MOVIES"}</b>
                            </p>
                            <p>{"Name: " + movieParkings.MovieParkingsName}</p>
                            <p>
                              {"Address: " + movieParkings.MovieParkingsAddress}
                            </p>
                          </Popup>
                        </Marker>
                      ))}
                      {/** PARKS PARKINGS */}
                      {this.state.markers_parks.map((parksParkings, idx) => (
                        <Marker
                          key={`marker-${idx}`}
                          position={parksParkings.position}
                          icon={L.divIcon(parksParkings.icon)}
                        >
                          <Popup>
                            <p>
                              <b>{"PARKINGS near PARKS"}</b>
                            </p>
                            <p>{"Name: " + parksParkings.ParksParkingsName}</p>
                            <p>
                              {"Address: " + parksParkings.ParksParkingsAddress}
                            </p>
                          </Popup>
                        </Marker>
                      ))}

                      {/** BEACHES PARKINGS */}
                      {this.state.markers_beaches.map(
                        (beachesParkings, idx) => (
                          <Marker
                            key={`marker-${idx}`}
                            position={beachesParkings.position}
                            icon={L.divIcon(beachesParkings.icon)}
                          >
                            <Popup>
                              <p>
                                <b>
                                  {"PARKINGS near " +
                                    beachesParkings.BeachesParkingsName +
                                    " BEACH"}
                                </b>
                              </p>
                              <p>
                                {"Name: " + beachesParkings.BeachesParkingsName}
                              </p>
                            </Popup>
                          </Marker>
                        )
                      )}
                      {/**PITCHES PARKINGS */}
                      {this.state.markers_playingPitches.map(
                        (playingPitchesParkings, idx) => (
                          <Marker
                            key={`marker-${idx}`}
                            position={playingPitchesParkings.position}
                            icon={L.divIcon(playingPitchesParkings.icon)}
                          >
                            <Popup>
                              <p>
                                <b>{"PARKINGS near PLAYING PITCHES"}</b>
                              </p>
                              <p>
                                {"Name:" +
                                  playingPitchesParkings.playingPitchesParkingsName}
                              </p>
                              <p>
                                {"Type:" +
                                  playingPitchesParkings.playingPitchesParkingsType}
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
                  <CardTitle tag="h5">Parkings</CardTitle>
                </CardHeader>
                <CardBody className="card-class">
                  <Table>
                    <tbody>
                      {/** PARKINGS AVAILABILITY*/}
                      {this.state.markers_parkings.map((parking_name, idx) => (
                        <tr key={idx}>
                          <td>
                            <b>{'PARKINGS AVAILABILITY'}</b>
                          </td>
                          <td>{"Area: " + parking_name.area}</td>
                          <td>{"Available Spaces: " + (parking_name.availableSpaces === 'undefined' ? 'NA' : 
                                                                                          parking_name.availableSpaces) }</td>
                        </tr>
                      ))}

                      {/** MOVIES PARKINGS */}
                      {this.state.markers_movies.map((movieParkings, idx) => (
                        <tr key={idx}>
                          <td>
                            <b>{'MOVIES PARKINGS'}</b>
                          </td>
                          <td>{"Name: " + movieParkings.MovieParkingsName}</td>
                          <td>{"Address: " + movieParkings.MovieParkingsAddress}</td>
                        </tr>
                      ))}
                      {/** PARKS PARKINGS */}
                      {this.state.markers_parks.map((parksParkings, idx) => (
                        <tr key={idx}>
                          <td>
                            <b>{'PARKS PARKINGS'}</b>
                          </td>
                          <td>{"Name: " + parksParkings.ParksParkingsName}</td>
                          <td>{"Address: " + parksParkings.ParksParkingsAddress}</td>
                        </tr>
                      ))}

                      {/** BEACHES PARKINGS */}
                      {this.state.markers_beaches.map(
                        (beachesParkings, idx) => (
                          <tr key={idx}>
                            <td>
                              <b>{'BEACH PARKINGS'}</b>
                            </td>
                            <td>{"Name: " + beachesParkings.BeachesParkingsName}</td>
                          </tr>
                        )
                      )}
                      {/**PITCHES PARKINGS */}
                      {this.state.markers_playingPitches.map(
                        (playingPitchesParkings, idx) => (
                          <tr key={idx}>
                            <td>
                              <b>{'PLAYING PITCH PARKINGS'}</b>
                            </td>
                            <td>{"Name: " + playingPitchesParkings.playingPitchesParkingsName}</td>
                            <td>{"Type: " + playingPitchesParkings.playingPitchesParkingsType}</td>
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

export default Parkings;
