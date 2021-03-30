import React, { Component } from 'react';
import { Input, Table, Tag, Alert, Button, Select, Form, Slider } from 'antd';
import axios from 'axios';
import { Link } from "react-router-dom";


export class SearchBar extends Component {
    constructor() {
        super()
        this.state = {
            dataSource: [],
            showResult: false
        };
        
        this.formRef = React.createRef();

        this.colors = ['geekblue', 'purple', 'magenta', 'cyan', 'green', 'yellow'];
    
        this.columns = [
            {
                title: 'Name',
                dataIndex: 'name',
                key: 'name',
                render: text => <a className="name">{text}</a>,
            },
            {
                title: 'Common Names',
                dataIndex: 'commonNames',
                key: 'commonNames',
                render: commonNames => (
                    <>
                      {commonNames.map(commonName => {
                        let color = this.colors[Math.floor(Math.random() * this.colors.length)]
                        return (
                          <Tag color={color} key={commonName}>
                            {commonName}
                          </Tag>
                        );
                      })}
                    </>
                ),
            },
            {
                title: 'Action',
                key: 'action',
                render: (text, record) => (
                    <Link to={"/mammal/" + record.id}>
                        <Button type="primary">Detail</Button>
                    </Link>
                )
            }
        ];
    }

    onFinish = params => {
        if (params.length_range !== undefined) {
            params.length_range = JSON.stringify(params.length_range)
        }
        if (params.mass_range !== undefined) {
            params.mass_range = JSON.stringify(params.mass_range)
        }
        if (params.lifespan_range !== undefined) {
            params.lifespan_range = JSON.stringify(params.lifespan_range)
        }
        const url = "http://127.0.0.1:5000/search";
        axios.get(url, {
            params: params
        }).then(res => {
            console.log("fetch search result success");
            const resultArr = res.data;
            this.setState({
                dataSource: resultArr.map(
                    (info, index) => ({
                        'key': index,
                        'name': info.name,
                        'id': info.id,
                        'commonNames': info.commonNames
                    })
                ),
                showResult: true
            });
        }).catch(e => {
            const error = e.error || 'Unknown Error';
            console.log("Cannot fetch due to error: " + error);
        })
    }

    onReset = () => {
        this.formRef.current.resetFields();
        this.setState({
            showResult: false
        })
    }
    
    render() {
        const layout = {
            labelCol: {
              span: 8,
            },
            wrapperCol: {
              span: 8,
            },
        };

        const tailLayout = {
            wrapperCol: {
              offset: 8,
              span: 8,
            },
        };
        
        return (
            <div>
                <Form 
                    {...layout} 
                    onFinish={this.onFinish.bind(this)} 
                    ref={this.formRef}
                >
                    <Form.Item
                        name="keyword"
                        label="Keyword"
                    >
                        <Input 
                            className="search-bar"
                            placeholder="input mammal keyword" 
                        />
                    </Form.Item> 

                    <Form.Item
                        name="status"
                        label="Status"
                        style={{marginBottom: 15}}  
                    >
                        <Select 
                            style={{width: 200, display: "flex"}}
                        >
                            <Select.Option value="least concern">Least concern</Select.Option>
                            <Select.Option value="vulnerable">Vulnerable</Select.Option>
                            <Select.Option value="endangered species">Endangered</Select.Option>
                            <Select.Option value="critically endangered">Critically endangered</Select.Option>
                            <Select.Option value="Near threatened">Near threatened</Select.Option>
                            <Select.Option value="extinct in the wild">Extinct in the wild</Select.Option>
                            <Select.Option value="extinct species">Extinct</Select.Option>
                        </Select> 
                    </Form.Item>

                    <Form.Item
                        name="length_range"
                        label="Length (m)"
                        style={{marginBottom: 10}}
                    >
                        <Slider 
                            range 
                            max={35}
                            marks={
                                {
                                    0: '0',
                                    35: '35'
                                }
                            }
                        />
                    </Form.Item>

                    <Form.Item
                        name="mass_range"
                        label="Mass (kg)"
                        style={{marginBottom: 10}}>
                        <Slider 
                            range 
                            max={1000}
                            marks={
                                {
                                    0: '0',
                                    100: '100',
                                    500: '500',
                                    1000: '1000'
                                }
                            }
                        />
                    </Form.Item>

                    <Form.Item
                        name="lifespan_range"
                        label="Life Span (years)"
                        style={{marginBottom: 10}}>
                        <Slider 
                            range 
                            max={130}
                            marks={
                                {
                                    0: '0',
                                    50: '50',
                                    130: '130'
                                }
                            }
                        />
                    </Form.Item>

                    <Form.Item {...tailLayout}>
                        <Button type="primary" htmlType="submit">
                        Submit
                        </Button>
                        <Button htmlType="button" onClick={this.onReset.bind(this)}>
                        Reset
                        </Button>
                    </Form.Item>

                </Form>

                {this.state.showResult && 
                    (this.state.dataSource.length > 0 ?
                        <Table 
                            className="search-result"
                            columns={this.columns}
                            dataSource={this.state.dataSource}
                            pagination={{ pageSize: 5 }}
                        /> 
                        : 
                        <Alert
                            className="search-alert"
                            message="No mammals matched!"
                            type="error"
                            showIcon
                        />
                    )
                }
            </div>
        );
    }
}
