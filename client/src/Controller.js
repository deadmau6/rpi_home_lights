import React, { Component } from 'react'
import es6ClassBindAll from 'es6-class-bind-all'
import socketIOClient from 'socket.io-client'
import ParamForm from './ParamForm'

export default class Controller extends Component {
    constructor(props) {
        super(props)
        this.state = {
            mode: 'SINGLE',
            modeParams: {},
            status: {},
        }
        es6ClassBindAll(this)
        this.socket = socketIOClient('http://192.168.1.16:4000')
        this.socket.on('status', data => this.updateStatus(data))
    }

    updateStatus(data) {
        const update = data['update'] || {}
        const params = update['params']
            ? Object.entries(update['params']).map(
                  ([key, value]) => `${key}=${value} `
              )
            : []
        this.setState({
            status: {
                status: data['status'],
                mode: update['mode'],
                params: params,
            },
        })
    }

    submitMessage(params) {
        this.socket.emit('lights', {
            status: 'running',
            mode: this.state.mode,
            mode_params: params,
        })
        this.setState({ modeParams: params })
    }

    componentWillUnmount() {
        this.socket.close()
        delete this.socket
    }

    render() {
        return (
            <div className="controller">
                <ParamForm onSubmit={this.submitMessage} />
                <div className="item-1">
                    <h3>Your Last Request:</h3>
                    <br />
                    <p>
                        {this.state.mode}: {'{'}
                    </p>
                    {Object.entries(this.state.modeParams).map(
                        ([key, value]) => (
                            <p>
                                {key}: {value}
                            </p>
                        )
                    )}
                    <p>{'{'}</p>
                </div>
                <div className="item-2">
                    <h3>Current Lights Status:</h3>
                    <br />
                    <p>{'{'}</p>
                    {Object.entries(this.state.status).map(([key, value]) => (
                        <p>
                            {key}: {value}
                        </p>
                    ))}
                    <p>{'{'}</p>
                </div>
            </div>
        )
    }
}
