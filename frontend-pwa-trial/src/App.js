import React, { Component } from 'react';
import logo from './logo.svg';
import axios from 'axios';
import './App.css';

class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      btcPrice: null
    };
  }

  componentDidMount() {
    console.log("MOUNTED");
    axios.get('https://api.coindesk.com/v1/bpi/currentprice/BTC.json')
      .then(res => {
        const price = Math.trunc(parseFloat(res.data.bpi.USD.rate.replace(',', '')));
        this.setState({ btcPrice: price });
        localStorage.setItem('btcPrice', price);
        console.log(price);
      })
      .catch(err => {
        const price = localStorage.getItem('btcPrice');
        console.log(price, " from localStorage");
        if (price) {
          this.setState({ btcPrice: price })
        } else {
          this.setState({ btcPrice: "Not cached." });
        }
      });
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload. -- {this.state.btcPrice}
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header>
      </div>
    );
  }
}

export default App;
