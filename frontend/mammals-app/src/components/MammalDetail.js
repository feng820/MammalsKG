import React, { Component } from 'react';
import axios from 'axios';
import { Image, Descriptions, Row, Col, Tag, Statistic, List, Divider, Button, Card, Collapse } from 'antd';
import ErrorImg from '../assets/No_image_available.svg'
import { Link } from "react-router-dom";

export class MammalDetail extends Component {
    constructor(props) {
        super();
        this.state = {
            mammalID: props.match.params.mammalId,
            mammalInfo: "",
            subspecies: [],
            ecoregion: [],
            competitors: [],
            predators: [],
            preys: [],
            nm_predators: [],
            nm_preys: [],
            nm_competitors: [],
        };
    }

    fetchData = () => {
        const url = "http://127.0.0.1:5000/mammal/" + this.state.mammalID;
        axios.get(url).then(res => {
            console.log(res.data);
            this.setState({
                mammalInfo: res.data.n,
                subspecies: res.data.subspecies,
                ecoregion: res.data.ecoregions,
                competitors: res.data.competitors,
                predators: res.data.predators,
                preys: res.data.preys,
                nm_predators: res.data.nm_predators === undefined ? [] : res.data.nm_predators,
                nm_preys: res.data.nm_preys === undefined ? [] : res.data.nm_preys,
                nm_competitors: res.data.nm_competitors === undefined ? [] : res.data.nm_competitors
            })

        }).catch(e => {
            const error = e.error || 'Unknown Error';
            console.log("Cannot fetch due to error: " + error);
        });
    }

    componentDidMount() {
        this.fetchData();
        window.scrollTo(0, 0)
    }

    render() {
        return (
            <div>
                <Divider orientation="center" style={{fontSize: 30}}> Basic Information </Divider>
                <Row style={{marginTop: 20}} justify="center">
                    <Col span={6}>
                        <Image
                            className="img"
                            src={this.state.mammalInfo.mammal__img}
                            height={350} 
                            width={350}
                            fallback={ErrorImg}
                        />
                    </Col>
                    <Col span={16} style={{marginLeft: 40, marginTop: 5}}>
                        <Descriptions bordered size="middle">
                            <Descriptions.Item label="Name">{this.state.mammalInfo.mammal__name}</Descriptions.Item>
                            <Descriptions.Item label="Taxon Name">{this.state.mammalInfo.mammal__taxonName}</Descriptions.Item>
                            <Descriptions.Item label="Status">{this.state.mammalInfo.mammal__status}</Descriptions.Item>
                            <Descriptions.Item label="Average Length">
                                <Statistic 
                                    value={ this.state.mammalInfo.mammal__avg_length } 
                                    valueStyle={{fontSize: 15}} 
                                    suffix=" m" />
                            </Descriptions.Item>
                            <Descriptions.Item label="Average Mass">
                                <Statistic 
                                    value={ this.state.mammalInfo.mammal__avg_mass } 
                                    valueStyle={{fontSize: 15}} 
                                    suffix=" kg" />
                            </Descriptions.Item>
                            <Descriptions.Item label="Average Life Span">
                                <Statistic 
                                    value={ this.state.mammalInfo.mammal__eol_life_span } 
                                    valueStyle={{fontSize: 15}} 
                                    suffix=" years" />
                            </Descriptions.Item>
                            {this.state.mammalInfo.mammal__eol_geographic_distribution && this.state.mammalInfo.mammal__eol_geographic_distribution.length > 0 &&
                                <Descriptions.Item label="Distribution" span={3}>
                                    {this.state.mammalInfo.mammal__eol_geographic_distribution 
                                        && this.state.mammalInfo.mammal__eol_geographic_distribution.map((m, index) => 
                                        <Tag color="geekblue" key={index}>
                                            {m}
                                        </Tag>
                                    )}
                                </Descriptions.Item>
                            }
                            {this.state.mammalInfo.mammal__Key_Behaviors && this.state.mammalInfo.mammal__Key_Behaviors.length > 0 &&
                                <Descriptions.Item label="Behavior" span={3}>
                                    {this.state.mammalInfo.mammal__Key_Behaviors 
                                        && this.state.mammalInfo.mammal__Key_Behaviors.map((m, index) => 
                                        <Tag color="geekblue" key={index}>
                                            {m}
                                        </Tag>
                                    )}
                                </Descriptions.Item>
                            }
                            {this.state.mammalInfo.mammal__Communication_Channels && this.state.mammalInfo.mammal__Communication_Channels.length > 0 &&
                                <Descriptions.Item label="Communication Channels" span={3}>
                                    {this.state.mammalInfo.mammal__Communication_Channels 
                                        && this.state.mammalInfo.mammal__Communication_Channels.map((m, index) => 
                                        <Tag color="geekblue" key={index}>
                                            {m}
                                        </Tag>
                                    )}
                                </Descriptions.Item>
                            }
                            {this.state.mammalInfo.mammal__Animal_Foods && this.state.mammalInfo.mammal__Animal_Foods.length > 0 &&
                                <Descriptions.Item label="Animal Food" span={3}>
                                    {this.state.mammalInfo.mammal__Animal_Foods 
                                        && this.state.mammalInfo.mammal__Animal_Foods.map((m, index) => 
                                        <Tag color="geekblue" key={index}>
                                            {m}
                                        </Tag>
                                    )}
                                </Descriptions.Item>
                            }
                            {this.state.mammalInfo.mammal__Plant_Foods && this.state.mammalInfo.mammal__Plant_Foods.length > 0 &&
                                <Descriptions.Item label="Plant Food" span={3}>
                                    {this.state.mammalInfo.mammal__Plant_Foods 
                                        && this.state.mammalInfo.mammal__Plant_Foods.map((m, index) => 
                                        <Tag color="geekblue" key={index}>
                                            {m}
                                        </Tag>
                                    )}
                                </Descriptions.Item>
                            }
                        </Descriptions>
                    </Col>
                </Row>
                
                <Divider orientation="center" style={{fontSize: 30}}> Subspecies </Divider>
                <Link to={{
                        pathname: "/mammal/" + this.state.mammalID + "/map",
                    }}>
                    <Button type="primary"> Show on Map </Button>
                </Link>
                <Row justify="space-around" style={{marginTop: 20}}>
                    <Col span={20}>
                        <Row gutter={250}>
                            {this.state.subspecies.map((n, index) => 
                                <Col span={3} key={index}>
                                    <Card
                                        hoverable
                                        style={{ width: 180}}
                                        cover={<Image
                                                className="img"
                                                src={n.mammal__icon}
                                                height={180} 
                                                width={180}
                                                fallback={ErrorImg}
                                        />}>
                                        <Card.Meta 
                                            description={
                                                n.mammal__wiki_uri !== null 
                                                ?
                                                <a href={n.mammal__wiki_uri} target="_blank" rel="noreferrer">{n.mammal__name}</a>
                                                : 
                                                n.mammal__name
                                        }
                                        />
                                    </Card>
                                </Col>
                            )},
                        </Row>
                    </Col>
                </Row>

                <Divider orientation="center" style={{fontSize: 30}}> Ecoregion </Divider>
                <Row justify="center" style={{marginBottom: 30}}>
                        <Col span={24}>
                            {this.state.ecoregion.length > 0 &&
                                <Card>
                                    {this.state.ecoregion.map((eco, index) => (
                                        <Link to={"/ecoregion/" + eco[0]}>
                                            <Card.Grid 
                                                style={{width: '25%', textAlign: 'center', height: 80}} 
                                                key={index}
                                            >{eco[1]}</Card.Grid>
                                        </Link>
                                    ))}
                                </Card>
                            }
                        </Col>
                </Row>
                
                <Divider orientation="center" style={{fontSize: 30}}> Food Chain </Divider>
                <div>
                    <Row justify="center" style={{marginBottom: 30}}>
                        <Col span={24}>
                            <Collapse accordion defaultActiveKey={['1']}>
                                {this.state.predators.length > 0 && !this.state.predators[0].includes(null) &&
                                    <Collapse.Panel header="Mammal Predators" key="1">
                                        <Card>
                                            {this.state.predators.map((animal, index) => 
                                                <Link to={"/mammal/" + animal[0]}>
                                                    <Card.Grid 
                                                        style={{width: '25%', textAlign: 'center',}} 
                                                        key={index}
                                                    >{animal[1]}</Card.Grid>
                                                </Link>
                                            )}
                                        </Card>
                                    </Collapse.Panel>
                                }

                                {this.state.preys.length > 0 && !this.state.preys[0].includes(null) &&
                                    <Collapse.Panel header="Mammal Preys" key="2">
                                        <Card>
                                            {this.state.preys.map((animal, index) => 
                                                <Link to={"/mammal/" + animal[0]}>
                                                    <Card.Grid 
                                                        style={{width: '25%', textAlign: 'center'}} 
                                                        key={index}
                                                    >{animal[1]}</Card.Grid>
                                                </Link>
                                            )}
                                        </Card>

                                    </Collapse.Panel>
                                }

                                {this.state.competitors.length > 0 && !this.state.competitors[0].includes(null) &&
                                    <Collapse.Panel header="Mammal Competitors" key="3">
                                        <Card>
                                            {this.state.competitors.map((animal, index) => 
                                                <Link to={"/mammal/" + animal[0]}>
                                                    <Card.Grid 
                                                        style={{width: '25%', textAlign: 'center'}} 
                                                        key={index}
                                                    >{animal[1]}</Card.Grid>
                                                </Link>
                                            )}
                                        </Card>

                                    </Collapse.Panel>
                                }
                            </Collapse>
                       </Col>
                    </Row>

                    {this.state.nm_predators.length > 0 && 
                        <div style={{marginBottom: 30}}>
                            <Divider orientation="center" style={{fontSize: 15, fontWeight: "bold"}}> Other Predators </Divider>
                            <Row justify="center" style={{marginTop: 20}}>
                                <Col span={20}>
                                    <Row gutter={214}>
                                        {this.state.nm_predators.map((n, index) => 
                                            <Col span={3} key={index}>
                                                <Card
                                                    hoverable
                                                    style={{ width: 180}}
                                                    cover={<Image
                                                            className="img"
                                                            src={n.non_mammal__icon}
                                                            height={180} 
                                                            width={180}
                                                            fallback={ErrorImg}
                                                    />}>
                                                    <Card.Meta 
                                                        description={
                                                            n.non_mammal__wiki_uri !== null 
                                                            ?
                                                            <a href={n.non_mammal__wiki_uri} target="_blank" rel="noreferrer">{n.non_mammal__name}</a>
                                                            : 
                                                            n.non_mammal__name
                                                    }
                                                    />
                                                </Card>
                                            </Col>
                                        )},
                                    </Row>
                                </Col>
                            </Row>
                        </div>
                    }

                    {this.state.nm_preys.length > 0 && 
                        <div style={{marginBottom: 30}}>
                            <Divider orientation="center" style={{fontSize: 15, fontWeight: "bold"}}> Other Preys </Divider>
                            <Row justify="center" style={{marginTop: 20}}>
                                <Col span={20}>
                                    <Row gutter={214}>
                                        {this.state.nm_preys.map((n, index) => 
                                            <Col span={3} key={index}>
                                                <Card
                                                    hoverable
                                                    style={{ width: 180}}
                                                    cover={<Image
                                                            className="img"
                                                            src={n.non_mammal__icon}
                                                            height={180} 
                                                            width={180}
                                                            fallback={ErrorImg}
                                                    />}>
                                                    <Card.Meta 
                                                        description={
                                                            n.non_mammal__wiki_uri !== null 
                                                            ?
                                                            <a href={n.non_mammal__wiki_uri} target="_blank" rel="noreferrer">{n.non_mammal__name}</a>
                                                            : 
                                                            n.non_mammal__name
                                                    }
                                                    />
                                                </Card>
                                            </Col>
                                        )},
                                    </Row>
                                </Col>
                            </Row>
                        </div>
                    }

                    {this.state.nm_competitors.length > 0 && 
                        <div style={{marginBottom: 30}}>
                            <Divider orientation="center" style={{fontSize: 15, fontWeight: "bold"}}> Other Competitors </Divider>
                            <Row justify="center" style={{marginTop: 20}}>
                                <Col span={20}>
                                    <Row gutter={214}>
                                        {this.state.nm_competitors.map((n, index) => 
                                            <Col span={3} key={index}>
                                                <Card
                                                    hoverable
                                                    style={{ width: 180}}
                                                    cover={<Image
                                                            className="img"
                                                            src={n.non_mammal__icon}
                                                            height={180} 
                                                            width={180}
                                                            fallback={ErrorImg}
                                                    />}>
                                                    <Card.Meta 
                                                        description={
                                                            n.non_mammal__wiki_uri !== null 
                                                            ?
                                                            <a href={n.non_mammal__wiki_uri} target="_blank" rel="noreferrer">{n.non_mammal__name}</a>
                                                            : 
                                                            n.non_mammal__name
                                                    } />
                                                </Card>
                                            </Col>
                                        )},
                                    </Row>
                                </Col>
                            </Row>
                        </div>
                    }
                </div>
            </div>
        );
    }
}
