import React, { Component } from 'react'
import es6ClassBindAll from 'es6-class-bind-all'
import { Button } from 'react-bootstrap'
import { SliderPicker, MaterialPicker } from 'react-color'

export default class SingleModeForm extends Component {
    constructor(props) {
        super(props)
        this.state = {
            hex: '#333',
            rgb: {
                red: 0,
                green: 0,
                blue: 0,
            },
        }
        es6ClassBindAll(this)
    }

    handleChange(color) {
        const newRGB = {
            red: color.rgb.r,
            green: color.rgb.g,
            blue: color.rgb.b,
        }
        this.setState({ hex: color.hex, rgb: newRGB })
    }

    handleSubmit(e) {
        e.preventDefault()
        this.props.onSubmit('SINGLE', this.state.rgb)
    }

    render() {
        return (
            <div className="single-mode-form">
                <br />
                <MaterialPicker
                    color={this.state.hex}
                    onChangeComplete={this.handleChange}
                />
                <br />
                <SliderPicker
                    color={this.state.hex}
                    onChangeComplete={this.handleChange}
                />
                <br />
                <Button onClick={this.handleSubmit}>Submit</Button>
            </div>
        )
    }
}
