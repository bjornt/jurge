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
                    <NavbarBrand href="/">
                      <Media object src="/jurge-website-header.577x130.png">
                      </Media>
                    </NavbarBrand>
                </Navbar>
                <Navbar className="navbar-grey" expand="md">
                  <Nav>
                    <NavItem>
                      <NavLink href="#">Örhängen</NavLink>
                    </NavItem>
                    <NavItem>
                      <NavLink href="#">Ringar</NavLink>
                    </NavItem>
                    <NavItem>
                      <NavLink href="#">Armband</NavLink>
                    </NavItem>
                  </Nav>
                </Navbar>
            </div>
        );
    }
}

export default App;
