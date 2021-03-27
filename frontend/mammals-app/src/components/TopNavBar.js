import React, { Component } from 'react';
import logo from '../assets/logo.svg';
import { Link } from "react-router-dom"; 

export class TopNavBar extends Component {
    render() {
        return (
            <header className="nav-header">
                <Link to="/">
                    <img src={logo} className="nav-logo" alt="logo" />
                </Link>
            </header>
        );
    }
}
