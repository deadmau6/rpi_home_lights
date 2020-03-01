import React, { Component } from 'react'
import es6ClassBindAll from 'es6-class-bind-all'
import socketIOClient from 'socket.io-client'

export default class Controller extends Component {
	constructor(props) {
		super(props)
		this.state = {
			currentText: '',
			messages: []
		}
		es6ClassBindAll(this)
		this.socket = socketIOClient('http://localhost:4000')
		this.socket.on('status', data => this.updateMessages(data.message))

	}

	updateMessages(message) {
		this.setState((prevState) => {
			const messages = [message, ...prevState.messages]
			return { messages, }
		})
	}

	handleText(event) {
		const currentText = event.target.value
		this.setState({ currentText, })
	}

	submitMessage(event) {
		event.preventDefault()
		this.socket.emit('lights', { message: this.state.currentText })
		this.setState({ currentText: '', })
	}

	componentWillUnmount() {
		this.socket.close()
		delete this.socket
	}

	render() {
		return (
			<div className="controller">
			<input type="text" onChange={this.handleText}/>
			<button onClick={this.submitMessage}>Submit</button>
			<ul>
			{
				this.state.messages.map((msg, i) => {
					return (<li key={i}>msg</li>) 
				})
			}
			</ul>
			</div>
		)
	}
}