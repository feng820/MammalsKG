import { Col, Collapse, Descriptions, Divider, Image, Row } from 'antd';
import axios from 'axios';
import React, { Component } from 'react';
import ErrorImg from '../assets/No_image_available.svg';
const { Panel } = Collapse;

function Describe(props) {
    // console.log(props.ecoInfo.uri)
    return (
        <div>
            <Row style={{ marginTop: 20 }} justify="center">
                <Col span={6}>
                    <Image
                        className="img"
                        src={props.ecoInfo.ecoregion__image}
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
                        <Descriptions.Item label="Coordinates">{props.ecoInfo.ecoregion__coordinates}</Descriptions.Item>
                        <Descriptions.Item label="Area">{props.ecoInfo.ecoregion__Area}</Descriptions.Item>
                        <Descriptions.Item label="url" span={3}><a target="_blank" href={props.ecoInfo.ecoregion__url} rel="noreferrer">{props.ecoInfo.ecoregion__url}</a></Descriptions.Item>
                        <Descriptions.Item label="uri" span={3}>{props.ecoInfo.uri}</Descriptions.Item>
                    </Descriptions>
                </Col>
            </Row>


        </div>
    )
}

function Accordion(props) {
    const text = `
  A dog is a type of domesticated animal.
  Known for its loyalty and faithfulness,
  it can be found as a welcome guest in many households across the world.
    `;
    return (
        <Collapse accordion>
            <Panel header="This is panel header 1" key="1">
                <p>{text}</p>
            </Panel>
            <Panel header="This is panel header 2" key="2">
                <p>{text}</p>
            </Panel>
            <Panel header="This is panel header 3" key="3">
                <p>{text}</p>
            </Panel>
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
            })
            console.log(this.state.ecoInfo);
        }).catch(err => {
            const errMsg = err.message || 'Unknown error';
            console.error(errMsg);
        });
    }

    render() {
        return (
            <div>
                <Divider orientation="center" style={{ fontSize: 30 }}> Basic Information </Divider>
                <Describe
                    ecoInfo={this.state.ecoInfo}
                />
                <Divider orientation="center" style={{ fontSize: 30 }}> Fauna Information </Divider>
                <Accordion />
                <Divider orientation="center" style={{ fontSize: 30 }}> Flora Information </Divider>
                <Accordion />
            </div>
        );
    }
}
