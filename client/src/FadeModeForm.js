import React, { Component } from 'react'
import es6ClassBindAll from 'es6-class-bind-all'
import { Form, Button } from 'react-bootstrap'
import { SliderPicker, MaterialPicker } from 'react-color'

export default class FadeModeForm extends Component {
    constructor(props) {
        super(props)
        this.state = {
            hex: '#333',
            cycle: true,
            num_of_colors: 3,
            steps: 3,
            red: 0,
            green: 0,
            blue: 0,
        }
        es6ClassBindAll(this)
    }

    handleChange(event) {
        const key = event.target.id
        const value = event.target.value
        this.setState({ [key]: value })
    }

    handleColor(color) {
        const {red, green, blue} = color.rgb
        this.setState({ red, green, blue, hex: color.hex })
    }

    handleSubmit(e) {
        e.preventDefault()
        this.props.onSubmit('FADE', {
            cycle: this.state.cycle,
            num_of_colors: this.state.num_of_colors,
            steps: this.state.steps,
            red: this.state.red,
            green: this.state.green,
            blue: this.state.blue,
        })
    }

    render() {
        return (
            <Form className="fade-mode-form">
                <Form.Group controlId="formCycle">
                    <Form.Check
                        type='checkbox'
                        id='cycle'
                        label='Cycle'
                        value={!this.state.cycle}
                        onSelect={this.handleChange}
                    />
                </Form.Group>
                <Form.Group controlId="formNumColors">
                    <Form.Label>Colors:</Form.Label>
                    <Form.Control
                        id='num_of_colors'
                        value={this.state.num_of_colors}
                        onChange={this.handleChange}
                    />
                </Form.Group>
                <Form.Group controlId="formSteps">
                    <Form.Label>Steps:</Form.Label>
                    <Form.Control
                        id='steps'
                        value={this.state.steps}
                        onChange={this.handleChange}
                    />
                </Form.Group>
                <br />
                <MaterialPicker
                    color={this.state.hex}
                    onChangeComplete={this.handleColor}
                />
                <br />
                <SliderPicker
                    color={this.state.hex}
                    onChangeComplete={this.handleColor}
                />
                <br />
                <Button onClick={this.handleSubmit}>Submit</Button>
            </Form>
        )
    }
}
