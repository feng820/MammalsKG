import { Card, Col, Collapse, Descriptions, Divider, Image, Row, Table } from 'antd';
import axios from 'axios';
import React, { Component } from 'react';
import { Link } from "react-router-dom";
import ErrorImg from '../assets/No_image_available.svg';
const { Panel } = Collapse;
const { Meta } = Card;
const { Column } = Table;

// TODO: add img
function Describe(props) {
    var coordinates = [];
    if (props.ecoInfo.ecoregion__coordinates && props.ecoInfo.ecoregion__coordinates !== "None") {
        coordinates = JSON.parse(props.ecoInfo.ecoregion__coordinates.replace(/'/g, '"'));
    }
    return (
        <div>
            <Row style={{ marginTop: 20 }} justify="center">
                <Col span={6}>
                    <Image
                        className="img"
                        src={props.ecoInfo.ecoregion__image || null}
                        height={300}
                        width={300}
                        fallback={ErrorImg}
                    />
                </Col>
                <Col span={16} style={{ marginLeft: 40, marginTop: 5 }}>
                    <Descriptions bordered size="middle">
                        <Descriptions.Item label="Name">{props.ecoInfo.ecoregion__name}</Descriptions.Item>
                        <Descriptions.Item label="Biome">{props.ecoInfo.ecoregion__Biome}</Descriptions.Item>
                        <Descriptions.Item label="Country">{props.ecoInfo.ecoregion__Country}</Descriptions.Item>
                        <Descriptions.Item label="Conservation status">{props.ecoInfo.ecoregion__Conservation_status}</Descriptions.Item>
                        <Descriptions.Item label="Coordinates">{coordinates[0]}<br />{coordinates[1]}</Descriptions.Item>
                        <Descriptions.Item label="Area">{props.ecoInfo.ecoregion__Area}</Descriptions.Item>
                        <Descriptions.Item label="URL" span={3}><a target="_blank" href={props.ecoInfo.ecoregion__url} rel="noreferrer">
                            {props.ecoInfo.ecoregion__url}</a></Descriptions.Item>
                        <Descriptions.Item label="URI" span={3}>{props.ecoInfo.uri}</Descriptions.Item>
                    </Descriptions>
                </Col>
            </Row>
        </div>
    )
}

function MyCard(props) {
    return (
        <Col span={6}>
            <Card
                size="small"
                hoverable
                bordered={false}
                cover={<Image
                    className="img"
                    src={props.item.non_mammal__icon}
                    height={180}
                    width={180}
                    fallback={ErrorImg}
                />}
            >
                <Meta title={props.item.non_mammal__name} description={props.item.non_mammal__taxonName} />
            </Card>
        </Col>
    )
}

function arrayToObject(arr) {
    var obj = {};
    var ind = ['name', 'time', 'coordinate']
    for (var i = 0; i < arr.length; ++i) {
        obj[ind[i]] = arr[i];
    }
    return obj;
}

class FancyCard extends React.Component {
    constructor(props) {
        super(props);
        // console.log(props.item)

        var locations = []
        const infos = JSON.parse(props.item.mammal__location_info.replace(/'/g, '"'))
        for (var i = 0; i < infos.length; ++i) {
            locations.push(arrayToObject(infos[i]))
        }
        // console.log(locations)

        const tabList = [
            {
                key: 'tab1',
                tab: 'Info',
            },
            {
                key: 'tab2',
                tab: 'Location',
            },
        ];

        const contentList = {
            tab1: <div>
                    <img src={ErrorImg} alt="No img available" width="150" height="200" />
                    <br />
                    {props.item.mammal__taxonName}
                  </div>,
            // tab2: <p>content2</p>,
            tab2: 
            <Table dataSource={locations} size="small" scroll={{y: 230}} pagination={{
                total: locations.length,
                pageSize: locations.length,
                hideOnSinglePage: true
            }}>
                <Column title="Name" dataIndex="name" key="name" />
                <Column title="Time" dataIndex="time" key="time" />
                <Column title="Coordinate" dataIndex="coordinate" key="coordinate" />
            </Table>
        };

        this.state = {
            tabList: tabList,
            contentList: contentList,
            key: 'tab1',
        }
    }

    onTabChange = (key, type) => {
        console.log(key, type);
        this.setState({ [type]: key });
    };

    render() {
        return (
            <Col span={8}>
                <Card
                    style={{ width: '100%', height: 400 }}
                    title={this.props.item.mammal__name}
                    extra={<a href="#">More</a>}
                    // cover={<Image
                    //     className="img"
                    //     src={this.props.item.uri}
                    //     height={180}
                    //     width={180}
                    //     fallback={ErrorImg}
                    // />}
                    tabList={this.state.tabList}
                    activeTabKey={this.state.key}
                    onTabChange={key => {
                        this.onTabChange(key, 'key');
                    }}
                >
                    {this.state.contentList[this.state.key]}
                </Card>
            </Col>
        )
    }
}

function Accordion(props) {
    const text = `
  A dog is a type of domesticated animal.
  Known for its loyalty and faithfulness,
  it can be found as a welcome guest in many households across the world.
    `;
    // console.log('hello')
    // if (props.floras.length > 0) {
    //     console.log(props.floras[0].uri)
    // }

    const gridStyle = {
        width: '25%',
        textAlign: 'center',
    };

    return (
        <Collapse accordion>
            {props.faunaMammals.length > 0 &&
                <Panel header="Fauna mammals" key="1">
                    <Card>
                        {props.faunaMammals.map((animal, index) => (
                            <Link to={{
                                pathname: "/mammal/" + animal[0],
                            }}>
                                <Card.Grid style={gridStyle} key={index}>{animal[1]}</Card.Grid>
                            </Link>
                        ))}
                    </Card>
                </Panel>
            }
            {props.faunaMammalSubs.length > 0 &&
                <Panel header="Fauna mammals subspecies" key="2">
                    {/* <p>{text}</p> */}
                    {/* <FancyCard extends React.></FancyCard extends React.> */}
                    <div className="site-card-wrapper">
                        <Row gutter={[16, 16]}>
                            {props.faunaMammalSubs.map((item) => (
                                <FancyCard
                                    item={item}
                                />
                            ))}
                        </Row>
                    </div>
                </Panel>
            }
            {props.faunaNonMammals.length > 0 &&
                <Panel header="Fauna non mammals" key="3">
                    {/* <p>{text}</p> */}
                    <div className="site-card-wrapper">
                        <Row gutter={[16, 16]}>
                            {props.faunaNonMammals.map((item) => (
                                <MyCard
                                    item={item}
                                />
                            ))}
                        </Row>
                    </div>
                </Panel>
            }
            {props.floras.length > 0 &&
                <Panel header="Floras" key="4">
                    {/* <p>{text}</p> */}
                    <div className="site-card-wrapper">
                        <Row gutter={[16, 16]}>
                            {props.floras.map((item) => (
                                <MyCard
                                    item={item}
                                />
                            ))}
                        </Row>
                    </div>
                </Panel>
            }
        </Collapse>
    )
}

export class Ecoregion extends Component {
    constructor(props) {
        super();
        console.log(props.match.params.ecoId);
        this.state = {
            ecoId: props.match.params.ecoId,
            ecoInfo: {},
            faunaMammals: [],
            faunaNonMammals: [],
            faunaMammalSubs: [],
            floras: [],
        }
        this.fetchData();
    }

    fetchData = () => {
        const url = "http://127.0.0.1:5000/ecoregion/" + this.state.ecoId;
        axios.get(url).then(res => {
            const eco = res.data;
            // console.log(eco);
            this.setState({
                ecoInfo: eco.n,
                faunaMammals: eco.fauna_mammals,
                faunaNonMammals: eco.fauna_non_mammals,
                faunaMammalSubs: eco.fauna_mammal_subs,
                floras: eco.floras,
            })
            // console.log(this.state.floras);
        }).catch(err => {
            const errMsg = err.message || 'Unknown error';
            console.error(errMsg);
        });
    }

    render() {
        return (
            <div>
                <Divider orientation="center" style={{ fontSize: 30 }}> Basic Information </Divider>
                {this.state.ecoInfo &&
                    <Describe
                        ecoInfo={this.state.ecoInfo}
                    />
                }
                <Divider orientation="center" style={{ fontSize: 30 }}> Fauna & Flora </Divider>
                <Accordion
                    faunaMammals={this.state.faunaMammals}
                    faunaNonMammals={this.state.faunaNonMammals}
                    faunaMammalSubs={this.state.faunaMammalSubs}
                    floras={this.state.floras}
                />
            </div>
        );
    }
}