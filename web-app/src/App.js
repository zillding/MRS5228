import React, { Component, PropTypes } from 'react';
import _ from 'lodash';

import { userData, itemData } from './data';

const spanStyle = {
  marginRight: 5
};

class Table extends Component {
  render() {
    const { data, k } = this.props;
    const array = _.map(data.sim, (value, key) => {
      return {
        id: key,
        sim: value
      };
    });
    const tableData = _.sortBy(array, 'sim').reverse().slice(0, k);
    console.log(tableData)

    return (
      <div>
        <table className="ui celled table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Centered Cosine Similarity</th>
            </tr>
          </thead>
          <tbody>
            {
              tableData.map(o =>
                <tr key={o.id}>
                  <td>{o.id}</td>
                  <td>{o.sim}</td>
                </tr>
              )
            }
          </tbody>
        </table>
      </div>
    );
  }
}

Table.propTypes = {
  data: PropTypes.object.isRequired,
  k: PropTypes.number.isRequired
};

class Result extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedItem: props.data[0].id
    }
  }

  _handleSelectChange(e) {
    const selectedItem = e.target.value;
    this.setState({ selectedItem });
  }

  render() {
    const { item, data, k } = this.props;
    const tableData = _.find(data, { id: this.state.selectedItem });

    return (
      <div>
        <div className="ui form">
          <div className="inline field">
            <label>Please select a {item}:</label>
            <select
              value={this.state.selectedItem}
              onChange={this._handleSelectChange.bind(this)}>
              {
                data.map(o =>
                  <option key={o.id} value={o.id}>{o.id}</option>
                )
              }
            </select>
          </div>
        </div>
        <div className="ui divider"></div>
        <Table data={tableData} k={k} />
      </div>
    );
  }
}

Result.propTypes = {
  item: PropTypes.string.isRequired,
  data: PropTypes.array.isRequired,
  k: PropTypes.number.isRequired
};

export class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      k: 3
    };
  }

  componentDidMount() {
    $('.menu .item').tab();
  }

  _handleSelectChange(e) {
    const k = parseInt(e.target.value);
    this.setState({ k });
  }

  render() {
    return (
      <div className="ui grid container">
        <div className="column">
          <h1>Recommender System</h1>
          <h3>Finding kNN</h3>
          <div className="ui form">
            <div className="inline field">
              <label>k =</label>
              <select
                value={this.state.k}
                onChange={this._handleSelectChange.bind(this)}>
                {
                  _.range(1, 10).map(value =>
                    <option key={value} value={value}>{value}</option>
                  )
                }
              </select>
            </div>
          </div>
          <div className="ui top attached tabular menu">
            <a className="active item" data-tab="first">user-user</a>
            <a className="item" data-tab="second">item-item</a>
          </div>
          <div className="ui bottom attached active tab segment" data-tab="first">
            <Result
              item={'user'}
              data={userData}
              k={this.state.k} />
          </div>
          <div className="ui bottom attached tab segment" data-tab="second">
            <Result
              item={'movie'}
              data={itemData}
              k={this.state.k} />
          </div>
        </div>
      </div>
    );
  }
}
