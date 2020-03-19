import React, { Component } from 'react'
import es6ClassBindAll from 'es6-class-bind-all'

export default class ParamForm extends Component {
    constructor(props) {
        super(props)
        this.state = {}
        es6ClassBindAll(this)
    }

    handleChange(e) {
        const key = e.target.id
        const value = e.target.value
        this.setState({ [key]: value })
    }

    handleSubmit(e) {
        e.preventDefault()
        this.props.onSubmit(this.state)
    }

    render() {
        return (
            <div className="param-form">
                <p>Red:</p>
                <input
                    type="text"
                    id="red"
                    onChange={this.handleChange}
                    value={this.state['red']}
                />
                <br />
                <p>Green:</p>
                <input
                    type="text"
                    id="green"
                    onChange={this.handleChange}
                    value={this.state['green']}
                />
                <br />
                <p>Blue:</p>
                <input
                    type="text"
                    id="blue"
                    onChange={this.handleChange}
                    value={this.state['blue']}
                />
                <br />
                <button onClick={this.handleSubmit}>Submit</button>
            </div>
        )
    }
}
