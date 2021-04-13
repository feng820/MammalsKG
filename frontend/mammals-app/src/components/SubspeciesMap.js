// We will use these things from the lib
// https://react-google-maps-api-docs.netlify.com/
// doc:
// https://react-google-maps-api-docs.netlify.app/
// https://medium.com/@allynak/how-to-use-google-map-api-in-react-app-edb59f64ac9d
// https://sites.google.com/site/gmapsdevelopment/
import {
    GoogleMap,
    InfoWindow, Marker, useLoadScript
} from "@react-google-maps/api";
import { Card, Carousel, Col, Divider, Image, Row } from 'antd';
import axios from 'axios';
import React, { Component, Fragment, useState } from "react";
import ErrorImg from '../assets/No_image_available.svg';

function Map(props) {
    // The things we need to track in state
    const [mapRef, setMapRef] = useState(null);
    const [selectedPlace, setSelectedPlace] = useState(null);
    const [markerMap, setMarkerMap] = useState({});
    const [center, setCenter] = useState({ lat: 0.0, lng: 0.0 });
    const [zoom, setZoom] = useState(3);
    const [clickedLatLng, setClickedLatLng] = useState(null);
    const [infoOpen, setInfoOpen] = useState(false);

    // Load the Google maps scripts
    const { isLoaded } = useLoadScript({
        // Enter your own Google Maps API key
        googleMapsApiKey: "AIzaSyCkj_10LMNcSTaDVK1jfrR8edmabgzJZjU",
        language: "en"
    });

    const myMammals = props.subspecies;
    const myPlaces = []
    const noPlaces = []
    var i = 0
    var type = 0
    myMammals.map((mammal) => {
        mammal.mammal__location_info.map(place => {
            const coords = place => {
                var arr = place[2].split(', ')
                var lat = parseFloat(arr[0].slice(0, -1))
                var lng = parseFloat(arr[1].slice(0, -1))
                if (arr[0].slice(-1) === 'S') {
                    lat *= -1;
                }
                if (arr[1].slice(-1) === 'W') {
                    lng *= -1;
                }
                return { lat: lat, lng: lng }
            }
            myPlaces.push({
                id: i++, pos: coords(place), place: place[0], time: place[1], name: mammal.mammal__name,
                taxonName: mammal.mammal__taxonName, wikiUrl: mammal.mammal__wiki_uri,
                uri: mammal.uri, type: type, coordinate: place[2]
            })
        })
        type++;

        if (mammal.mammal__location_info.length === 0) {
            noPlaces.push({
                name: mammal.mammal__name, taxonName: mammal.mammal__taxonName,
                wikiUrl: mammal.mammal__wiki_uri
            })
        }
    })

    // Iterate myPlaces to size, center, and zoom map to contain all markers
    const fitBounds = (map) => {
        const bounds = new window.google.maps.LatLngBounds();
        myPlaces.map((place) => {
            bounds.extend(place.pos);
            return place.id;
        });
        map.fitBounds(bounds);
    };

    const loadHandler = (map) => {
        setZoom(3);
        // Store a reference to the google map instance in state
        setMapRef(map);
        // TODO: Fit map bounds to contain all markers
        // fitBounds(map);
    };

    // We have to create a mapping of our places to actual Marker objects
    const markerLoadHandler = (marker, place) => {
        return setMarkerMap((prevState) => {
            return { ...prevState, [place.id]: marker };
        });
    };

    const markerClickHandler = (event, place) => {
        // Remember which place was clicked
        setSelectedPlace(place);

        // Required so clicking a 2nd marker works as expected
        if (infoOpen) {
            setInfoOpen(false);
        }

        setInfoOpen(true);

        // If you want to zoom in a little on marker click
        //   if (zoom < 10) {
        //     setZoom(10);
        //   }

        // if you want to center the selected Marker
        //   setCenter(place.pos)
    };

    const colorList = ['yellow', 'blue', 'green', 'lightblue', 'orange', 'pink', 'purple', 'red'];
    const contentStyle = {
        paddingTop: '15px',
        height: '300px',
        color: '#fff',
        fontSize: '20px',
        lineHeight: '7px',
        textAlign: 'center',
        background: '#C0C0C0',
    };
    const italicStyle = {
        fontStyle: 'italic',
    }
    const renderMap = () => {
        return (
            <Fragment>
                <Row>
                    <Col span={18}>
                        <GoogleMap
                            // Do stuff on map initial laod
                            onLoad={loadHandler}
                            // Save the current center position in state
                            onCenterChanged={() => setCenter(mapRef.getCenter().toJSON())}
                            // Save the user's map click position
                            onClick={(e) => setClickedLatLng(e.latLng.toJSON())}
                            center={center}
                            zoom={zoom}
                            mapContainerStyle={{
                                height: "93vh",
                                width: "100%"
                            }}
                        >
                            {myPlaces.map((place) => (
                                <Marker
                                    key={place.id}
                                    position={place.pos}
                                    onLoad={(marker) => markerLoadHandler(marker, place)}
                                    onMouseOver={(event) => markerClickHandler(event, place)}
                                    onMouseOut={() => setInfoOpen(false)}
                                    icon={{
                                        url: `http://maps.google.com/mapfiles/ms/icons/${colorList[place.type % colorList.length]}.png`,
                                        fillOpacity: 1.0,
                                        strokeWeight: 0,
                                        scale: 1
                                    }}
                                />
                            ))}

                            {infoOpen && selectedPlace && (
                                <InfoWindow
                                    anchor={markerMap[selectedPlace.id]}
                                    onCloseClick={() => setInfoOpen(false)}
                                >
                                    <div>
                                        <h3>{selectedPlace.name}</h3>
                                        <div>
                                            <p>Place found: {selectedPlace.place}</p>
                                            <p>Found time: {selectedPlace.time}</p>
                                            <p>Coordinate: {selectedPlace.coordinate}</p>
                                        </div>
                                    </div>
                                </InfoWindow>
                            )}
                        </GoogleMap>
                    </Col>

                    <Col span={6}>
                        {noPlaces.length > 0 && (
                            <>
                                <Divider orientation="center" style={{ fontSize: 25 }}> Other Mammals </Divider>
                                <Carousel autoplay>
                                    {noPlaces.map((place) => (
                                        <div>
                                            <div style={contentStyle}>
                                                <p>Name: <span style={italicStyle}>{place.name}</span></p>
                                                <p>Taxon name: <span style={italicStyle}>{place.taxonName}</span></p>
                                                {/* TODO: 加入subspecies img */}
                                                <a href={place.wikiUrl} target="_blank" rel="noreferrer">
                                                <Image
                                                    preview={false}
                                                    width={150}
                                                    height={200}
                                                    src={place.mammal__icon || 'error'}
                                                    fallback={ErrorImg}
                                                />
                                                </a>
                                            </div>
                                        </div>
                                    ))}
                                </Carousel>
                            </>
                        )}


                        {selectedPlace && (
                            // <div>
                            //     <h2>Name: {selectedPlace.name}</h2>
                            //     <p>Taxon Name: {selectedPlace.taxonName}</p>
                            //     <p>WiKi url:
                            // <a target="_blank" href={selectedPlace.wikiUrl} rel="noreferrer"> {selectedPlace.wikiUrl}</a>
                            //     </p>
                            // </div>
                            <>
                                <Divider orientation="center" style={{ fontSize: 25 }}> Selected Mammals </Divider>
                                <Card
                                    hoverable
                                    // style={{ width: 240 }}
                                    title={selectedPlace.name}
                                    extra={<a target="_blank" href={selectedPlace.wikiUrl} rel="noreferrer"> More</a>}
                                >
                                    <p>Taxon Name: {selectedPlace.taxonName}</p>
                                    {/* <Meta title='' description= "Selected mammal"/> */}
                                </Card>
                            </>
                            //     <>
                            //     <Descriptions title="User Info">
                            //     <Descriptions.Item label="UserName">Zhou Maomao</Descriptions.Item>
                            //     <Descriptions.Item label="Telephone">1810000000</Descriptions.Item>
                            //     <Descriptions.Item label="Live">Hangzhou, Zhejiang</Descriptions.Item>
                            //     <Descriptions.Item label="Remark">empty</Descriptions.Item>
                            //     <Descriptions.Item label="Address">
                            //       No. 18, Wantang Road, Xihu District, Hangzhou, Zhejiang, China
                            //     </Descriptions.Item>
                            //   </Descriptions>,
                            //   </>
                        )}
                    </Col>
                </Row>
            </Fragment>
        );
    };

    return isLoaded ? renderMap() : null;
}

export class SubspeciesMap extends Component {
    constructor(props) {
        super();
        this.state = {
            mammalId: props.match.params.mammalId,
            subspecies: [],
        }
        this.fetchData();
    }

    fetchData = () => {
        const url = "http://127.0.0.1:5000/mammal/" + this.state.mammalId;
        axios.get(url).then(res => {
            const mammal = res.data;
            this.setState({
                subspecies: mammal.subspecies,
            })
        }).catch(err => {
            const errMsg = err.message || 'Unknown error';
            console.error(errMsg);
        });
    }

    render() {
        return (
            <Map
                subspecies={this.state.subspecies}
            />
        )
    }
}
