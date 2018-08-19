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
import { Link, Route, Switch } from 'react-router-dom';
import './App.css';

import { Bracelets, Earrings, Rings } from './Products.js';

class App extends Component {
    constructor(props) {
        super(props);

        this.toggle = this.toggle.bind(this);
        this.state = {
            isOpen: false
        };
    }
    toggle() {
        this.setState({
            isOpen: !this.state.isOpen
        });
    }
    render() {
        return (
            <div>
                <Navbar light expand="md" className="d-flex justify-content-center">
                    <NavbarBrand tag={Link} to='/'>
                      <Media object src="/jurge-website-header.577x130.png">
                      </Media>
                    </NavbarBrand>
                </Navbar>
                <Navbar className="navbar-grey" expand="md">
                  <Nav>
                    <NavItem>
                      <NavLink tag={Link} to='/earrings'>Örhängen</NavLink>
                    </NavItem>
                    <NavItem>
                      <NavLink tag={Link} to='/rings'>Ringar</NavLink>
                    </NavItem>
                    <NavItem>
                      <NavLink tag={Link} to='/bracelets'>Armband</NavLink>
                    </NavItem>
                  </Nav>
                </Navbar>
                <Switch>
                  <Route exact path='/' component={Earrings}/>
                  <Route exact path='/earrings' component={Earrings}/>
                  <Route exact path='/rings' component={Rings}/>
                  <Route exact path='/bracelets' component={Bracelets}/>
                </Switch>
            </div>
        );
    }
}

export default App;
