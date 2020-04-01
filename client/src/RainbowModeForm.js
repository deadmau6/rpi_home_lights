import React, { Component } from 'react'
import es6ClassBindAll from 'es6-class-bind-all'
import { Form, Button } from 'react-bootstrap'

export default class RainbowModeForm extends Component {
    constructor(props) {
        super(props)
        this.state = {
            wait: 0.01,
        }
        es6ClassBindAll(this)
    }

    handleChange(event) {
        const value = event.target.value
        this.setState({ wait: value })
    }

    handleSubmit(e) {
        e.preventDefault()
        this.props.onSubmit('RAINBOW', this.state)
    }

    render() {
        return (
            <Form className="rainbow-mode-form">
                <Form.Group controlId="formBasicRange">
                    <Form.Label>Refresh Speed:</Form.Label>
                    <Form.Control
                        type="range"
                        value={this.state.wait}
                        onChange={this.handleChange}
                        min="0.01"
                        max="1.0"
                        step="0.01"
                    />
                </Form.Group>
                <p>{`(${this.state.wait}ms)`}</p>
                <Button onClick={this.handleSubmit}>Submit</Button>
            </Form>
        )
    }
}
