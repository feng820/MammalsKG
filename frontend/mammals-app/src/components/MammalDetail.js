import React, { Component } from 'react';

export class MammalDetail extends Component {
    constructor(props) {
        super();
        this.mammalID = props.match.params.mammalId;
    }

    render() {
        return (
            <div>
                Mammals Detail for { this.mammalID }
            </div>
        );
    }
}
