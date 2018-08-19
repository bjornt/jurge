import React, { Component } from 'react';
import {
    Collapse,
    Media,
    Navbar,
    NavbarToggler,
    NavbarBrand,
    Nav,
    NavItem,
    NavLink,
    Container,
    Row,
    Col,
    Jumbotron,
    Button
} from 'reactstrap';
import './App.css';

export class Earrings extends Component {

    render() {
        return (
            <Products category="earrings">
            </Products>
        );
    }
}


export class Rings extends Component {

    render() {
        return (
            <Products category="rings">
            </Products>
        );
    }
}


export class Bracelets extends Component {

    render() {
        return (
            <Products category="bracelets">
            </Products>
        );
    }
}


class Products extends Component {
    render() {
        return (
            <div>
                {this.props.category}
            </div>
        );
    }
}
