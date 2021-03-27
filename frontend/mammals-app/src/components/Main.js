import React, { Component } from 'react';
import { SearchBar } from './SearchBar';

export class Main extends Component {
    render() {
        return (
            <div>
                <h1 className="title">Mammals KG</h1>
                <SearchBar />
            </div>
        );
    }
}
