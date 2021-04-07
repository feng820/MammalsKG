import React, { Component } from 'react';

export class Ecoregion extends Component {
    constructor(props) {
        super();
        console.log(props.match.params.ecoId);
    }

    render() {
        return (
            <div>
                Hello Ecoregion
            </div>
        );
    }
}
